---
name: youtube-transcript-pdf
description: "Create readable PDF transcripts from YouTube videos using yt-dlp, Pandoc, Chrome, and optional local Whisper diarization."
---

# YouTube Transcript PDF

Use when asked to download a YouTube transcript/captions and return a readable PDF. Also use this for audio-only pages or videos without usable subtitles; the helper falls back to local `faster-whisper`.

## Workflow

1. Run the helper script with the YouTube URL.
2. It selects the best English caption track, preferring human subtitles over auto-captions.
3. If no usable captions are available, it downloads best audio or a low-resolution video fallback with `yt-dlp` and transcribes locally with `faster-whisper`.
4. It writes the raw subtitle/Whisper JSON, raw audit `.txt`, deterministic pre-LLM cleaned `.txt`, final cleaned `.txt`, cleaned `.md`, audit files, and final `.pdf` under `youtube-transcripts/<video_id>/`.
5. The PDF defaults to a Dario Amodei blog light-mode theme rendered through Chrome: Newsreader fonts, `#f0eee6` page background, narrow measure, simple headings, minimal chrome, and dark links.
6. After cleaning the transcript and before rendering Markdown/PDF, the helper generates summaries when `--brief-summary` and `--detailed-summary` are not provided. Default is LLM-written summaries via `codex exec` using the user's Codex home for auth; if Codex is unavailable, unauthenticated, times out, or returns invalid JSON, the helper falls back to extractive summaries. The default Markdown/PDF sections are always ordered as Brief Summary, Detailed Summary, Cleaned Transcript.
7. The cleaned transcript improves readability without paraphrasing: remove filler-only ums/uhs/ahs and duplicate stutters, fix obvious ASR misspellings, punctuation, and casing, preserve meaning and order, and add editorial section headings around topic shifts.
8. For diarized transcripts, the helper runs a deterministic speaker-boundary repair pass before rendering. It fixes obvious tiny boundary artifacts such as `This`/`Is...`, `You`/`Could...`, and one-word bridge turns like `much` when they split one sentence across speakers. If repairs are applied, it writes a `.repair-audit.md` file beside the outputs.
9. By default, the helper then runs a strict LLM paragraph cleanup pass via `codex exec` after known speaker labels have been applied. The LLM may merge/split paragraphs and fix capitalization, punctuation, and obvious ASR mistakes, but must not paraphrase, add, delete, reorder, or change speaker order. The helper rejects the LLM output if speaker labels change or if the normalized body-token delta is too large, writes a `.llm-cleanup-audit.md`, and falls back to the deterministic transcript if cleanup fails.
10. Keep the raw/verbatim transcript text file and `.pre-llm.cleaned.txt` beside the final cleaned output for auditability and manual repair.
11. Attach the generated PDF when the request came from chat and the user asks for an attachment.

## Local Whisper

Local Whisper is optional and is only used when captions are missing or diarization is requested. The default interpreter path is:

```bash
~/.local/share/youtube-transcript-pdf/whisper-venv/bin/python
```

Create that environment yourself, or pass `--whisper-python /path/to/python`. The default fallback is `faster-whisper` with `large-v3`, `cuda`, and `int8_float16`. Use `--whisper-model large-v3-turbo` when speed matters more than maximum accuracy. Use `--whisper-model medium`, `--whisper-device cpu`, or a different `--whisper-compute-type` on smaller machines.

## Optional Diarization

The helper has three experimental diarization paths for multi-speaker videos. For interviews with usable YouTube captions, prefer `hybrid`.

Use `pyannote` when the source captions are high quality and you mainly need coarse speaker labels. It works with downloaded captions when available, and with local Whisper fallback transcripts otherwise:

```bash
python3 scripts/youtube_transcript_pdf.py \
  "https://youtu.be/..." \
  --diarize pyannote
```

Use `hybrid` for the normal interview workflow. It keeps YouTube captions as the canonical transcript text, then uses WhisperX word-level diarization to split/label speaker turns:

```bash
python3 scripts/youtube_transcript_pdf.py \
  "https://youtu.be/..." \
  --diarize hybrid \
  --min-speakers 2 \
  --max-speakers 2
```

Use `whisperx` when speaker boundaries matter but captions are bad or missing. This ignores downloaded captions and runs WhisperX word-level transcription, alignment, and diarization:

```bash
python3 scripts/youtube_transcript_pdf.py \
  "https://youtu.be/..." \
  --diarize whisperx \
  --min-speakers 2 \
  --max-speakers 2
```

It reads `HF_TOKEN` from the environment first, then from:

```bash
~/.config/youtube-transcript-pdf/huggingface.env
```

That should contain a Hugging Face read token, and the account must have accepted the gated terms for:

- `pyannote/speaker-diarization-3.1`
- `pyannote/segmentation-3.0`
- `pyannote/speaker-diarization-community-1`

The Whisper venv includes `torch`, `torchaudio`, `torchcodec`, `nvidia-npp-cu12`, and `pyannote.audio`. The helper builds an `LD_LIBRARY_PATH` from the venv's pip-installed `nvidia/*/lib` directories before launching Whisper or pyannote subprocesses, so TorchCodec can find CUDA/NPP libraries.

When `--diarize pyannote` is enabled, the helper downloads audio even if captions already exist, runs pyannote speaker diarization on that audio, then prefixes transcript chunks when the active speaker changes, e.g. `[SPEAKER_00] ...`.

WhisperX is optional and is installed separately from the faster-whisper environment. The default interpreter path is:

```bash
~/.local/share/youtube-transcript-pdf/whisperx-venv/bin/python
```

When `--diarize hybrid` is enabled, the helper downloads audio, normalizes it to 16 kHz mono WAV, runs the WhisperX CLI with pyannote diarization, aligns caption tokens against the WhisperX word stream, smooths tiny speaker flips, repairs obvious sentence-boundary artifacts, and emits diarized caption text. This usually gives the best interview PDF: better wording from YouTube captions, better speaker boundaries from WhisperX. It still needs spot checks around very short interruptions and bad caption text.

When `--diarize whisperx` is enabled, the helper downloads audio, normalizes it to 16 kHz mono WAV, runs the WhisperX CLI with pyannote diarization, converts word-level speaker assignments into YouTube `json3`-style chunks, and smooths tiny speaker flips between longer same-speaker runs. It improves boundary placement compared with caption-level pyannote, but the transcript text comes from WhisperX instead of YouTube captions, so names and technical terms may need spot checks.

When the speaker identities are known, render human names with repeated `--speaker-label` flags:

```bash
--speaker-label "SPEAKER_00=Host Name" --speaker-label "SPEAKER_01=Guest Name"
```

## PDF Theme

The default theme is:

```bash
themes/dario-light.css
```

It is intended to approximate the light-mode feel of Dario Amodei's long-form blog: cream page background to the sheet edges, Newsreader serif text, a 640px body column, 18.5px body text with 30px line height, 1in top/bottom print margins, compact headings, and no title page or report chrome. Keep it plain and text-forward; avoid colored boxes, heavy borders, or academic-report styling unless the user explicitly asks for that.

The older LaTeX/Eisvogel route remains available with `--pdf-mode latex`; its header theme is:

```bash
themes/dario-blog.tex
```

## Completion Gate

This skill is not complete when the transcript has merely been fetched, cleaned, summarized, or saved as Markdown.

The required deliverable is a rendered PDF transcript unless the user explicitly asks for a different format or passes `--no-pdf`.

Before reporting completion:

- Confirm the cleaned Markdown file exists.
- Confirm the Markdown/PDF do not contain the placeholder text `Brief summary not provided.` or `Detailed summary not provided.` unless the source transcript is empty or the user explicitly passed those strings.
- For diarized transcripts, check whether `.repair-audit.md` and `.llm-cleanup-audit.md` files exist. Mention them when relevant; the LLM cleanup pass is already default unless `--no-llm-cleanup` was used.
- Render the PDF with the default Pandoc-to-HTML plus Chrome Dario-light path, unless the user explicitly chooses `--pdf-mode latex`.
- Confirm the PDF exists, has nonzero size, and `pdfinfo` can read its page count.
- If the request came from chat and the user expects the deliverable there, upload or attach the PDF to the thread/channel.
- Report the PDF path first and the Markdown path second.

Never say "done" for this skill if only the raw transcript, cleaned text, Markdown, or summary exists.

## Command

```bash
python3 scripts/youtube_transcript_pdf.py "https://youtu.be/..."
```

Useful flags:

- `--output-root PATH` changes the output directory. Default: `youtube-transcripts`.
- `--pdf-mode chrome|latex` sets the renderer. Default: `chrome`, which uses the Dario-light HTML/CSS theme.
- `--css PATH` sets the HTML/Chrome CSS theme. Default: `themes/dario-light.css` in this skill.
- `--template PATH` sets the Eisvogel template for `--pdf-mode latex`. Default: `~/.local/share/pandoc/templates/eisvogel.latex`.
- `--theme PATH` sets the Pandoc LaTeX header theme for `--pdf-mode latex`. Default: `themes/dario-blog.tex` in this skill. Use `--theme none` to disable.
- `--lang LANG` forces a caption language instead of auto-selecting.
- `--no-pdf` only produces cleaned text/Markdown.
- `--verbatim` disables cleanup and editorial headings when exact captions are wanted.
- `--brief-summary TEXT` sets the 2-4 sentence brief summary.
- `--detailed-summary TEXT` sets the detailed summary block, including Markdown bullets.
- `--summary-provider codex|extractive` controls automatic summaries. Default: `codex`, with extractive fallback.
- `--summary-codex-command COMMAND` changes the Codex CLI command used for LLM summaries. Default: `codex`.
- `--summary-codex-home PATH` sets `CODEX_HOME` for Codex summary subprocesses. Default: the current user's Codex home.
- `--summary-codex-model MODEL` optionally sets a Codex model for summary generation.
- `--summary-timeout-seconds N` sets the LLM summary timeout before falling back. Default: `240`.
- `--no-llm-cleanup` disables the default strict LLM paragraph cleanup pass.
- `--llm-cleanup-timeout-seconds N` sets the LLM paragraph cleanup timeout before falling back to deterministic cleanup. Default: `360`.
- `--no-whisper` disables the fallback and fails when captions are missing.
- `--whisper-model MODEL` sets the fallback model. Default: `large-v3`.
- `--whisper-device DEVICE` sets the fallback device. Default: `cuda`.
- `--whisper-compute-type TYPE` sets the fallback compute type. Default: `int8_float16`.
- `--whisper-python PATH` changes the Whisper venv interpreter. Default: `~/.local/share/youtube-transcript-pdf/whisper-venv/bin/python`.
- `--diarize off|pyannote|hybrid|whisperx` optionally adds speaker labels for multi-speaker videos. `pyannote` overlays captions coarsely; `hybrid` overlays WhisperX speakers onto captions; `whisperx` uses WhisperX text and word-level speaker alignment. Default: `off`.
- `--whisperx-python PATH` changes the WhisperX venv interpreter. Default: `~/.local/share/youtube-transcript-pdf/whisperx-venv/bin/python`.
- `--whisperx-model MODEL` sets the WhisperX model. Default: `large-v3`.
- `--whisperx-compute-type TYPE` sets the WhisperX compute type. Default: `int8`.
- `--min-speakers N` and `--max-speakers N` provide diarization speaker-count hints.
- `--hf-token-file PATH` changes the env-style Hugging Face token file for diarization. Default: `~/.config/youtube-transcript-pdf/huggingface.env`.
- `--speaker-label SPEAKER_00=Name` renders a diarized speaker ID with a human name in the transcript/PDF. Repeat for multiple speakers.

## Verification

After a PDF run, check `pdfinfo` and sample text:

```bash
pdfinfo output.pdf | sed -n '1,20p'
pdftotext output.pdf - | sed -n '1,30p'
```
