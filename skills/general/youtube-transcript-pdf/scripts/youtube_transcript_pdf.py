#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = Path.home() / ".local/share/pandoc/templates/eisvogel.latex"
DEFAULT_WHISPER_PYTHON = Path.home() / ".local/share/youtube-transcript-pdf/whisper-venv/bin/python"
DEFAULT_WHISPERX_PYTHON = Path.home() / ".local/share/youtube-transcript-pdf/whisperx-venv/bin/python"
DEFAULT_THEME = SKILL_ROOT / "themes/dario-blog.tex"
DEFAULT_CSS = SKILL_ROOT / "themes/dario-light.css"
DEFAULT_HF_TOKEN_FILE = Path.home() / ".config/youtube-transcript-pdf/huggingface.env"

DEFAULT_BRIEF_SUMMARY = "Brief summary not provided."
DEFAULT_DETAILED_SUMMARY = "Detailed summary not provided."
DEFAULT_SUMMARY_PROVIDER = "codex"
DEFAULT_SUMMARY_TIMEOUT_SECONDS = 240
DEFAULT_SUMMARY_CODEX_HOME = Path.home() / ".codex"
DEFAULT_LLM_CLEANUP_TIMEOUT_SECONDS = 360
SUMMARY_STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "because",
    "been",
    "before",
    "being",
    "could",
    "does",
    "doing",
    "down",
    "each",
    "from",
    "have",
    "here",
    "into",
    "just",
    "like",
    "more",
    "much",
    "only",
    "other",
    "over",
    "people",
    "really",
    "should",
    "some",
    "such",
    "than",
    "that",
    "their",
    "there",
    "these",
    "they",
    "thing",
    "think",
    "this",
    "those",
    "through",
    "very",
    "what",
    "when",
    "where",
    "which",
    "while",
    "will",
    "with",
    "work",
    "would",
    "your",
}

FILLER_ONLY = re.compile(r"^(?:um+|uh+|ah+|er+|erm+|hmm+|mm+|mhm+)[,.\s-]*$", re.I)
FILLER_INLINE = re.compile(r"\b(?:um+|uh+|ah+|er+|erm+)\b[, ]*", re.I)
STUTTER = re.compile(r"\b([A-Za-z]{2,})[-\s]+\1\b", re.I)
SPEAKER_LABEL = re.compile(r"^\[(SPEAKER_[A-Z0-9_]+|SPEAKER_UNKNOWN)\]\s*(.*)$")

COMMON_ASR_FIXES = {
    r"\bai\b": "AI",
    r"\ba i\b": "AI",
    r"\bagi\b": "AGI",
    r"\bllm\b": "LLM",
    r"\bllms\b": "LLMs",
    r"\brl\b": "RL",
    r"\btd learning\b": "TD learning",
    r"\btemporal difference\b": "temporal-difference",
    r"\bback propagation\b": "backpropagation",
    r"\bdeep mind\b": "DeepMind",
    r"\bopen ai\b": "OpenAI",
    r"\balph go\b": "AlphaGo",
    r"\balpha fold\b": "AlphaFold",
    r"\balpha proof\b": "AlphaProof",
    r"\bgt sophie\b": "Gran Turismo Sophy",
    r"\bal claw code\b": "Claude Code",
    r"\brl lift\b": "RL Lyft",
    r"\bjeff bar\b": "JEPA",
    r"\bjet bra\b": "JEPA",
    r"\bjetbra\b": "JEPA",
    r"\bjeppa\b": "JEPA",
    r"\bami\b": "AMI",
    r"\bcompany, me\b": "company, AMI",
    r"\bi mean labs\b": "AMI Labs",
    r"\bfor more information\b": "more information",
    r"\brich sudden\b": "Rich Sutton",
    r"\brichard sudden\b": "Richard Sutton",
    r"\bsutton's\b": "Sutton's",
    r"\bbackforth\b": "back-and-forth",
    r"\bworldchanging\b": "world-changing",
    r"\boperate conditioning\b": "operant conditioning",
    r"\bsarcastic aspects\b": "stochastic aspects",
    r"\bback prop\b": "backprop",
    r"\bbackrop\b": "backprop",
    r"\bno novel\b": "novel",
    r"\bnever easier easy\b": "never easy",
    r"\bthe if the\b": "if the",
    r"\bget us get us\b": "get us",
    r"\band science and and programming\b": "and programming",
    r"\bevaluation or attention\b": "evaluation or retention",
    r"\bis it is\b": "it is",
    r"\bu the\b": "the",
}

TOPIC_HEADINGS = [
    (
        "Generative AI, Novelty, and Goodness",
        ("generative ai", "novel", "good", "mimic", "hallucinations", "stochastic"),
    ),
    (
        "Discovery Beyond Mimicry",
        ("discovery", "creativity", "science", "mathematics", "alphago", "alphafold"),
    ),
    (
        "Evaluation and Selective Retention",
        ("evaluation", "retention", "variation", "objective", "value", "generated"),
    ),
    (
        "Variation, Backpropagation, and Plasticity",
        ("backprop", "variation", "random", "initialized", "plasticity", "continual"),
    ),
    (
        "Autonomous AI Scientists",
        ("autonomous", "scientists", "goals", "goal", "participate", "automate creativity"),
    ),
    (
        "Reinforcement Learning and Intelligence",
        ("reinforcement learning", "reward", "agent", "policy", "control", "prediction"),
    ),
    (
        "Experience, Search, and Planning",
        ("experience", "search", "planning", "model", "simulation", "trajectory"),
    ),
    (
        "Scaling, Computation, and the Bitter Lesson",
        ("scale", "computation", "compute", "bitter lesson", "general methods", "learning"),
    ),
    (
        "Neural Networks and Representation",
        ("neural", "representation", "deep learning", "features", "backpropagation", "network"),
    ),
    (
        "Human Knowledge and AI Research",
        ("human knowledge", "knowledge", "research", "scientist", "expert", "hand"),
    ),
    (
        "Questions and Discussion",
        ("question", "audience", "ask", "answer", "discussion"),
    ),
]


def run(
    cmd: list[str],
    *,
    capture: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd,
            check=True,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        if capture and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        raise


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"missing required tool: {name}")


def require_path(path: Path, description: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing {description}: {path}")


def whisper_env(whisper_python: Path) -> dict[str, str]:
    env = os.environ.copy()
    site_packages = whisper_python.parent.parent / "lib" / "python3.11" / "site-packages"
    nvidia_root = site_packages / "nvidia"
    lib_dirs = sorted(nvidia_root.glob("*/lib")) if nvidia_root.exists() else []
    existing = env.get("LD_LIBRARY_PATH")
    paths = [str(path) for path in lib_dirs if path.exists()]
    if existing:
        paths.append(existing)
    if paths:
        env["LD_LIBRARY_PATH"] = ":".join(paths)
    return env


def load_hf_token(token_file: Path) -> str | None:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if token:
        return token.strip()
    if not token_file.exists():
        return None
    for line in token_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() in {"HF_TOKEN", "HUGGINGFACE_TOKEN"}:
            return value.strip().strip('"').strip("'")
    return None


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value[:80] or fallback


def apply_asr_fixes(text: str) -> str:
    for pattern, replacement in COMMON_ASR_FIXES.items():
        text = re.sub(pattern, replacement, text, flags=re.I)
    text = STUTTER.sub(r"\1", text)
    text = re.sub(r"\b(if|as|some|now|AI)\s+\1\b", r"\1", text, flags=re.I)
    text = re.sub(r"\bgener\s+generative\b", "generative", text, flags=re.I)
    text = re.sub(r"\bthat I that is\b", "that is", text, flags=re.I)
    text = re.sub(r"\bwe the evaluation\b", "we, the evaluation", text, flags=re.I)
    text = re.sub(r"\bit but\b", "but", text, flags=re.I)
    return text


def choose_lang(info: dict, forced: str | None) -> tuple[str, bool]:
    if forced:
        is_manual = forced in (info.get("subtitles") or {})
        return forced, is_manual

    subtitles = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}

    manual_english = sorted(k for k in subtitles if k == "en" or k.startswith("en-"))
    if manual_english:
        return manual_english[0], True

    for candidate in ("en-orig", "en"):
        if candidate in auto:
            return candidate, False

    auto_english = sorted(k for k in auto if k == "en" or k.startswith("en-"))
    if auto_english:
        return auto_english[0], False

    raise SystemExit("no English subtitle or auto-caption track found")


def extract_caption_text(subtitle_json: Path) -> list[str]:
    if subtitle_json.suffix.lower() == ".vtt":
        return extract_vtt_text(subtitle_json)

    data = json.loads(subtitle_json.read_text())
    chunks: list[str] = []
    for event in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in event.get("segs") or [])
        text = html.unescape(text).replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        if text and text != "\u266a":
            chunks.append(text)

    cleaned: list[str] = []
    previous = None
    for chunk in chunks:
        if chunk != previous:
            cleaned.append(chunk)
        previous = chunk
    return cleaned


def parse_timestamp(value: str) -> float:
    value = value.strip().replace(",", ".")
    parts = value.split(":")
    seconds = float(parts[-1])
    if len(parts) >= 2:
        seconds += int(parts[-2]) * 60
    if len(parts) >= 3:
        seconds += int(parts[-3]) * 3600
    return seconds


def extract_vtt_events(vtt_path: Path) -> list[dict]:
    events: list[dict] = []
    current_start: float | None = None
    current_end: float | None = None
    current_text: list[str] = []

    def flush() -> None:
        nonlocal current_start, current_end, current_text
        if current_start is None or current_end is None:
            current_text = []
            return
        text = " ".join(current_text)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        if text:
            events.append({
                "tStartMs": int(current_start * 1000),
                "dDurationMs": max(1, int((current_end - current_start) * 1000)),
                "segs": [{"utf8": text}],
            })
        current_start = None
        current_end = None
        current_text = []

    for raw_line in vtt_path.read_text(errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line == "WEBVTT" or line.startswith(("NOTE", "STYLE", "REGION")):
            flush()
            continue
        if "-->" in line:
            flush()
            start, end = line.split("-->", 1)
            current_start = parse_timestamp(start)
            current_end = parse_timestamp(end.split()[0])
            current_text = []
            continue
        if current_start is not None:
            current_text.append(line)
    flush()
    return events


def extract_vtt_text(vtt_path: Path) -> list[str]:
    return [
        "".join(seg.get("utf8", "") for seg in event.get("segs") or []).strip()
        for event in extract_vtt_events(vtt_path)
        if event.get("segs")
    ]


def ensure_json3_subtitle(subtitle_path: Path, out_dir: Path, lang: str) -> Path:
    if subtitle_path.suffix.lower() == ".json3":
        return subtitle_path
    if subtitle_path.suffix.lower() != ".vtt":
        raise SystemExit(f"unsupported subtitle format for diarization: {subtitle_path.suffix}")
    output_path = out_dir / f"{subtitle_path.stem}.json3"
    output_path.write_text(json.dumps({"events": extract_vtt_events(subtitle_path)}, ensure_ascii=False, indent=2))
    return output_path


def write_whisper_json3(segments: list[dict], output_path: Path) -> Path:
    events = []
    for segment in segments:
        text = re.sub(r"\s+", " ", str(segment.get("text") or "")).strip()
        if not text:
            continue
        start = float(segment.get("start") or 0)
        end = max(float(segment.get("end") or start), start)
        events.append({
            "tStartMs": int(start * 1000),
            "dDurationMs": max(1, int((end - start) * 1000)),
            "segs": [{"utf8": text}],
        })
    output_path.write_text(json.dumps({"events": events}, ensure_ascii=False, indent=2))
    return output_path


def download_audio(url: str, out_dir: Path) -> Path:
    output_template = str(out_dir / "whisper-audio.%(ext)s")
    run([
        "yt-dlp",
        "--no-playlist",
        "-f",
        "bestaudio/best[height<=360]/worst",
        "-x",
        "--audio-format",
        "m4a",
        "--audio-quality",
        "0",
        "-o",
        output_template,
        url,
    ])
    audio_path = out_dir / "whisper-audio.m4a"
    if audio_path.exists():
        return audio_path
    audio_candidates = sorted(
        p
        for p in out_dir.glob("whisper-audio.*")
        if p.suffix.lower() not in {".json", ".part", ".ytdl"}
    )
    if not audio_candidates:
        raise SystemExit("yt-dlp did not produce an audio file for Whisper transcription")
    return audio_candidates[-1]


def normalize_audio_for_diarization(audio_path: Path, out_dir: Path) -> Path:
    output_path = out_dir / "diarization-audio.wav"
    if output_path.exists() and output_path.stat().st_size > 0:
        return output_path
    run([
        "ffmpeg",
        "-y",
        "-i",
        str(audio_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-vn",
        str(output_path),
    ])
    return output_path


def transcribe_with_whisper(
    audio_path: Path,
    out_dir: Path,
    *,
    whisper_python: Path,
    model: str,
    device: str,
    compute_type: str,
    lang: str,
) -> Path:
    require_path(whisper_python, "Whisper Python interpreter")
    output_path = out_dir / f"whisper.{lang}.json3"
    transcriber = r"""
import json
import sys
from faster_whisper import WhisperModel

audio_path, model_name, device, compute_type, language = sys.argv[1:6]
model = WhisperModel(model_name, device=device, compute_type=compute_type)
segments, _ = model.transcribe(audio_path, language=language, vad_filter=True)
print(json.dumps([
    {"start": segment.start, "end": segment.end, "text": segment.text}
    for segment in segments
], ensure_ascii=False))
"""
    try:
        result = run(
            [
                str(whisper_python),
                "-c",
                transcriber,
                str(audio_path),
                model,
                device,
                compute_type,
                lang.split("-")[0],
            ],
            capture=True,
            env=whisper_env(whisper_python),
        )
    except subprocess.CalledProcessError:
        if device != "cpu":
            result = run(
                [
                    str(whisper_python),
                    "-c",
                    transcriber,
                    str(audio_path),
                    model,
                    "cpu",
                    "int8",
                    lang.split("-")[0],
                ],
                capture=True,
                env=whisper_env(whisper_python),
            )
        else:
            raise
    return write_whisper_json3(json.loads(result.stdout), output_path)


def diarize_with_pyannote(
    audio_path: Path,
    subtitle_json: Path,
    out_dir: Path,
    *,
    whisper_python: Path,
    hf_token: str,
    lang: str,
) -> Path:
    require_path(whisper_python, "Whisper Python interpreter")
    audio_path = normalize_audio_for_diarization(audio_path, out_dir)
    source_stem = re.sub(r"[^A-Za-z0-9_.-]+", "-", subtitle_json.stem)
    output_path = out_dir / f"{source_stem}.diarized.json3"
    diarizer = r"""
import json
import os
import sys

import torch

try:
    from pyannote.audio import Pipeline
except ModuleNotFoundError:
    raise SystemExit(
        "pyannote.audio is not installed in the Whisper venv. Install torch and pyannote.audio "
        "there before using --diarize pyannote."
    )

audio_path, subtitle_path, output_path = sys.argv[1:4]
token = os.environ.get("HF_TOKEN")
if not token:
    raise SystemExit("HF_TOKEN is required for pyannote diarization")

data = json.loads(open(subtitle_path, encoding="utf-8").read())
events = []
for event in data.get("events", []):
    start = float(event.get("tStartMs") or 0) / 1000.0
    duration = float(event.get("dDurationMs") or 0) / 1000.0
    text = "".join(seg.get("utf8", "") for seg in event.get("segs") or []).strip()
    if text:
        events.append({"start": start, "end": start + max(duration, 0.001), "text": text})

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", token=token)
if torch.cuda.is_available():
    pipeline.to(torch.device("cuda"))
diarization_output = pipeline(str(audio_path))
diarization = getattr(diarization_output, "speaker_diarization", diarization_output)
turns = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    turns.append({"start": float(turn.start), "end": float(turn.end), "speaker": speaker})

def speaker_for(start, end):
    best = None
    best_overlap = 0.0
    for turn in turns:
        overlap = max(0.0, min(end, turn["end"]) - max(start, turn["start"]))
        if overlap > best_overlap:
            best_overlap = overlap
            best = turn["speaker"]
    return best or "SPEAKER_UNKNOWN"

diarized_events = []
last_speaker = None
for event in events:
    speaker = speaker_for(event["start"], event["end"])
    text = event["text"]
    if speaker != last_speaker:
        text = f"[{speaker}] {text}"
        last_speaker = speaker
    diarized_events.append({
        "tStartMs": int(event["start"] * 1000),
        "dDurationMs": max(1, int((event["end"] - event["start"]) * 1000)),
        "segs": [{"utf8": text}],
    })

open(output_path, "w", encoding="utf-8").write(json.dumps({
    "events": diarized_events,
    "diarization": turns,
}, ensure_ascii=False, indent=2))
"""
    env = whisper_env(whisper_python)
    env["HF_TOKEN"] = hf_token
    run(
        [
            str(whisper_python),
            "-c",
            diarizer,
            str(audio_path),
            str(subtitle_json),
            str(output_path),
        ],
        env=env,
    )
    return output_path


def env_with_hf_token(python_path: Path, hf_token: str) -> dict[str, str]:
    env = whisper_env(python_path)
    env["HF_TOKEN"] = hf_token
    return env


def normalize_whisperx_words(whisperx_json: Path) -> list[dict]:
    data = json.loads(whisperx_json.read_text(encoding="utf-8"))
    words = []
    for word in data.get("word_segments") or []:
        text = re.sub(r"\s+", " ", str(word.get("word") or "")).strip()
        speaker = str(word.get("speaker") or "SPEAKER_UNKNOWN")
        start = word.get("start")
        end = word.get("end")
        if text and start is not None and end is not None:
            words.append({
                "text": text,
                "speaker": speaker,
                "start": float(start),
                "end": float(end),
            })
    return smooth_tiny_speaker_runs(words)


def smooth_tiny_speaker_runs(items: list[dict]) -> list[dict]:
    if len(items) < 3:
        return items

    runs: list[dict] = []
    for item in items:
        if runs and runs[-1]["speaker"] == item["speaker"]:
            runs[-1]["words"].append(item)
        else:
            runs.append({"speaker": item["speaker"], "words": [item]})

    def duration(run: dict) -> float:
        return float(run["words"][-1]["end"] - run["words"][0]["start"])

    def word_count(run: dict) -> int:
        return len(run["words"])

    for index, run in enumerate(runs):
        if run["speaker"] == "SPEAKER_UNKNOWN":
            continue
        tiny = word_count(run) <= 2 or duration(run) <= 0.65
        short_fragment = word_count(run) <= 3 and duration(run) <= 1.15
        if not (tiny or short_fragment):
            continue

        previous_run = runs[index - 1] if index > 0 else None
        next_run = runs[index + 1] if index + 1 < len(runs) else None
        if (
            previous_run
            and next_run
            and previous_run["speaker"] == next_run["speaker"]
            and previous_run["speaker"] != run["speaker"]
        ):
            run["speaker"] = previous_run["speaker"]
            for word in run["words"]:
                word["speaker"] = run["speaker"]

    smoothed: list[dict] = []
    for run in runs:
        smoothed.extend(run["words"])
    return smoothed


def punct_join(tokens: list[str]) -> str:
    text = " ".join(tokens)
    text = re.sub(r"\s+([,.!?;:%])", r"\1", text)
    text = re.sub(r"\s+(['’])", r"\1", text)
    return text.strip()


def whisperx_words_to_json3(whisperx_json: Path, output_path: Path) -> Path:
    words = normalize_whisperx_words(whisperx_json)
    events = []
    current_speaker: str | None = None
    current_words: list[dict] = []
    last_event_speaker: str | None = None

    def flush() -> None:
        nonlocal current_speaker, current_words, last_event_speaker
        if not current_words:
            return
        start = current_words[0]["start"]
        end = max(word["end"] for word in current_words)
        text = punct_join([word["text"] for word in current_words])
        if current_speaker and current_speaker != last_event_speaker:
            text = f"[{current_speaker}] {text}"
        events.append({
            "tStartMs": int(start * 1000),
            "dDurationMs": max(1, int((end - start) * 1000)),
            "segs": [{"utf8": text}],
        })
        last_event_speaker = current_speaker
        current_words = []

    for word in words:
        starts_new_speaker = current_speaker is not None and word["speaker"] != current_speaker
        too_long = current_words and word["end"] - current_words[0]["start"] > 28
        sentence_end = current_words and re.search(r"[.!?][\"')\]]*$", current_words[-1]["text"])
        enough_words = len(current_words) >= 55
        if starts_new_speaker or (too_long and sentence_end) or enough_words:
            flush()
        current_speaker = word["speaker"]
        current_words.append(word)
    flush()

    output_path.write_text(json.dumps({
        "events": events,
        "whisperx": str(whisperx_json),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def caption_events(subtitle_json: Path) -> list[dict]:
    if subtitle_json.suffix.lower() == ".vtt":
        raw_events = extract_vtt_events(subtitle_json)
    else:
        raw_events = json.loads(subtitle_json.read_text(encoding="utf-8")).get("events", [])

    events: list[dict] = []
    for event in raw_events:
        text = html.unescape("".join(seg.get("utf8", "") for seg in event.get("segs") or []))
        text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
        if not text or text == "\u266a":
            continue
        start = float(event.get("tStartMs") or 0) / 1000.0
        duration = float(event.get("dDurationMs") or 0) / 1000.0
        events.append({
            "text": text,
            "start": start,
            "end": start + max(duration, 0.001),
        })
    return events


def dominant_speaker(words: list[dict], start: float, end: float) -> str:
    overlaps: dict[str, float] = {}
    for word in words:
        overlap = max(0.0, min(end, word["end"]) - max(start, word["start"]))
        if overlap > 0:
            overlaps[word["speaker"]] = overlaps.get(word["speaker"], 0.0) + overlap
    if not overlaps:
        return "SPEAKER_UNKNOWN"
    return max(overlaps.items(), key=lambda item: item[1])[0]


def caption_tokens_with_speakers(event: dict, words: list[dict]) -> list[tuple[str, str]]:
    tokens = [
        token
        for token in re.findall(r"\S+", event["text"])
        if token not in {">>", "<<", "\u266a"}
    ]
    if not tokens:
        return []

    start = event["start"]
    end = event["end"]
    local_words = [
        word
        for word in words
        if start - 1.25 <= (word["start"] + word["end"]) / 2 <= end + 1.25
        or max(0.0, min(end + 1.25, word["end"]) - max(start - 1.25, word["start"])) > 0
    ]
    if not local_words:
        speaker = dominant_speaker(words, start, end)
        return [(token, speaker) for token in tokens]

    def normalize_token(value: str) -> str:
        value = html.unescape(value)
        value = re.sub(r"\[[^\]]+\]", "", value)
        value = re.sub(r"[^A-Za-z0-9]+", "", value).lower()
        return value

    result: list[tuple[str, str]] = []
    cursor = 0
    last_speaker = dominant_speaker(words, start, end)
    for token in tokens:
        normalized = normalize_token(token)
        match_index: int | None = None
        if normalized:
            for index in range(cursor, min(len(local_words), cursor + 12)):
                if normalize_token(local_words[index]["text"]) == normalized:
                    match_index = index
                    break
            if match_index is None:
                for index in range(cursor, min(len(local_words), cursor + 12)):
                    word_norm = normalize_token(local_words[index]["text"])
                    if word_norm and (normalized.startswith(word_norm) or word_norm.startswith(normalized)):
                        match_index = index
                        break
        if match_index is not None:
            last_speaker = local_words[match_index]["speaker"]
            cursor = match_index + 1
        result.append((token, last_speaker))
    return smooth_tiny_token_runs(result)


def smooth_tiny_token_runs(token_speakers: list[tuple[str, str]]) -> list[tuple[str, str]]:
    if len(token_speakers) < 3:
        return token_speakers

    runs: list[dict] = []
    for token, speaker in token_speakers:
        if runs and runs[-1]["speaker"] == speaker:
            runs[-1]["tokens"].append(token)
        else:
            runs.append({"speaker": speaker, "tokens": [token]})

    for index, run in enumerate(runs):
        previous_run = runs[index - 1] if index > 0 else None
        next_run = runs[index + 1] if index + 1 < len(runs) else None
        if (
            previous_run
            and next_run
            and previous_run["speaker"] == next_run["speaker"]
            and len(run["tokens"]) <= 2
            and run["speaker"] != previous_run["speaker"]
        ):
            run["speaker"] = previous_run["speaker"]

    smoothed: list[tuple[str, str]] = []
    for run in runs:
        smoothed.extend((token, run["speaker"]) for token in run["tokens"])
    return smoothed


def hybrid_captions_with_whisperx(subtitle_json: Path, whisperx_json: Path, output_path: Path) -> Path:
    words = normalize_whisperx_words(whisperx_json)
    events: list[dict] = []
    last_event_speaker: str | None = None

    for event in caption_events(subtitle_json):
        token_speakers = caption_tokens_with_speakers(event, words)
        if not token_speakers:
            continue

        runs: list[dict] = []
        for token, speaker in token_speakers:
            if runs and runs[-1]["speaker"] == speaker:
                runs[-1]["tokens"].append(token)
            else:
                runs.append({"speaker": speaker, "tokens": [token]})

        total_tokens = sum(len(run["tokens"]) for run in runs)
        elapsed = 0
        for run in runs:
            run_token_count = len(run["tokens"])
            run_start = event["start"] + (event["end"] - event["start"]) * elapsed / max(1, total_tokens)
            elapsed += run_token_count
            run_end = event["start"] + (event["end"] - event["start"]) * elapsed / max(1, total_tokens)
            text = punct_join(run["tokens"])
            if run["speaker"] != last_event_speaker:
                text = f"[{run['speaker']}] {text}"
            events.append({
                "tStartMs": int(run_start * 1000),
                "dDurationMs": max(1, int((run_end - run_start) * 1000)),
                "segs": [{"utf8": text}],
            })
            last_event_speaker = run["speaker"]

    output_path.write_text(json.dumps({
        "events": events,
        "caption_source": str(subtitle_json),
        "whisperx": str(whisperx_json),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def run_whisperx_diarization(
    audio_path: Path,
    out_dir: Path,
    *,
    whisperx_python: Path,
    hf_token: str,
    model: str,
    device: str,
    compute_type: str,
    lang: str,
    min_speakers: int | None,
    max_speakers: int | None,
) -> Path:
    require_path(whisperx_python, "WhisperX Python interpreter")
    audio_path = normalize_audio_for_diarization(audio_path, out_dir)
    output_dir = out_dir / "whisperx"
    output_dir.mkdir(parents=True, exist_ok=True)
    whisperx_json = output_dir / f"{audio_path.stem}.json"
    if whisperx_json.exists() and whisperx_json.stat().st_size > 0:
        return whisperx_json

    command = [
        str(whisperx_python.parent / "whisperx"),
        str(audio_path),
        "--model",
        model,
        "--language",
        lang.split("-")[0],
        "--device",
        device,
        "--compute_type",
        compute_type,
        "--batch_size",
        "8",
        "--diarize",
        "--hf_token",
        hf_token,
        "--output_dir",
        str(output_dir),
        "--output_format",
        "json",
        "--print_progress",
        "True",
    ]
    if min_speakers is not None:
        command.extend(["--min_speakers", str(min_speakers)])
    if max_speakers is not None:
        command.extend(["--max_speakers", str(max_speakers)])
    run(command, env=env_with_hf_token(whisperx_python, hf_token))
    if not whisperx_json.exists():
        candidates = sorted(output_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            raise SystemExit("WhisperX did not produce a JSON transcript")
        whisperx_json = candidates[0]
    return whisperx_json


def transcribe_diarize_with_whisperx(
    audio_path: Path,
    out_dir: Path,
    *,
    whisperx_python: Path,
    hf_token: str,
    model: str,
    device: str,
    compute_type: str,
    lang: str,
    min_speakers: int | None,
    max_speakers: int | None,
) -> Path:
    whisperx_json = run_whisperx_diarization(
        audio_path,
        out_dir,
        whisperx_python=whisperx_python,
        hf_token=hf_token,
        model=model,
        device=device,
        compute_type=compute_type,
        lang=lang,
        min_speakers=min_speakers,
        max_speakers=max_speakers,
    )
    return whisperx_words_to_json3(whisperx_json, out_dir / f"whisperx.{lang}.diarized.json3")


def diarize_hybrid_with_whisperx(
    audio_path: Path,
    subtitle_json: Path,
    out_dir: Path,
    *,
    whisperx_python: Path,
    hf_token: str,
    model: str,
    device: str,
    compute_type: str,
    lang: str,
    min_speakers: int | None,
    max_speakers: int | None,
) -> Path:
    whisperx_json = run_whisperx_diarization(
        audio_path,
        out_dir,
        whisperx_python=whisperx_python,
        hf_token=hf_token,
        model=model,
        device=device,
        compute_type=compute_type,
        lang=lang,
        min_speakers=min_speakers,
        max_speakers=max_speakers,
    )
    return hybrid_captions_with_whisperx(
        subtitle_json,
        whisperx_json,
        out_dir / f"hybrid.{lang}.diarized.json3",
    )


def raw_caption_text(chunks: list[str]) -> str:
    return "\n".join(chunks).strip() + "\n"


def normalize_caption_text(chunks: list[str]) -> str:
    text = " ".join(chunks)
    text = apply_asr_fixes(text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([(\[{])\s+", r"\1", text)
    text = re.sub(r"\s+([)\]}])", r"\1", text)
    return text.strip()


def clean_caption_chunk(chunk: str) -> str:
    text = html.unescape(chunk).replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text or text == "\u266a" or FILLER_ONLY.fullmatch(text):
        return ""

    text = re.sub(r"(?:^|\s)>>\s*", " ", text)
    text = re.sub(r"\[\s*__\s*\]", "[expletive]", text)
    text = FILLER_INLINE.sub("", text)
    text = apply_asr_fixes(text)
    text = re.sub(r"\bi\b", "I", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_caption_text(chunks: list[str]) -> list[str]:
    cleaned: list[str] = []
    previous = None
    for chunk in chunks:
        text = clean_caption_chunk(chunk)
        if text and text != previous:
            cleaned.append(text)
        previous = text
    return cleaned


def terminal_punctuation(text: str) -> bool:
    return bool(re.search(r'[.!?][\'")\]]*$', text.strip()))


def first_word(text: str) -> str:
    match = re.match(r'\s*["\'(]*([A-Za-z][A-Za-z0-9\'-]*)', text)
    return match.group(1).lower() if match else ""


def last_word(text: str) -> str:
    matches = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", text)
    return matches[-1].lower() if matches else ""


def remove_last_word(text: str) -> str:
    return re.sub(r"\s+[A-Za-z][A-Za-z0-9'-]*\s*$", "", text.strip()).strip()


def remove_first_word(text: str) -> tuple[str, str]:
    match = re.match(r'(\s*["\'(]*)([A-Za-z][A-Za-z0-9\'-]*)([,;:]?)(\s*)(.*)$', text.strip())
    if not match:
        return "", text.strip()
    prefix, word, punctuation, _, rest = match.groups()
    if punctuation and punctuation != ",":
        return "", text.strip()
    return word, f"{prefix}{rest}".strip()


def speaker_turns_from_chunks(chunks: list[str]) -> list[dict]:
    turns: list[dict] = []
    current_speaker: str | None = None

    for chunk in chunks:
        match = SPEAKER_LABEL.match(chunk.strip())
        if match:
            current_speaker = match.group(1)
            text = match.group(2).strip()
            if text:
                turns.append({"speaker": current_speaker, "text": text})
        else:
            text = chunk.strip()
            if text:
                turns.append({"speaker": current_speaker, "text": text})
    return turns


def chunks_from_speaker_turns(turns: list[dict]) -> list[str]:
    chunks: list[str] = []
    for turn in turns:
        text = re.sub(r"\s+", " ", turn["text"]).strip()
        if not text:
            continue
        speaker = turn.get("speaker")
        chunks.append(f"[{speaker}] {text}" if speaker else text)
    return chunks


DANGLING_TAIL_WORDS = {
    "i",
    "this",
    "that",
    "it",
    "you",
    "we",
    "and",
    "but",
    "so",
}

CONTINUATION_STARTERS = {
    "also",
    "is",
    "are",
    "am",
    "was",
    "were",
    "could",
    "would",
    "should",
    "can",
    "can't",
    "cannot",
    "will",
    "won't",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "mean",
    "don't",
    "dont",
}

TINY_BRIDGE_WORDS = {
    "a",
    "an",
    "as",
    "is",
    "are",
    "the",
    "to",
    "of",
    "much",
    "many",
    "more",
    "less",
    "ai",
    "ais",
}


def repair_speaker_boundaries(chunks: list[str]) -> tuple[list[str], list[str]]:
    if not any(SPEAKER_LABEL.match(chunk.strip()) for chunk in chunks):
        return chunks, []

    turns = speaker_turns_from_chunks(chunks)
    audit: list[str] = []
    index = 0
    while index < len(turns):
        if index + 2 < len(turns):
            previous = turns[index]
            bridge = turns[index + 1]
            following = turns[index + 2]
            bridge_words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", bridge["text"])
            if (
                previous.get("speaker")
                and previous.get("speaker") == following.get("speaker")
                and bridge.get("speaker") != previous.get("speaker")
                and 0 < len(bridge_words) <= 3
                and all(word.lower() in TINY_BRIDGE_WORDS for word in bridge_words)
                and (not terminal_punctuation(previous["text"]) or first_word(following["text"]) not in {"i", "we", "they", "he", "she"})
            ):
                before = f"{previous['speaker']} | {previous['text']} / {bridge['speaker']} | {bridge['text']} / {following['speaker']} | {following['text']}"
                previous["text"] = f"{previous['text']} {bridge['text']} {following['text']}".strip()
                del turns[index + 1:index + 3]
                audit.append(f"folded tiny bridge turn into surrounding speaker: {before} -> {previous['speaker']} | {previous['text']}")
                continue

        if index + 1 < len(turns):
            current = turns[index]
            following = turns[index + 1]
            tail = last_word(current["text"])
            head = first_word(following["text"])
            if (
                current.get("speaker") != following.get("speaker")
                and tail in DANGLING_TAIL_WORDS
                and head in CONTINUATION_STARTERS
            ):
                before_current = current["text"]
                before_following = following["text"]
                current["text"] = remove_last_word(current["text"])
                following["text"] = f"{tail} {following['text']}".strip()
                audit.append(
                    f"moved dangling tail word '{tail}' to next speaker: "
                    f"{current.get('speaker')} | {before_current} / {following.get('speaker')} | {before_following}"
                )
                index += 1
                continue

            moved, remainder = remove_first_word(following["text"])
            if (
                current.get("speaker") != following.get("speaker")
                and moved.lower() in {"is", "are", "was", "were"}
                and not terminal_punctuation(current["text"])
                and first_word(remainder) in {"what", "why", "how", "whether", "if"}
            ):
                before_current = current["text"]
                before_following = following["text"]
                current["text"] = f"{current['text']} {moved.lower()},".strip()
                following["text"] = remainder
                audit.append(
                    f"moved leading auxiliary '{moved}' to previous speaker: "
                    f"{current.get('speaker')} | {before_current} / {following.get('speaker')} | {before_following}"
                )

        index += 1

    return chunks_from_speaker_turns(turns), audit


def write_repair_audit(path: Path, audit: list[str]) -> None:
    lines = [
        "# Speaker Boundary Repair Audit",
        "",
        "Deterministic post-diarization repair ran before Markdown/PDF rendering.",
        "The raw transcript remains unchanged.",
        "",
    ]
    if audit:
        lines.append("## Repairs")
        lines.extend(f"- {entry}" for entry in audit)
        lines.extend([
            "",
            "Consider an optional LLM cleanup pass if any repaired window still reads awkwardly or the speaker attribution is ambiguous.",
        ])
    else:
        lines.append("No boundary repairs were applied.")
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def fix_sentence_casing(sentence: str) -> str:
    sentence = sentence.strip()
    if not sentence:
        return sentence
    sentence = sentence[0].upper() + sentence[1:]
    sentence = re.sub(r"([.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), sentence)
    return sentence


def split_sentences(text: str) -> list[str]:
    if not text:
        return []

    sentence_end = re.compile(r".+?(?:[.!?][\"')\]]*)(?=\s+[A-Z0-9\"'(-]|\s*$)", re.S)
    sentences = []
    last_end = 0
    for match in sentence_end.finditer(text):
        sentences.append(re.sub(r"\s+", " ", match.group(0)).strip())
        last_end = match.end()
    remainder = text[last_end:].strip()
    if remainder:
        if sentences:
            sentences[-1] = f"{sentences[-1]} {remainder}".strip()
        else:
            sentences.append(remainder)
    return sentences


def plain_paragraphs(chunks: list[str], *, cleanup: bool = True) -> list[str]:
    result: list[str] = []
    current: list[str] = []
    words = 0

    for sentence in split_sentences(normalize_caption_text(chunks)):
        if cleanup:
            sentence = fix_sentence_casing(sentence)
        sentence_words = len(sentence.split())
        if current and words + sentence_words > 130:
            result.append(" ".join(current).strip())
            current = []
            words = 0

        current.append(sentence)
        words += sentence_words
        if words >= 95:
            result.append(" ".join(current).strip())
            current = []
            words = 0

    if current:
        result.append(" ".join(current).strip())

    return [
        re.sub(r"\s+", " ", re.sub(r"\s+([,.!?;:])", r"\1", p)).strip()
        for p in result
        if p.strip()
    ]


def paragraphs(chunks: list[str], *, cleanup: bool = True) -> list[str]:
    speaker_sections: list[tuple[str | None, list[str]]] = []
    current_speaker: str | None = None
    current_chunks: list[str] = []

    for chunk in chunks:
        match = SPEAKER_LABEL.match(chunk.strip())
        if match:
            speaker = match.group(1)
            text = match.group(2).strip()
            if current_chunks and speaker != current_speaker:
                speaker_sections.append((current_speaker, current_chunks))
                current_chunks = []
            current_speaker = speaker
            if text:
                current_chunks.append(text)
        else:
            text = chunk.strip()
            if text:
                current_chunks.append(text)

    if current_chunks:
        speaker_sections.append((current_speaker, current_chunks))

    if not any(speaker for speaker, _ in speaker_sections):
        return plain_paragraphs(chunks, cleanup=cleanup)

    result: list[str] = []
    for speaker, section_chunks in speaker_sections:
        section_paragraphs = plain_paragraphs(section_chunks, cleanup=cleanup)
        for paragraph_index, paragraph in enumerate(section_paragraphs):
            if speaker and paragraph_index == 0:
                result.append(f"[{speaker}] {paragraph}")
            else:
                result.append(paragraph)
    return result


def parse_speaker_labels(values: list[str]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"invalid --speaker-label value {value!r}; expected SPEAKER_00=Name")
        speaker, label = value.split("=", 1)
        speaker = speaker.strip()
        label = label.strip()
        if not speaker or not label:
            raise SystemExit(f"invalid --speaker-label value {value!r}; expected SPEAKER_00=Name")
        labels[speaker] = label
    return labels


def apply_speaker_labels(paragraph_list: list[str], labels: dict[str, str]) -> list[str]:
    if not labels:
        return paragraph_list
    rendered: list[str] = []
    for paragraph in paragraph_list:
        match = SPEAKER_LABEL.match(paragraph)
        if match and match.group(1) in labels:
            rendered.append(f"**{labels[match.group(1)]}:** {match.group(2).strip()}")
        else:
            rendered.append(paragraph)
    return rendered


def choose_heading(paragraph_group: list[str], used: set[str]) -> str:
    text = " ".join(paragraph_group).lower()
    scores: list[tuple[int, str]] = []
    for heading, keywords in TOPIC_HEADINGS:
        score = sum(text.count(keyword) for keyword in keywords)
        if heading in used:
            score -= 2
        scores.append((score, heading))
    score, heading = max(scores, key=lambda item: item[0])
    if score > 0:
        used.add(heading)
        return heading
    return "Continued Discussion"


def transcript_markdown(paragraph_list: list[str], *, headings: bool) -> str:
    if not headings:
        return "\n\n".join(paragraph_list).strip() + "\n"

    sections: list[str] = []
    used: set[str] = set()
    for index in range(0, len(paragraph_list), 6):
        group = paragraph_list[index : index + 6]
        heading = choose_heading(group, used)
        sections.append(f"## {heading}\n\n" + "\n\n".join(group))
    return "\n\n".join(sections).strip() + "\n"


def markdown_block(value: str) -> str:
    value = value.strip()
    return value if value else DEFAULT_DETAILED_SUMMARY


def transcript_word_sequence(paragraph_list: list[str]) -> list[str]:
    text = "\n\n".join(paragraph_list)
    text = re.sub(r"^\s*\*\*[^*\n]+:\*\*\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*\[(?:SPEAKER_[A-Z0-9_]+|SPEAKER_UNKNOWN)\]\s*", "", text, flags=re.M)
    text = apply_asr_fixes(text)
    return [
        token.lower()
        for token in re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?|[$][0-9]+|[0-9]+%", text)
    ]


def speaker_marker_sequence(paragraph_list: list[str]) -> list[str]:
    markers: list[str] = []
    for paragraph in paragraph_list:
        stripped = paragraph.strip()
        markdown = re.match(r"^\*\*([^*\n]+):\*\*\s*", stripped)
        bracket = re.match(r"^\[(SPEAKER_[A-Z0-9_]+|SPEAKER_UNKNOWN)\]\s*", stripped)
        if markdown:
            markers.append(markdown.group(1).strip())
        elif bracket:
            markers.append(bracket.group(1).strip())
    return markers


def token_delta_ratio(before: list[str], after: list[str]) -> tuple[float, int]:
    import difflib

    matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    changed = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        changed += max(i2 - i1, j2 - j1)
    denominator = max(len(before), 1)
    return changed / denominator, changed


def acceptable_llm_cleanup(
    before: list[str],
    after: list[str],
    *,
    max_delta_ratio: float = 0.005,
) -> tuple[bool, str]:
    before_markers = speaker_marker_sequence(before)
    after_markers = speaker_marker_sequence(after)
    if before_markers != after_markers:
        return False, "speaker labels changed or moved"

    before_tokens = transcript_word_sequence(before)
    after_tokens = transcript_word_sequence(after)
    ratio, changed = token_delta_ratio(before_tokens, after_tokens)
    if ratio > max_delta_ratio:
        return False, f"token delta too large: {changed} changed tokens ({ratio:.3%})"
    return True, f"accepted with {changed} changed normalized body tokens ({ratio:.3%})"


def write_llm_cleanup_audit(
    path: Path,
    *,
    applied: bool,
    reason: str,
    audit_lines: list[str] | None = None,
) -> None:
    lines = [
        "# LLM Transcript Cleanup Audit",
        "",
        f"Applied: {'yes' if applied else 'no'}",
        f"Reason: {reason}",
        "",
    ]
    if audit_lines:
        lines.append("## Notes")
        lines.extend(f"- {line}" for line in audit_lines if line.strip())
        lines.append("")
    lines.extend([
        "The deterministic pre-LLM transcript is preserved beside the final outputs.",
        "The cleanup pass is only accepted when speaker labels are unchanged and normalized body-token changes stay within the configured tolerance.",
    ])
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def codex_cleaned_paragraphs(
    info: dict,
    paragraph_list: list[str],
    *,
    codex_command: str,
    codex_home: Path | None,
    codex_model: str | None,
    timeout_seconds: int,
) -> tuple[list[str], list[str]] | None:
    codex_path = shutil.which(codex_command)
    if not codex_path:
        print(f"[cleanup] {codex_command!r} not found; using deterministic transcript", file=sys.stderr)
        return None

    title = info.get("title") or "Transcript"
    uploader = info.get("uploader") or "Unknown uploader"
    duration = info.get("duration_string") or ""
    transcript = "\n\n".join(paragraph_list)
    prompt = f"""You are cleaning a diarized transcript for a PDF.

Your job is paragraph cleanup only.

Hard requirements:
- Return exactly one JSON object and no surrounding prose.
- JSON keys: "paragraphs", "audit".
- "paragraphs" must be an array of Markdown paragraph strings.
- "audit" must be an array of short notes about paragraph-boundary changes.
- Do not paraphrase.
- Do not summarize.
- Do not omit, add, reorder, or rewrite words.
- Preserve every speaker label exactly as written, including Markdown bold labels like **Name:** and bracket labels like [SPEAKER_02].
- Preserve speaker order.
- You may only merge or split paragraphs at semantically sensible boundaries.
- You may fix capitalization, punctuation, and obvious ASR mistakes.
- Keep wording otherwise as close as possible to the input.
- If a sentence is split across paragraphs, merge it.
- If a paragraph contains multiple unrelated ideas, split it.

Validation note: your output will be rejected if speaker labels change or if more than a tiny share of normalized body tokens changes.

Metadata:
Title: {title}
Uploader: {uploader}
Duration: {duration}

Input paragraphs:
{json.dumps(paragraph_list, ensure_ascii=False, indent=2)}
"""
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as output_file:
        output_path = Path(output_file.name)
    cmd = [
        codex_path,
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--output-last-message",
        str(output_path),
    ]
    if codex_model:
        cmd.extend(["--model", codex_model])
    cmd.append("-")

    env = os.environ.copy()
    if codex_home:
        env["CODEX_HOME"] = str(codex_home)

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=timeout_seconds,
            env=env,
        )
        output = output_path.read_text().strip() if output_path.exists() else ""
        if not output:
            output = (result.stdout or "").strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        message = getattr(exc, "stderr", None) or getattr(exc, "stdout", None) or str(exc)
        print(f"[cleanup] Codex cleanup failed; using deterministic transcript: {process_error_excerpt(message)}", file=sys.stderr)
        return None
    finally:
        output_path.unlink(missing_ok=True)

    parsed = extract_json_object(output)
    if not parsed:
        print("[cleanup] Codex cleanup returned invalid JSON; using deterministic transcript", file=sys.stderr)
        return None
    paragraphs_value = parsed.get("paragraphs")
    audit_value = parsed.get("audit", [])
    if not isinstance(paragraphs_value, list) or not all(isinstance(item, str) for item in paragraphs_value):
        print("[cleanup] Codex cleanup omitted valid paragraphs; using deterministic transcript", file=sys.stderr)
        return None
    cleaned = [re.sub(r"\s+", " ", item).strip() for item in paragraphs_value if item.strip()]
    if not cleaned:
        print("[cleanup] Codex cleanup returned no paragraphs; using deterministic transcript", file=sys.stderr)
        return None
    accepted, reason = acceptable_llm_cleanup(paragraph_list, cleaned)
    if not accepted:
        print(f"[cleanup] Codex cleanup rejected: {reason}; using deterministic transcript", file=sys.stderr)
        return None
    audit = [str(item).strip() for item in audit_value] if isinstance(audit_value, list) else []
    audit.insert(0, reason)
    return cleaned, audit


def needs_generated_summary(value: str, default: str) -> bool:
    return not value.strip() or value.strip() == default


def sentence_tokens(sentence: str) -> list[str]:
    return [
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", sentence)
        if token.lower() not in SUMMARY_STOPWORDS
    ]


def sentence_score(sentence: str, frequencies: dict[str, int], index: int, total: int) -> float:
    tokens = sentence_tokens(sentence)
    if not tokens:
        return 0.0
    score = sum(frequencies.get(token, 0) for token in tokens) / (len(tokens) ** 0.65)
    if index < max(3, total // 10):
        score *= 1.15
    if any(term in sentence.lower() for term in ("important", "main", "key", "problem", "benefit", "risk", "future")):
        score *= 1.12
    return score


def clean_summary_sentence(sentence: str) -> str:
    sentence = re.sub(r"^\[(?:SPEAKER_[A-Z0-9_]+|SPEAKER_UNKNOWN)\]\s*", "", sentence.strip())
    sentence = re.sub(r"^\*\*[^*]+:\*\*\s*", "", sentence)
    return sentence.strip()


def select_summary_sentences(paragraph_list: list[str], count: int) -> list[str]:
    sentences = [
        clean_summary_sentence(sentence)
        for paragraph in paragraph_list
        for sentence in split_sentences(re.sub(r"\*\*([^*]+):\*\*", r"\1:", paragraph))
    ]
    sentences = [sentence for sentence in sentences if 45 <= len(sentence) <= 260 and len(sentence.split()) >= 8]
    if not sentences:
        return []

    frequencies: dict[str, int] = {}
    for sentence in sentences:
        for token in sentence_tokens(sentence):
            frequencies[token] = frequencies.get(token, 0) + 1

    ranked = sorted(
        enumerate(sentences),
        key=lambda item: sentence_score(item[1], frequencies, item[0], len(sentences)),
        reverse=True,
    )
    selected: list[tuple[int, str]] = []
    seen_roots: set[str] = set()
    for index, sentence in ranked:
        roots = set(sentence_tokens(sentence)[:12])
        if roots and len(roots & seen_roots) / max(len(roots), 1) > 0.55:
            continue
        selected.append((index, sentence))
        seen_roots.update(roots)
        if len(selected) >= count:
            break

    return [sentence for _, sentence in sorted(selected, key=lambda item: item[0])]


def generated_summaries(paragraph_list: list[str]) -> tuple[str, str]:
    brief_sentences = select_summary_sentences(paragraph_list, 2)
    detailed_sentences = select_summary_sentences(paragraph_list, 8)
    brief = " ".join(brief_sentences).strip() or DEFAULT_BRIEF_SUMMARY
    detailed = "\n".join(f"- {sentence}" for sentence in detailed_sentences).strip() or DEFAULT_DETAILED_SUMMARY
    return brief, detailed


def transcript_excerpt_for_summary(paragraph_list: list[str], limit: int = 70000) -> str:
    transcript = "\n\n".join(
        re.sub(r"^\*\*([^*]+):\*\*\s*", r"\1: ", paragraph.strip())
        for paragraph in paragraph_list
        if paragraph.strip()
    )
    if len(transcript) <= limit:
        return transcript
    first = transcript[:28000].rsplit("\n\n", 1)[0]
    midpoint = len(transcript) // 2
    middle_start = max(0, midpoint - 12000)
    middle_end = min(len(transcript), midpoint + 12000)
    middle = transcript[middle_start:middle_end].split("\n\n", 1)[-1].rsplit("\n\n", 1)[0]
    last = transcript[-28000:].split("\n\n", 1)[-1]
    return "\n\n[... transcript excerpted for summary: middle section follows ...]\n\n".join(
        [first, middle, last]
    )


def extract_json_object(text: str) -> dict | None:
    text = text.strip()
    candidates = [text]
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fenced:
        candidates.insert(0, fenced.group(1))
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        candidates.append(text[first : last + 1])
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def process_error_excerpt(message: object) -> str:
    if isinstance(message, bytes):
        text = message.decode("utf-8", errors="replace")
    else:
        text = str(message or "")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    useful = [
        line
        for line in lines
        if any(term in line.lower() for term in ("error", "unauthorized", "failed", "timeout", "timed out"))
    ]
    selected = useful[-6:] if useful else lines[-6:]
    return " | ".join(selected)[:1600] or "unknown error"


def codex_generated_summaries(
    info: dict,
    paragraph_list: list[str],
    *,
    codex_command: str,
    codex_home: Path | None,
    codex_model: str | None,
    timeout_seconds: int,
) -> tuple[str, str] | None:
    codex_path = shutil.which(codex_command)
    if not codex_path:
        print(f"[summary] {codex_command!r} not found; using extractive summaries", file=sys.stderr)
        return None

    title = info.get("title") or "Transcript"
    uploader = info.get("uploader") or "Unknown uploader"
    duration = info.get("duration_string") or ""
    transcript = transcript_excerpt_for_summary(paragraph_list)
    prompt = f"""You are preparing a PDF transcript package.

Write summaries of the cleaned transcript below.

Requirements:
- Return exactly one JSON object and no surrounding prose.
- JSON keys: "brief_summary", "detailed_summary".
- brief_summary: 2-4 sentences.
- detailed_summary: 7-10 Markdown bullets in one string, each bullet starting with "- ".
- Preserve the speaker's claims and emphasis. Do not add facts not supported by the transcript.
- Use clear prose for a technically literate reader.

Metadata:
Title: {title}
Uploader: {uploader}
Duration: {duration}

Cleaned transcript:
{transcript}
"""
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as output_file:
        output_path = Path(output_file.name)
    cmd = [
        codex_path,
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--output-last-message",
        str(output_path),
    ]
    if codex_model:
        cmd.extend(["--model", codex_model])
    cmd.append("-")

    env = os.environ.copy()
    if codex_home:
        env["CODEX_HOME"] = str(codex_home)

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=timeout_seconds,
            env=env,
        )
        output = output_path.read_text().strip() if output_path.exists() else ""
        if not output:
            output = (result.stdout or "").strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        message = getattr(exc, "stderr", None) or getattr(exc, "stdout", None) or str(exc)
        print(f"[summary] Codex summary failed; using extractive summaries: {process_error_excerpt(message)}", file=sys.stderr)
        return None
    finally:
        output_path.unlink(missing_ok=True)

    parsed = extract_json_object(output)
    if not parsed:
        print("[summary] Codex summary returned invalid JSON; using extractive summaries", file=sys.stderr)
        return None
    brief = str(parsed.get("brief_summary") or "").strip()
    detailed = str(parsed.get("detailed_summary") or "").strip()
    if not brief or not detailed:
        print("[summary] Codex summary omitted a required field; using extractive summaries", file=sys.stderr)
        return None
    return brief, detailed


def auto_summaries(
    info: dict,
    paragraph_list: list[str],
    *,
    provider: str,
    codex_command: str,
    codex_home: Path | None,
    codex_model: str | None,
    timeout_seconds: int,
) -> tuple[str, str]:
    if provider == "codex":
        summaries = codex_generated_summaries(
            info,
            paragraph_list,
            codex_command=codex_command,
            codex_home=codex_home,
            codex_model=codex_model,
            timeout_seconds=timeout_seconds,
        )
        if summaries:
            return summaries
    return generated_summaries(paragraph_list)


def yaml_quote(value: str) -> str:
    return value.replace('"', '\\"')


def find_chrome() -> str:
    for candidate in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(candidate)
        if path:
            return path
    raise SystemExit("Chrome/Chromium not found; install google-chrome or use --pdf-mode latex")


def copy_dario_assets(css: Path, out_dir: Path) -> Path:
    css_out = out_dir / css.name
    shutil.copy2(css, css_out)
    fonts_src = css.parent / "dario-fonts"
    if fonts_src.exists():
        fonts_out = out_dir / "dario-fonts"
        if fonts_out.exists():
            shutil.rmtree(fonts_out)
        shutil.copytree(fonts_src, fonts_out)
    return css_out


def write_outputs(
    info: dict,
    subtitle_json: Path,
    out_dir: Path,
    template: Path,
    theme: Path | None,
    css: Path,
    make_pdf: bool,
    pdf_mode: str,
    brief_summary: str,
    detailed_summary: str,
    summary_provider: str,
    summary_codex_command: str,
    summary_codex_home: Path | None,
    summary_codex_model: str | None,
    summary_timeout_seconds: int,
    verbatim: bool,
    speaker_labels: dict[str, str] | None = None,
    llm_cleanup: bool = True,
    llm_cleanup_timeout_seconds: int = DEFAULT_LLM_CLEANUP_TIMEOUT_SECONDS,
) -> dict[str, Path]:
    title = info.get("title") or "YouTube Transcript"
    uploader = info.get("uploader") or "Unknown uploader"
    url = info.get("webpage_url") or info.get("original_url") or ""
    duration = info.get("duration_string") or ""
    upload_date = info.get("upload_date") or ""
    if len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

    stem = f"{slugify(title, info.get('id') or 'youtube-transcript')}-transcript"
    md_path = out_dir / f"{stem}.md"
    html_path = out_dir / f"{stem}.html"
    txt_path = out_dir / f"{stem}.cleaned.txt"
    pre_llm_txt_path = out_dir / f"{stem}.pre-llm.cleaned.txt"
    raw_txt_path = out_dir / f"{stem}.raw.txt"
    pdf_path = out_dir / f"{stem}.pdf"
    repair_audit_path = out_dir / f"{stem}.repair-audit.md"
    llm_cleanup_audit_path = out_dir / f"{stem}.llm-cleanup-audit.md"
    if repair_audit_path.exists():
        repair_audit_path.unlink()
    if llm_cleanup_audit_path.exists():
        llm_cleanup_audit_path.unlink()

    raw_chunks = extract_caption_text(subtitle_json)
    raw_body = raw_caption_text(raw_chunks)
    raw_txt_path.write_text(raw_body)

    output_chunks = raw_chunks if verbatim else clean_caption_text(raw_chunks)
    repair_audit: list[str] = []
    if not verbatim:
        output_chunks, repair_audit = repair_speaker_boundaries(output_chunks)
    output_paragraphs = paragraphs(output_chunks, cleanup=not verbatim)
    output_paragraphs = apply_speaker_labels(output_paragraphs, speaker_labels or {})
    pre_llm_body = transcript_markdown(output_paragraphs, headings=not verbatim)
    pre_llm_txt_path.write_text(pre_llm_body)
    if llm_cleanup and not verbatim:
        cleaned_paragraphs = codex_cleaned_paragraphs(
            info,
            output_paragraphs,
            codex_command=summary_codex_command,
            codex_home=summary_codex_home,
            codex_model=summary_codex_model,
            timeout_seconds=llm_cleanup_timeout_seconds,
        )
        if cleaned_paragraphs:
            output_paragraphs, cleanup_audit = cleaned_paragraphs
            write_llm_cleanup_audit(
                llm_cleanup_audit_path,
                applied=True,
                reason="accepted Codex paragraph cleanup; speaker labels were unchanged and normalized token delta stayed within tolerance",
                audit_lines=cleanup_audit,
            )
        else:
            write_llm_cleanup_audit(
                llm_cleanup_audit_path,
                applied=False,
                reason="cleanup unavailable or rejected; deterministic transcript used",
            )
    elif not verbatim:
        write_llm_cleanup_audit(
            llm_cleanup_audit_path,
            applied=False,
            reason="LLM cleanup disabled by flag",
        )
    body = transcript_markdown(output_paragraphs, headings=not verbatim)
    txt_path.write_text(body)
    if repair_audit:
        write_repair_audit(repair_audit_path, repair_audit)
    if needs_generated_summary(brief_summary, DEFAULT_BRIEF_SUMMARY) or needs_generated_summary(
        detailed_summary,
        DEFAULT_DETAILED_SUMMARY,
    ):
        generated_brief, generated_detailed = auto_summaries(
            info,
            output_paragraphs,
            provider=summary_provider,
            codex_command=summary_codex_command,
            codex_home=summary_codex_home,
            codex_model=summary_codex_model,
            timeout_seconds=summary_timeout_seconds,
        )
        if needs_generated_summary(brief_summary, DEFAULT_BRIEF_SUMMARY):
            brief_summary = generated_brief
        if needs_generated_summary(detailed_summary, DEFAULT_DETAILED_SUMMARY):
            detailed_summary = generated_detailed
    brief_summary = brief_summary.strip() or DEFAULT_BRIEF_SUMMARY
    detailed_summary = markdown_block(detailed_summary)
    transcript_heading = "Verbatim Transcript" if verbatim else "Cleaned Transcript"
    yaml_title = yaml_quote(title)
    yaml_uploader = yaml_quote(uploader)
    md_path.write_text(
        f"""---
title: "{yaml_title}"
subtitle: "Summary and Transcript"
author: "{yaml_uploader}"
date: "{upload_date}"
lang: en-US
mainfont: "TeX Gyre Pagella"
sansfont: "Noto Sans"
monofont: "DejaVu Sans Mono"
geometry: "top=1.05in, bottom=1.1in, left=1.25in, right=1.25in"
fontsize: 11pt
colorlinks: true
urlcolor: DarioLink
linkcolor: DarioLink
toc: false
titlepage: false
header-left: " "
header-right: " "
footer-left: '\\mbox{{}}'
footer-right: '\\mbox{{}}'
---

Source: <{url}>  
Duration: {duration}

# Brief Summary

{brief_summary}

# Detailed Summary

{detailed_summary}

# {transcript_heading}

{body}"""
    )

    paths = {
        "md": md_path,
        "cleaned_txt": txt_path,
        "pre_llm_cleaned_txt": pre_llm_txt_path,
        "raw_txt": raw_txt_path,
    }
    if repair_audit_path.exists():
        paths["repair_audit"] = repair_audit_path
    if llm_cleanup_audit_path.exists():
        paths["llm_cleanup_audit"] = llm_cleanup_audit_path
    if make_pdf:
        if pdf_mode == "chrome":
            css_out = copy_dario_assets(css, out_dir)
            run([
                "pandoc",
                str(md_path),
                "--standalone",
                "--shift-heading-level-by=1",
                "--metadata",
                "pagetitle=" + title,
                "--css",
                css_out.name,
                "-o",
                str(html_path),
            ])
            run([
                find_chrome(),
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                html_path.resolve().as_uri(),
            ])
            paths["html"] = html_path
        else:
            cmd = [
                "pandoc",
                str(md_path),
                "-o",
                str(pdf_path),
                f"--template={template}",
                "--pdf-engine=xelatex",
            ]
            if theme:
                cmd.append(f"--include-in-header={theme}")
            run(cmd)
        paths["pdf"] = pdf_path
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a readable PDF transcript from a YouTube video.")
    parser.add_argument("url")
    parser.add_argument("--output-root", default="youtube-transcripts")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--theme", default=str(DEFAULT_THEME), help="Pandoc LaTeX header theme. Use 'none' to disable.")
    parser.add_argument("--css", default=str(DEFAULT_CSS), help="HTML/Chrome CSS theme used by the default Dario-light PDF mode.")
    parser.add_argument("--pdf-mode", choices=("chrome", "latex"), default="chrome", help="PDF renderer. Default: chrome.")
    parser.add_argument("--lang")
    parser.add_argument("--no-pdf", action="store_true")
    parser.add_argument("--verbatim", action="store_true", help="Use exact caption text without cleanup or editorial headings.")
    parser.add_argument("--brief-summary", default=DEFAULT_BRIEF_SUMMARY)
    parser.add_argument("--detailed-summary", default=DEFAULT_DETAILED_SUMMARY)
    parser.add_argument(
        "--summary-provider",
        choices=("codex", "extractive"),
        default=DEFAULT_SUMMARY_PROVIDER,
        help="How to auto-generate summaries when explicit summaries are not provided. Default: codex with extractive fallback.",
    )
    parser.add_argument("--summary-codex-command", default="codex", help="Codex CLI command used by --summary-provider codex.")
    parser.add_argument(
        "--summary-codex-home",
        default=str(DEFAULT_SUMMARY_CODEX_HOME),
        help="CODEX_HOME used for Codex summary subprocesses. Default: the current user's Codex home.",
    )
    parser.add_argument("--summary-codex-model", help="Optional Codex model override for summary generation.")
    parser.add_argument(
        "--summary-timeout-seconds",
        type=int,
        default=DEFAULT_SUMMARY_TIMEOUT_SECONDS,
        help="Timeout for LLM summary generation before falling back to extractive summaries.",
    )
    parser.add_argument(
        "--no-llm-cleanup",
        action="store_true",
        help="Disable the default LLM paragraph cleanup pass and use deterministic transcript cleanup only.",
    )
    parser.add_argument(
        "--llm-cleanup-timeout-seconds",
        type=int,
        default=DEFAULT_LLM_CLEANUP_TIMEOUT_SECONDS,
        help="Timeout for the default LLM paragraph cleanup pass before falling back to deterministic cleanup.",
    )
    parser.add_argument("--no-whisper", action="store_true", help="Fail instead of falling back to local Whisper when captions are unavailable.")
    parser.add_argument("--whisper-python", default=str(DEFAULT_WHISPER_PYTHON))
    parser.add_argument("--whisper-model", default="large-v3")
    parser.add_argument("--whisper-device", default="cuda")
    parser.add_argument("--whisper-compute-type", default="int8_float16")
    parser.add_argument("--whisperx-python", default=str(DEFAULT_WHISPERX_PYTHON))
    parser.add_argument("--whisperx-model", default="large-v3", help="WhisperX model for word-level diarization. Default: large-v3.")
    parser.add_argument("--whisperx-compute-type", default="int8", choices=("default", "float16", "float32", "int8"))
    parser.add_argument("--min-speakers", type=int, help="Minimum speaker count hint for pyannote/WhisperX diarization.")
    parser.add_argument("--max-speakers", type=int, help="Maximum speaker count hint for pyannote/WhisperX diarization.")
    parser.add_argument("--diarize", choices=("off", "pyannote", "whisperx", "hybrid"), default="off", help="Optionally add speaker labels. pyannote overlays captions; whisperx uses word-level audio alignment; hybrid overlays WhisperX speakers onto captions.")
    parser.add_argument("--hf-token-file", default=str(DEFAULT_HF_TOKEN_FILE), help="Env-style file containing HF_TOKEN for pyannote diarization.")
    parser.add_argument("--speaker-label", action="append", default=[], help="Render a diarized speaker as a human label, e.g. SPEAKER_00='Ross Douthat'. Repeat for multiple speakers.")
    args = parser.parse_args()

    require_tool("yt-dlp")
    require_tool("ffmpeg")
    if not args.no_pdf:
        require_tool("pandoc")
        if args.pdf_mode == "latex":
            require_tool("xelatex")
        else:
            find_chrome()

    template = Path(args.template).expanduser()
    if not args.no_pdf and args.pdf_mode == "latex" and not template.exists():
        raise SystemExit(f"Eisvogel template not found: {template}")
    theme = None if str(args.theme).lower() == "none" else Path(args.theme).expanduser()
    if not args.no_pdf and args.pdf_mode == "latex" and theme and not theme.exists():
        raise SystemExit(f"PDF theme not found: {theme}")
    css = Path(args.css).expanduser()
    if not args.no_pdf and args.pdf_mode == "chrome" and not css.exists():
        raise SystemExit(f"PDF CSS theme not found: {css}")

    info = json.loads(run(["yt-dlp", "--dump-single-json", "--skip-download", args.url], capture=True).stdout)
    video_id = info.get("id") or "youtube"
    out_dir = Path(args.output_root).expanduser() / video_id
    out_dir.mkdir(parents=True, exist_ok=True)

    lang = args.lang or "en"
    if args.diarize == "whisperx":
        hf_token = load_hf_token(Path(args.hf_token_file).expanduser())
        if not hf_token:
            raise SystemExit(
                "HF_TOKEN not found. Set HF_TOKEN or create "
                f"{Path(args.hf_token_file).expanduser()} with HF_TOKEN=..."
            )
        audio_path = download_audio(args.url, out_dir)
        subtitle_path = transcribe_diarize_with_whisperx(
            audio_path,
            out_dir,
            whisperx_python=Path(args.whisperx_python).expanduser(),
            hf_token=hf_token,
            model=args.whisperx_model,
            device=args.whisper_device,
            compute_type=args.whisperx_compute_type,
            lang=lang,
            min_speakers=args.min_speakers,
            max_speakers=args.max_speakers,
        )
        paths = write_outputs(
            info,
            subtitle_path,
            out_dir,
            template,
            theme,
            css,
            not args.no_pdf,
            args.pdf_mode,
            args.brief_summary,
            args.detailed_summary,
            args.summary_provider,
            args.summary_codex_command,
            Path(args.summary_codex_home).expanduser() if args.summary_codex_home else None,
            args.summary_codex_model,
            args.summary_timeout_seconds,
            args.verbatim,
            parse_speaker_labels(args.speaker_label),
            not args.no_llm_cleanup,
            args.llm_cleanup_timeout_seconds,
        )
        print(json.dumps({k: str(v.resolve()) for k, v in paths.items()}, indent=2))
        return 0

    subtitle_path: Path | None = None
    try:
        lang, is_manual = choose_lang(info, args.lang)
    except SystemExit:
        if args.no_whisper:
            raise
        is_manual = False

    output_template = str(out_dir / "%(title).120B [%(id)s].%(ext)s")
    subtitle_glob = [f"*.{lang}.json3", f"*.{lang}.vtt"]
    existing_subtitles = sorted(
        (
            p
            for pattern in subtitle_glob
            for p in out_dir.glob(pattern)
            if not p.name.startswith("whisper.")
        ),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    existing_info = sorted(out_dir.glob("*.info.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if subtitle_path is None and (not existing_subtitles or not existing_info):
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--sub-format",
            "json3/vtt/best",
            "--sub-langs",
            lang,
            "--write-info-json",
            "-o",
            output_template,
        ]
        cmd.append("--write-subs" if is_manual else "--write-auto-subs")
        cmd.append(args.url)
        try:
            run(cmd)
        except subprocess.CalledProcessError:
            if args.no_whisper:
                raise

    info_candidates = sorted(out_dir.glob("*.info.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    info_path = info_candidates[0] if info_candidates else None
    subtitle_candidates = sorted(
        (
            p
            for pattern in subtitle_glob
            for p in out_dir.glob(pattern)
            if not p.name.startswith("whisper.")
        ),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if subtitle_path is None and subtitle_candidates:
        subtitle_path = subtitle_candidates[0]
    if subtitle_path is None:
        whisper_candidates = sorted(
            out_dir.glob(f"whisper.{lang}.json3"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if whisper_candidates:
            subtitle_path = whisper_candidates[0]
    if subtitle_path is None:
        if args.no_whisper:
            raise SystemExit(f"downloaded subtitle JSON not found for language {lang}")
        audio_path = download_audio(args.url, out_dir)
        subtitle_path = transcribe_with_whisper(
            audio_path,
            out_dir,
            whisper_python=Path(args.whisper_python).expanduser(),
            model=args.whisper_model,
            device=args.whisper_device,
            compute_type=args.whisper_compute_type,
            lang=lang,
        )
        if args.diarize == "pyannote":
            hf_token = load_hf_token(Path(args.hf_token_file).expanduser())
            if not hf_token:
                raise SystemExit(
                    "HF_TOKEN not found. Set HF_TOKEN or create "
                    f"{Path(args.hf_token_file).expanduser()} with HF_TOKEN=..."
                )
            subtitle_path = diarize_with_pyannote(
                audio_path,
                subtitle_path,
                out_dir,
                whisper_python=Path(args.whisper_python).expanduser(),
                hf_token=hf_token,
                lang=lang,
            )
        elif args.diarize == "hybrid":
            hf_token = load_hf_token(Path(args.hf_token_file).expanduser())
            if not hf_token:
                raise SystemExit(
                    "HF_TOKEN not found. Set HF_TOKEN or create "
                    f"{Path(args.hf_token_file).expanduser()} with HF_TOKEN=..."
                )
            subtitle_path = diarize_hybrid_with_whisperx(
                audio_path,
                ensure_json3_subtitle(subtitle_path, out_dir, lang),
                out_dir,
                whisperx_python=Path(args.whisperx_python).expanduser(),
                hf_token=hf_token,
                model=args.whisperx_model,
                device=args.whisper_device,
                compute_type=args.whisperx_compute_type,
                lang=lang,
                min_speakers=args.min_speakers,
                max_speakers=args.max_speakers,
            )
    elif args.diarize == "pyannote":
        hf_token = load_hf_token(Path(args.hf_token_file).expanduser())
        if not hf_token:
            raise SystemExit(
                "HF_TOKEN not found. Set HF_TOKEN or create "
                f"{Path(args.hf_token_file).expanduser()} with HF_TOKEN=..."
            )
        audio_path = download_audio(args.url, out_dir)
        subtitle_path = diarize_with_pyannote(
            audio_path,
            ensure_json3_subtitle(subtitle_path, out_dir, lang),
            out_dir,
            whisper_python=Path(args.whisper_python).expanduser(),
            hf_token=hf_token,
            lang=lang,
        )
    elif args.diarize == "hybrid":
        hf_token = load_hf_token(Path(args.hf_token_file).expanduser())
        if not hf_token:
            raise SystemExit(
                "HF_TOKEN not found. Set HF_TOKEN or create "
                f"{Path(args.hf_token_file).expanduser()} with HF_TOKEN=..."
            )
        audio_path = download_audio(args.url, out_dir)
        subtitle_path = diarize_hybrid_with_whisperx(
            audio_path,
            ensure_json3_subtitle(subtitle_path, out_dir, lang),
            out_dir,
            whisperx_python=Path(args.whisperx_python).expanduser(),
            hf_token=hf_token,
            model=args.whisperx_model,
            device=args.whisper_device,
            compute_type=args.whisperx_compute_type,
            lang=lang,
            min_speakers=args.min_speakers,
            max_speakers=args.max_speakers,
        )

    downloaded_info = json.loads(info_path.read_text()) if info_path else info
    paths = write_outputs(
        downloaded_info,
        subtitle_path,
        out_dir,
        template,
        theme,
        css,
        not args.no_pdf,
        args.pdf_mode,
        args.brief_summary,
        args.detailed_summary,
        args.summary_provider,
        args.summary_codex_command,
        Path(args.summary_codex_home).expanduser() if args.summary_codex_home else None,
        args.summary_codex_model,
        args.summary_timeout_seconds,
        args.verbatim,
        parse_speaker_labels(args.speaker_label),
        not args.no_llm_cleanup,
        args.llm_cleanup_timeout_seconds,
    )

    print(json.dumps({k: str(v.resolve()) for k, v in paths.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
