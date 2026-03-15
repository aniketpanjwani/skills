from __future__ import annotations

from pathlib import Path

from pdf_extract import _annotate_markdown_with_table_artifacts, _table_artifact_block


def test_annotate_markdown_with_table_artifact_block(tmp_path: Path) -> None:
    md_path = tmp_path / "paper.docling.md"
    raw_table = "\n".join(
        [
            "| Variable | (1) |",
            "|---|---|",
            "| Robot exposure | -0.12 |",
        ]
    )
    md_path.write_text(f"Intro text.\n\n{raw_table}\n\nOutro text.\n", encoding="utf-8")

    tables_dir = tmp_path / "paper.tables"
    tables_dir.mkdir()
    artifact_block = _table_artifact_block(
        table_id="table_001",
        page=3,
        verification_required=True,
        verification_reasons=["contains many columns"],
        md_dir=tmp_path,
        agent_json_path=tables_dir / "table_001.agent.json",
        latex_path=tables_dir / "table_001.tex",
        crop_path=tables_dir / "table_001.crop.png",
        html_path=tables_dir / "table_001.html",
        otsl_path=tables_dir / "table_001.otsl.txt",
        raw_docling_json_path=tables_dir / "table_001.raw_docling.json",
    )

    _annotate_markdown_with_table_artifacts(
        md_path,
        [{"raw_markdown": raw_table, "artifact_block": artifact_block}],
    )

    annotated = md_path.read_text(encoding="utf-8")
    expected_fragment = (
        f"{raw_table}\n\n"
        "<!-- table-artifact:start table_001 -->\n"
        "```yaml\n"
        'table_id: "table_001"\n'
        "page: 3\n"
        "verification_required: true\n"
        "verification_reasons:\n"
        '  - "contains many columns"\n'
        'agent_table: "paper.tables/table_001.agent.json"\n'
    )
    assert expected_fragment in annotated
    assert "<!-- table-artifact:end table_001 -->" in annotated
