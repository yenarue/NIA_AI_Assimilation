from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
SUBSET_DIR = BASE_DIR / "working" / "subset"
RENAME_DIR = BASE_DIR / "working" / "rename"
LOG_PATH = RENAME_DIR / "rename_log.txt"

# Try UTF-8 first, then Korean encodings as fallback.
ENCODING_CANDIDATES = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]

RENAME_MAPPINGS = {
    2019: {
        "Q33": "it_org_any_raw",
        "Q33A1": "it_org_internal_raw",
        "Q33A2": "it_org_mixed_raw",
        "Q33A3": "it_org_outsource_raw",
        "Q32": "it_invest_share_raw",
        "Q50": "ai_use_raw",
        "Q58A1": "proc_efficiency_raw",
        "Q58A2": "proc_cost_raw",
        "D_SIZE": "firm_size_raw",
        "D_IND": "industry_raw",
        "D_INDSIZE": "industry_size_raw",
        "WT": "weight_raw",
        "year": "year",
    },
    2020: {
        "Q41": "it_org_any_raw",
        "Q41A1": "it_org_internal_raw",
        "Q41A2": "it_org_mixed_raw",
        "Q41A3": "it_org_outsource_raw",
        "Q40": "it_invest_share_raw",
        "Q33": "ai_use_raw",
        "Q42A1": "proc_improve_raw",
        "Q42A3": "decision_improve_raw",
        "Q42A5": "innov_outcome_raw",
        "D_SIZE": "firm_size_raw",
        "D_IND": "industry_raw",
        "D_INDSIZE1": "industry_size_raw",
        "WT": "weight_raw",
        "year": "year",
    },
    2021: {
        "Q44": "it_org_any_raw",
        "Q44A1": "it_org_internal_raw",
        "Q44A2": "it_org_mixed_raw",
        "Q44A3": "it_org_outsource_raw",
        "Q43": "it_invest_share_raw",
        "REQ43": "it_invest_share_cat_raw",
        "Q36": "ai_use_raw",
        "Q45A1": "proc_improve_raw",
        "Q45A3": "decision_improve_raw",
        "Q45A5": "innov_outcome_raw",
        "D_SIZE": "firm_size_raw",
        "D_IND": "industry_raw",
        "D_INDSIZE": "industry_size_raw",
        "RIM_WT": "weight_raw",
        "year": "year",
    },
    2022: {
        "Q44": "it_org_any_raw",
        "Q44A1": "it_org_internal_raw",
        "Q44A2": "it_org_mixed_raw",
        "Q44A3": "it_org_outsource_raw",
        "Q43": "it_invest_share_raw",
        "REQ43": "it_invest_share_cat_raw",
        "Q36": "ai_use_raw",
        "Q45A1": "proc_improve_raw",
        "Q45A3": "decision_improve_raw",
        "Q45A5": "innov_outcome_raw",
        "D_SIZE": "firm_size_raw",
        "D_IND": "industry_raw",
        "D_INDSIZE": "industry_size_raw",
        "RIM_WT": "weight_raw",
        "year": "year",
    },
    2023: {
        "Q34": "it_org_any_raw",
        "Q34_1_1": "it_org_internal_raw",
        "Q34_1_2": "it_org_mixed_raw",
        "Q34_1_3": "it_org_outsource_raw",
        "Q33": "it_invest_share_raw",
        "REQ33": "it_invest_share_cat_raw",
        "Q28": "ai_use_raw",
        "Q35_1": "proc_improve_raw",
        "Q35_3": "decision_improve_raw",
        "Q35_5": "innov_outcome_raw",
        "D_SIZE": "firm_size_raw",
        "D_IND": "industry_raw",
        "D_INDSIZE": "industry_size_raw",
        "RIM_WT": "weight_raw",
        "year": "year",
    },
    2024: {
        "Q34": "it_org_any_raw",
        "Q34_1_1": "it_org_internal_raw",
        "Q34_1_2": "it_org_mixed_raw",
        "Q34_1_3": "it_org_outsource_raw",
        "Q33": "it_invest_share_raw",
        "REQ33": "it_invest_share_cat_raw",
        "Q28": "ai_use_raw",
        "Q35_1": "proc_improve_raw",
        "Q35_3": "decision_improve_raw",
        "Q35_5": "innov_outcome_raw",
        "D_SIZE": "firm_size_raw",
        "D_IND": "industry_raw",
        "D_INDSIZE": "industry_size_raw",
        "RIM_WT": "weight_raw",
        "year": "year",
    },
}


def detect_encoding(csv_path: Path) -> str:
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
        f"Could not decode {csv_path} with supported encodings.",
    )


def format_mapping(mapping: dict[str, str]) -> str:
    return ", ".join(f"{source} -> {target}" for source, target in mapping.items())


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "(none)"


def rename_one_year(year: int) -> dict[str, object]:
    input_path = SUBSET_DIR / f"nia_{year}_subset.csv"
    output_path = RENAME_DIR / f"nia_{year}_renamed.csv"
    requested_mapping = RENAME_MAPPINGS[year]

    encoding = detect_encoding(input_path)
    df = pd.read_csv(
        input_path,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
    )

    columns_found = [column for column in requested_mapping if column in df.columns]
    columns_missing = [
        column for column in requested_mapping if column not in df.columns
    ]

    if "year" not in df.columns:
        df["year"] = str(year)
        if "year" in columns_missing:
            columns_missing.remove("year")
        if "year" not in columns_found:
            columns_found.append("year")

    rename_map = {
        source: target for source, target in requested_mapping.items() if source in df.columns
    }
    renamed_df = df.rename(columns=rename_map)
    renamed_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return {
        "year": year,
        "input_path": input_path,
        "output_path": output_path,
        "encoding": encoding,
        "requested_mapping": requested_mapping,
        "columns_found": columns_found,
        "columns_missing": columns_missing,
        "row_count": len(renamed_df),
        "final_columns": renamed_df.columns.tolist(),
    }


def write_log(results: list[dict[str, object]]) -> None:
    lines: list[str] = []
    lines.append("NIA rename log")
    lines.append("=" * 80)

    for result in results:
        lines.append(f"Year: {result['year']}")
        lines.append(f"Input file: {result['input_path']}")
        lines.append(f"Output file: {result['output_path']}")
        lines.append(f"Encoding used: {result['encoding']}")
        lines.append(
            f"Requested rename mapping: {format_mapping(result['requested_mapping'])}"
        )
        lines.append(f"Columns found: {format_list(result['columns_found'])}")
        lines.append(f"Columns missing: {format_list(result['columns_missing'])}")
        lines.append(f"Row count: {result['row_count']}")
        lines.append(f"Final columns after rename: {format_list(result['final_columns'])}")
        lines.append("-" * 80)

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RENAME_DIR.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []

    for year in sorted(RENAME_MAPPINGS):
        result = rename_one_year(year)
        results.append(result)

        print(
            f"[{year}] rows={result['row_count']}, "
            f"found={len(result['columns_found'])}, "
            f"missing={len(result['columns_missing'])}"
        )
        if result["columns_missing"]:
            print(f"  missing columns: {format_list(result['columns_missing'])}")

    write_log(results)
    print(f"Rename log saved to: {LOG_PATH}")


if __name__ == "__main__":
    main()
