from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "working" / "cleaned"
OUTPUT_DIR = BASE_DIR / "cleaned_v2"
LOG_PATH = OUTPUT_DIR / "invest_share_standardization_log.txt"
CHECK_PATH = OUTPUT_DIR / "invest_share_value_check.csv"

YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
SPECIAL_MISSING_CODES = {997, 998, 999}


def safe_numeric(series: pd.Series) -> tuple[pd.Series, int]:
    """Safely convert text values to numeric after stripping spaces, commas, and percent signs."""
    text = series.astype("object").map(lambda v: pd.NA if pd.isna(v) else str(v).strip())
    text = text.map(lambda v: pd.NA if pd.isna(v) or v == "" else v)
    text = text.map(lambda v: pd.NA if pd.isna(v) else v.replace(",", "").replace("%", ""))
    numeric = pd.to_numeric(text, errors="coerce")
    failed_count = int(series.notna().sum() - numeric.notna().sum())
    return numeric, failed_count


def apply_special_missing_codes(series: pd.Series) -> tuple[pd.Series, int]:
    """Replace 997/998/999 style special codes with missing."""
    cleaned = series.copy()
    mask = cleaned.isin(list(SPECIAL_MISSING_CODES))
    count = int(mask.sum())
    cleaned = cleaned.mask(mask, pd.NA)
    return cleaned, count


def recode_std4_from_cat(series: pd.Series) -> pd.Series:
    """Direct mapping when the source already represents the 4 ordered categories."""
    mapped = series.map({1: 1, 2: 2, 3: 3, 4: 4})
    return mapped.astype("Int64")


def recode_std4_from_pct(series: pd.Series) -> pd.Series:
    """Recode actual percent values into the common 4-category scheme."""
    result = pd.Series(pd.NA, index=series.index, dtype="Int64")
    result = result.mask(series.le(1), 1)
    result = result.mask(series.gt(1) & series.lt(5), 2)
    result = result.mask(series.ge(5) & series.lt(10), 3)
    result = result.mask(series.ge(10), 4)
    return result.astype("Int64")


def summarize_std4_counts(series: pd.Series) -> dict[str, int]:
    return {
        "std4_non_missing_n": int(series.notna().sum()),
        "std4_value_1_n": int(series.eq(1).sum()),
        "std4_value_2_n": int(series.eq(2).sum()),
        "std4_value_3_n": int(series.eq(3).sum()),
        "std4_value_4_n": int(series.eq(4).sum()),
        "std4_missing_n": int(series.isna().sum()),
    }


def summarize_pct(series: pd.Series) -> dict[str, Any]:
    non_missing = series.dropna()
    if non_missing.empty:
        return {
            "pct_non_missing_n": 0,
            "pct_missing_n": int(series.isna().sum()),
            "pct_min": pd.NA,
            "pct_p25": pd.NA,
            "pct_median": pd.NA,
            "pct_p75": pd.NA,
            "pct_max": pd.NA,
        }
    return {
        "pct_non_missing_n": int(non_missing.notna().sum()),
        "pct_missing_n": int(series.isna().sum()),
        "pct_min": float(non_missing.min()),
        "pct_p25": float(non_missing.quantile(0.25)),
        "pct_median": float(non_missing.quantile(0.50)),
        "pct_p75": float(non_missing.quantile(0.75)),
        "pct_max": float(non_missing.max()),
    }


def process_one_year(year: int) -> tuple[dict[str, Any], dict[str, Any]]:
    input_path = INPUT_DIR / f"nia_{year}_cleaned.csv"
    output_path = OUTPUT_DIR / f"nia_{year}_cleaned.csv"

    df = pd.read_csv(input_path, encoding="utf-8-sig", dtype=str, keep_default_na=False, na_filter=False)
    input_rows = len(df)

    warnings: list[str] = []
    notes: list[str] = []

    raw_num, raw_failed = safe_numeric(df["it_invest_share_raw"]) if "it_invest_share_raw" in df.columns else (pd.Series(pd.NA, index=df.index, dtype="float64"), 0)
    raw_num, raw_special_count = apply_special_missing_codes(raw_num)

    cat_exists = "it_invest_share_cat_raw" in df.columns
    cat_num = pd.Series(float("nan"), index=df.index, dtype="float64")
    cat_failed = 0
    cat_special_count = 0
    cat_used = False
    raw_recode_used = False

    if cat_exists:
        cat_num, cat_failed = safe_numeric(df["it_invest_share_cat_raw"])
        cat_num, cat_special_count = apply_special_missing_codes(cat_num)

    if year in [2019, 2020]:
        source_raw_column_used = "it_invest_share_raw"
        source_cat_column_used = ""
        std4 = recode_std4_from_cat(raw_num)
        pct = pd.Series(pd.NA, index=df.index, dtype="Float64")
        raw_recode_used = True
        notes.append("2019~2020은 원값을 범주 코드로 간주하여 std4에 직접 매핑함")
    else:
        cat_valid = bool(cat_exists and cat_num.notna().sum() > 0)
        if cat_valid:
            std4 = recode_std4_from_cat(cat_num)
            source_raw_column_used = "it_invest_share_raw"
            source_cat_column_used = "it_invest_share_cat_raw"
            cat_used = True
            notes.append("cat_raw 우선 사용")
        else:
            std4 = recode_std4_from_pct(raw_num)
            source_raw_column_used = "it_invest_share_raw"
            source_cat_column_used = "it_invest_share_cat_raw" if cat_exists else ""
            raw_recode_used = True
            notes.append("cat_raw 부재 또는 전부 결측이어서 raw 퍼센트에서 std4 직접 재코딩")
        pct = raw_num.astype("Float64")

    if year in [2019, 2020]:
        pct = pd.Series(pd.NA, index=df.index, dtype="Float64")

    df["it_invest_share_std4"] = std4
    df["it_invest_share_pct"] = pct

    # Remove the old standardized investment-share column from the v2 output
    # and insert the new two columns in its place.
    if "it_invest_share" in df.columns:
        original_columns = df.columns.tolist()
        insert_at = original_columns.index("it_invest_share")
        reordered_columns = [col for col in original_columns if col != "it_invest_share"]
        for new_col in ["it_invest_share_std4", "it_invest_share_pct"]:
            reordered_columns.remove(new_col)
        reordered_columns[insert_at:insert_at] = ["it_invest_share_std4", "it_invest_share_pct"]
        df = df[reordered_columns]

    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    output_rows = len(df)
    invalid_std4 = sorted({str(v) for v in df["it_invest_share_std4"].dropna().tolist() if v not in [1, 2, 3, 4]})
    if invalid_std4:
        warnings.append(f"std4에 허용 외 값 존재: {', '.join(invalid_std4)}")
    if year in [2019, 2020] and df["it_invest_share_pct"].notna().sum() > 0:
        warnings.append(f"{year}년 pct가 결측이어야 하나 비결측이 존재함")
    if input_rows != output_rows:
        warnings.append("입력/출력 행 수가 다름")
    if raw_failed > 0:
        warnings.append(f"raw 숫자 변환 실패 {raw_failed}건")
    if cat_failed > 0:
        warnings.append(f"cat_raw 숫자 변환 실패 {cat_failed}건")

    std4_counts = summarize_std4_counts(df["it_invest_share_std4"])
    pct_summary = summarize_pct(df["it_invest_share_pct"])

    log_info = {
        "year": year,
        "input_file": input_path,
        "output_file": output_path,
        "source_raw_column_used": source_raw_column_used,
        "source_cat_column_used": source_cat_column_used,
        "cat_raw_used": cat_used,
        "raw_direct_recode_used": raw_recode_used,
        "raw_special_missing_count": raw_special_count,
        "cat_special_missing_count": cat_special_count,
        "std4_counts": std4_counts,
        "pct_non_missing_count": pct_summary["pct_non_missing_n"],
        "warnings": warnings,
        "notes": notes,
    }

    check_row = {
        "year": year,
        "source_raw_column_used": source_raw_column_used,
        "source_cat_column_used": source_cat_column_used,
        **std4_counts,
        **pct_summary,
        "notes": " | ".join(notes) if notes else "",
    }
    return log_info, check_row


def write_log(logs: list[dict[str, Any]]) -> None:
    lines: list[str] = []
    lines.append("정보화 투자비중 표준화 로그")
    lines.append("=" * 96)
    for item in logs:
        lines.append(f"연도: {item['year']}")
        lines.append(f"input file: {item['input_file']}")
        lines.append(f"output file: {item['output_file']}")
        lines.append(f"사용한 원천 raw 열: {item['source_raw_column_used']}")
        lines.append(f"사용한 원천 cat 열: {item['source_cat_column_used'] if item['source_cat_column_used'] else '(없음)'}")
        lines.append(f"cat_raw 사용 여부: {item['cat_raw_used']}")
        lines.append(f"raw 직접 재코딩 여부: {item['raw_direct_recode_used']}")
        lines.append("특수코드 결측 처리 규칙: 997, 998, 999 -> 결측")
        lines.append(f"raw 특수코드 결측 처리 건수: {item['raw_special_missing_count']}")
        lines.append(f"cat 특수코드 결측 처리 건수: {item['cat_special_missing_count']}")
        lines.append(
            "std4 value counts: "
            f"1={item['std4_counts']['std4_value_1_n']}, "
            f"2={item['std4_counts']['std4_value_2_n']}, "
            f"3={item['std4_counts']['std4_value_3_n']}, "
            f"4={item['std4_counts']['std4_value_4_n']}, "
            f"missing={item['std4_counts']['std4_missing_n']}"
        )
        lines.append(f"pct non-missing count: {item['pct_non_missing_count']}")
        lines.append(f"notes: {' | '.join(item['notes']) if item['notes'] else '(없음)'}")
        lines.append(f"warnings: {' | '.join(item['warnings']) if item['warnings'] else '(없음)'}")
        lines.append("-" * 96)
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logs: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []

    for year in YEARS:
        log_info, check_row = process_one_year(year)
        logs.append(log_info)
        checks.append(check_row)
        print(
            f"[{year}] std4_non_missing={check_row['std4_non_missing_n']}, "
            f"pct_non_missing={check_row['pct_non_missing_n']}, "
            f"warnings={len(log_info['warnings'])}"
        )

    write_log(logs)
    pd.DataFrame(checks).to_csv(CHECK_PATH, index=False, encoding="utf-8-sig")
    print(f"log saved to: {LOG_PATH}")
    print(f"value check saved to: {CHECK_PATH}")


if __name__ == "__main__":
    main()
