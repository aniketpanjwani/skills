from __future__ import annotations

import json
from pathlib import Path

from table_agent import build_agent_table, cell_text_to_latex
from table_cleanup import TableCleanupReport


class FakeBBox:
    def __init__(self, l: float, t: float, r: float, b: float, coord_origin: str = "TOPLEFT") -> None:
        self.l = l
        self.t = t
        self.r = r
        self.b = b
        self.coord_origin = coord_origin

    def model_dump(self, mode: str | None = None) -> dict[str, object]:
        return {
            "l": self.l,
            "t": self.t,
            "r": self.r,
            "b": self.b,
            "coord_origin": self.coord_origin,
        }


class FakeProv:
    def __init__(self, page_no: int, bbox: FakeBBox) -> None:
        self.page_no = page_no
        self.bbox = bbox


class FakeCell:
    def __init__(
        self,
        text: str,
        row_start: int,
        row_end: int,
        col_start: int,
        col_end: int,
        *,
        column_header: bool = False,
        row_header: bool = False,
        row_section: bool = False,
    ) -> None:
        self.text = text
        self.start_row_offset_idx = row_start
        self.end_row_offset_idx = row_end
        self.start_col_offset_idx = col_start
        self.end_col_offset_idx = col_end
        self.column_header = column_header
        self.row_header = row_header
        self.row_section = row_section
        self.bbox = FakeBBox(10 + (col_start * 20), 10 + (row_start * 8), 20 + (col_end * 20), 18 + (row_end * 8))


class FakeData:
    def __init__(self, table_cells: list[FakeCell]) -> None:
        self.table_cells = table_cells


class FakeTable:
    def __init__(self) -> None:
        self.data = FakeData(
            [
                FakeCell("", 0, 1, 0, 1, column_header=True),
                FakeCell("Models", 0, 1, 1, 3, column_header=True),
                FakeCell("Variable", 1, 2, 0, 1, column_header=True),
                FakeCell("(1)", 1, 2, 1, 2, column_header=True),
                FakeCell("(2)", 1, 2, 2, 3, column_header=True),
                FakeCell("Robots", 2, 3, 0, 1),
                FakeCell("-0.123***", 2, 3, 1, 2),
                FakeCell("-0.456", 2, 3, 2, 3),
                FakeCell("", 3, 4, 0, 1),
                FakeCell("(0.045)", 3, 4, 1, 2),
                FakeCell("(0.078)", 3, 4, 2, 3),
                FakeCell("Controls", 4, 5, 0, 1),
                FakeCell("Yes", 4, 5, 1, 2),
                FakeCell("No", 4, 5, 2, 3),
                FakeCell("Observations", 5, 6, 0, 1),
                FakeCell("1000", 5, 6, 1, 2),
                FakeCell("900", 5, 6, 2, 3),
            ]
        )
        self.prov = [FakeProv(1, FakeBBox(0, 0, 120, 48, "TOPLEFT"))]
        self.footnotes = [{"text": "Robust standard errors in parentheses."}]

    def caption_text(self, doc: object) -> str:
        return "Table 1: Example Regression"


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def test_cell_text_to_latex_synthesizes_significance_markers() -> None:
    latex, source, confidence = cell_text_to_latex("-0.123***")
    assert latex == "$-0.123^{***}$"
    assert source == "deterministic"
    assert confidence > 0.9


def test_build_agent_table_matches_regression_fixture() -> None:
    table = FakeTable()
    report = TableCleanupReport(verification_required=False, reasons=[])
    agent_table, full_latex = build_agent_table(
        table=table,
        doc=object(),
        pdf_path=Path("/tmp/example.pdf"),
        table_index=1,
        raw_markdown="",
        cleaned_markdown="| Variable | (1) | (2) |",
        cleaned_report=report,
        html=None,
        otsl=None,
        crop_path=None,
        table_image=None,
        plumber_pdf=None,
    )

    expected_semantics = json.loads((FIXTURE_DIR / "example_regression_semantics.json").read_text(encoding="utf-8"))
    expected_full_latex = (FIXTURE_DIR / "example_table.tex").read_text(encoding="utf-8")
    expected_tabular = (FIXTURE_DIR / "example_tabular.tex").read_text(encoding="utf-8")

    assert agent_table["title"] == "Table 1: Example Regression"
    assert agent_table["regression_semantics"] == expected_semantics
    assert agent_table["renderings"]["latex_tabular"] == expected_tabular
    assert full_latex == expected_full_latex

    cells_by_id = {cell["cell_id"]: cell for cell in agent_table["cells"]}
    assert cells_by_id["r2_c1"]["latex"] == "$-0.123^{***}$"
    assert cells_by_id["r4_c1"]["text_normalized"] == "Yes"
