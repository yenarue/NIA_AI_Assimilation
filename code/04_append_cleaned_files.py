from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CLEANED_DIR = BASE_DIR / "working" / "cleaned"
MERGED_DIR = BASE_DIR / "merged"
LOG_PATH = MERGED_DIR / "append_log.txt"

STANDARDIZED_COLUMNS = [
    "year",
    "weight",
    "industry",
    "industry_size",
    "firm_size",
    "it_org_any",
    "it_org_internal",
    "it_org_mixed",
    "it_org_outsource",
    "it_org_type",
    "it_invest_share",
    "it_invest_share_cat",
    "ai_use",
    "proc_improve",
    "innov_outcome",
    "decision_improve",
]

OUTPUT_COLUMNS = [
    "year",
    "source_file",
    "weight",
    "industry",
    "industry_size",
    "firm_size",
    "it_org_any",
    "it_org_internal",
    "it_org_mixed",
    "it_org_outsource",
    "it_org_type",
    "it_invest_share",
    "it_invest_share_cat",
    "ai_use",
    "proc_improve",
    "innov_outcome",
    "decision_improve",
]

MAIN_YEARS = [2020, 2021, 2022, 2023, 2024]
EXTENDED_YEARS = [2019, 2020, 2021, 2022, 2023, 2024]


def cleaned_path(year: int) -> Path:
    return CLEANED_DIR / f"nia_{year}_cleaned.csv"


def load_one_year(year: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    path = cleaned_path(year)
    df = pd.read_csv(path, encoding="utf-8-sig", dtype=str, keep_default_na=False, na_filter=False)

    missing_added: list[str] = []
    type_harmonization: list[str] = []

    for column in STANDARDIZED_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA
            missing_added.append(column)

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
        type_harmonization.append("year -> Int64")
    else:
        df["year"] = year
        type_harmonization.append("year missing -> filled from file year and cast to Int64")

    df["source_file"] = path.name
    type_harmonization.append("source_file -> string")

    # Keep only standardized columns plus source_file in a fixed order.
    df = df[OUTPUT_COLUMNS].copy()

    return df, {
        "year": year,
        "path": path,
        "row_count": len(df),
        "missing_added": missing_added,
        "type_harmonization": type_harmonization,
    }


def append_years(years: list[int], output_path: Path) -> dict[str, Any]:
    frames: list[pd.DataFrame] = []
    year_logs: list[dict[str, Any]] = []

    for year in years:
        df, info = load_one_year(year)
        frames.append(df)
        year_logs.append(info)

    merged = pd.concat(frames, axis=0, ignore_index=True)
    merged.to_csv(output_path, index=False, encoding="utf-8-sig")

    expected_rows = sum(item["row_count"] for item in year_logs)
    actual_rows = len(merged)
    year_distribution = merged["year"].value_counts(dropna=False).sort_index().to_dict()
    duplicate_columns = merged.columns[merged.columns.duplicated()].tolist()
    missing_standardized = [col for col in OUTPUT_COLUMNS if col not in merged.columns]

    return {
        "output_path": output_path,
        "years": years,
        "year_logs": year_logs,
        "expected_rows": expected_rows,
        "actual_rows": actual_rows,
        "year_distribution": year_distribution,
        "duplicate_columns": duplicate_columns,
        "missing_standardized": missing_standardized,
    }


def write_log(main_info: dict[str, Any], extended_info: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append("NIA cleaned 파일 append 로그")
    lines.append("=" * 96)

    for title, info in [
        ("Main merged dataset", main_info),
        ("Extended/reference dataset", extended_info),
    ]:
        lines.append(title)
        lines.append(f"output file: {info['output_path']}")
        lines.append(f"years included: {', '.join(str(y) for y in info['years'])}")
        lines.append("input files used:")
        for item in info["year_logs"]:
            lines.append(f"  - {item['path']} (rows={item['row_count']})")
        lines.append(f"total row count expected: {info['expected_rows']}")
        lines.append(f"total row count actual: {info['actual_rows']}")
        lines.append(f"row count validation passed: {info['expected_rows'] == info['actual_rows']}")
        lines.append(f"year distribution: {info['year_distribution']}")
        lines.append(
            "missing standardized columns added artificially:"
        )
        any_missing = False
        for item in info["year_logs"]:
            if item["missing_added"]:
                any_missing = True
                lines.append(f"  - {item['year']}: {', '.join(item['missing_added'])}")
        if not any_missing:
            lines.append("  - (none)")
        lines.append("data type harmonization applied before append:")
        for item in info["year_logs"]:
            lines.append(f"  - {item['year']}: {', '.join(item['type_harmonization'])}")
        lines.append(
            f"duplicate column names: {', '.join(info['duplicate_columns']) if info['duplicate_columns'] else '(none)'}"
        )
        lines.append(
            f"missing output columns after append: {', '.join(info['missing_standardized']) if info['missing_standardized'] else '(none)'}"
        )
        lines.append("-" * 96)

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    MERGED_DIR.mkdir(parents=True, exist_ok=True)

    main_output = MERGED_DIR / "nia_2020_2024_merged.csv"
    extended_output = MERGED_DIR / "nia_2019_2024_extended.csv"

    main_info = append_years(MAIN_YEARS, main_output)
    extended_info = append_years(EXTENDED_YEARS, extended_output)

    write_log(main_info, extended_info)

    print(
        f"[main] rows={main_info['actual_rows']}, years={main_info['year_distribution']}, "
        f"row_check={main_info['expected_rows'] == main_info['actual_rows']}"
    )
    print(
        f"[extended] rows={extended_info['actual_rows']}, years={extended_info['year_distribution']}, "
        f"row_check={extended_info['expected_rows'] == extended_info['actual_rows']}"
    )
    print(f"append log saved to: {LOG_PATH}")


if __name__ == "__main__":
    main()
