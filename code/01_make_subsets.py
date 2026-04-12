from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "raw"
WORKING_DIR = BASE_DIR / "working"
LOG_PATH = WORKING_DIR / "subset_extraction_log.txt"

# Try UTF-8 first, then common Korean encodings found in the raw files.
ENCODING_CANDIDATES = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]

REQUESTED_COLUMNS = {
    2019: [
        "Q33",
        "Q33A1",
        "Q33A2",
        "Q33A3",
        "Q32",
        "Q50",
        "Q58A1",
        "Q58A2",
        "D_SIZE",
        "D_IND",
        "D_INDSIZE",
        "WT",
    ],
    2020: [
        "Q41",
        "Q41A1",
        "Q41A2",
        "Q41A3",
        "Q40",
        "Q33",
        "Q42A1",
        "Q42A3",
        "Q42A5",
        "D_IND",
        "D_INDSIZE1",
        "WT",
        "D_SIZE",
    ],
    2021: [
        "Q44",
        "Q44A1",
        "Q44A2",
        "Q44A3",
        "Q43",
        "REQ43",
        "Q36",
        "Q45A1",
        "Q45A3",
        "Q45A5",
        "D_SIZE",
        "D_IND",
        "D_INDSIZE",
        "RIM_WT",
    ],
    2022: [
        "Q44",
        "Q44A1",
        "Q44A2",
        "Q44A3",
        "Q43",
        "REQ43",
        "Q36",
        "Q45A1",
        "Q45A3",
        "Q45A5",
        "D_SIZE",
        "D_IND",
        "D_INDSIZE",
        "RIM_WT",
    ],
    2023: [
        "Q34",
        "Q34_1_1",
        "Q34_1_2",
        "Q34_1_3",
        "Q33",
        "REQ33",
        "Q28",
        "Q35_1",
        "Q35_3",
        "Q35_5",
        "D_SIZE",
        "D_IND",
        "D_INDSIZE",
        "RIM_WT",
    ],
    2024: [
        "Q34",
        "Q34_1_1",
        "Q34_1_2",
        "Q34_1_3",
        "Q33",
        "REQ33",
        "Q28",
        "Q35_1",
        "Q35_3",
        "Q35_5",
        "D_SIZE",
        "D_IND",
        "D_INDSIZE",
        "RIM_WT",
    ],
}


def detect_encoding(csv_path: Path) -> str:
    """Return the first encoding that can read the file header."""
    for encoding in ENCODING_CANDIDATES:
        try:
            pd.read_csv(csv_path, encoding=encoding, nrows=0)
            return encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"Could not decode {csv_path} with: {', '.join(ENCODING_CANDIDATES)}",
    )


def format_columns(columns: Iterable[str]) -> str:
    values = list(columns)
    return ", ".join(values) if values else "(none)"


def extract_one_year(year: int) -> dict[str, object]:
    source_path = RAW_DIR / f"nia_{year}_raw.csv"
    output_path = WORKING_DIR / f"nia_{year}_subset.csv"
    requested_columns = REQUESTED_COLUMNS[year]

    encoding = detect_encoding(source_path)
    header = pd.read_csv(source_path, encoding=encoding, nrows=0).columns.tolist()

    extracted_columns = [column for column in requested_columns if column in header]
    missing_columns = [column for column in requested_columns if column not in header]

    if extracted_columns:
        subset = pd.read_csv(
            source_path,
            encoding=encoding,
            usecols=extracted_columns,
            dtype=str,
            keep_default_na=False,
            na_filter=False,
        )
    else:
        subset = pd.read_csv(
            source_path,
            encoding=encoding,
            dtype=str,
            keep_default_na=False,
            na_filter=False,
        ).iloc[:, 0:0]

    subset = subset.reindex(columns=extracted_columns)
    subset["year"] = year
    subset.to_csv(output_path, index=False, encoding="utf-8-sig")

    return {
        "year": year,
        "source_path": source_path,
        "output_path": output_path,
        "encoding": encoding,
        "requested_columns": requested_columns,
        "extracted_columns": extracted_columns,
        "missing_columns": missing_columns,
        "row_count": len(subset),
        "column_count": len(subset.columns),
    }


def write_log(results: list[dict[str, object]]) -> None:
    lines: list[str] = []
    lines.append("NIA subset extraction log")
    lines.append("=" * 80)

    for result in results:
        lines.append(f"Year: {result['year']}")
        lines.append(f"Source file path: {result['source_path']}")
        lines.append(f"Output file path: {result['output_path']}")
        lines.append(f"Encoding used: {result['encoding']}")
        lines.append(
            f"Requested columns: {format_columns(result['requested_columns'])}"
        )
        lines.append(
            f"Extracted columns found: {format_columns(result['extracted_columns'])}"
        )
        lines.append(
            f"Missing columns: {format_columns(result['missing_columns'])}"
        )
        lines.append(f"Output row count: {result['row_count']}")
        lines.append(f"Output column count: {result['column_count']}")
        lines.append("-" * 80)

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    WORKING_DIR.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []

    for year in sorted(REQUESTED_COLUMNS):
        result = extract_one_year(year)
        results.append(result)

        print(
            f"[{year}] rows={result['row_count']}, cols={result['column_count']}, "
            f"encoding={result['encoding']}, "
            f"found={len(result['extracted_columns'])}, "
            f"missing={len(result['missing_columns'])}"
        )
        if result["missing_columns"]:
            print(f"  missing columns: {format_columns(result['missing_columns'])}")

    write_log(results)
    print(f"Extraction log saved to: {LOG_PATH}")


if __name__ == "__main__":
    main()
