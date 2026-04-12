from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import math
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RENAME_DIR = BASE_DIR / "working" / "rename"
CLEANED_DIR = BASE_DIR / "working" / "cleaned"
RAW_DIR = BASE_DIR / "raw"

LOG_PATH = CLEANED_DIR / "cleaning_log.txt"
PROFILE_PATH = CLEANED_DIR / "value_profile_by_year.csv"
CLASSIFICATION_PATH = CLEANED_DIR / "variable_classification_report.csv"

ENCODING_CANDIDATES = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]
EMPTY_MARKERS = {
    "",
    ".",
    "-",
    "--",
    "NA",
    "N/A",
    "na",
    "n/a",
    "None",
    "none",
    "null",
    "NULL",
    "unknown",
    "Unknown",
}

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
    "ai_use",
    "proc_improve",
    "innov_outcome",
    "decision_improve",
]

RAW_COLUMNS_BY_YEAR = {
    2019: [
        "year",
        "weight_raw",
        "industry_raw",
        "industry_size_raw",
        "firm_size_raw",
        "it_org_any_raw",
        "it_org_internal_raw",
        "it_org_mixed_raw",
        "it_org_outsource_raw",
        "it_invest_share_raw",
        "ai_use_raw",
        "proc_efficiency_raw",
        "proc_cost_raw",
    ],
    2020: [
        "year",
        "weight_raw",
        "industry_raw",
        "industry_size_raw",
        "firm_size_raw",
        "it_org_any_raw",
        "it_org_internal_raw",
        "it_org_mixed_raw",
        "it_org_outsource_raw",
        "it_invest_share_raw",
        "ai_use_raw",
        "proc_improve_raw",
        "decision_improve_raw",
        "innov_outcome_raw",
    ],
    2021: [
        "year",
        "weight_raw",
        "industry_raw",
        "industry_size_raw",
        "firm_size_raw",
        "it_org_any_raw",
        "it_org_internal_raw",
        "it_org_mixed_raw",
        "it_org_outsource_raw",
        "it_invest_share_raw",
        "it_invest_share_cat_raw",
        "ai_use_raw",
        "proc_improve_raw",
        "decision_improve_raw",
        "innov_outcome_raw",
    ],
    2022: [
        "year",
        "weight_raw",
        "industry_raw",
        "industry_size_raw",
        "firm_size_raw",
        "it_org_any_raw",
        "it_org_internal_raw",
        "it_org_mixed_raw",
        "it_org_outsource_raw",
        "it_invest_share_raw",
        "it_invest_share_cat_raw",
        "ai_use_raw",
        "proc_improve_raw",
        "decision_improve_raw",
        "innov_outcome_raw",
    ],
    2023: [
        "year",
        "weight_raw",
        "industry_raw",
        "industry_size_raw",
        "firm_size_raw",
        "it_org_any_raw",
        "it_org_internal_raw",
        "it_org_mixed_raw",
        "it_org_outsource_raw",
        "it_invest_share_raw",
        "it_invest_share_cat_raw",
        "ai_use_raw",
        "proc_improve_raw",
        "decision_improve_raw",
        "innov_outcome_raw",
    ],
    2024: [
        "year",
        "weight_raw",
        "industry_raw",
        "industry_size_raw",
        "firm_size_raw",
        "it_org_any_raw",
        "it_org_internal_raw",
        "it_org_mixed_raw",
        "it_org_outsource_raw",
        "it_invest_share_raw",
        "it_invest_share_cat_raw",
        "ai_use_raw",
        "proc_improve_raw",
        "decision_improve_raw",
        "innov_outcome_raw",
    ],
}

SOURCE_VARIABLES = {
    2019: {
        "weight_raw": "WT",
        "industry_raw": "D_IND",
        "industry_size_raw": "D_INDSIZE",
        "firm_size_raw": "D_SIZE",
        "it_org_any_raw": "Q33",
        "it_org_internal_raw": "Q33A1",
        "it_org_mixed_raw": "Q33A2",
        "it_org_outsource_raw": "Q33A3",
        "it_invest_share_raw": "Q32",
        "ai_use_raw": "Q50",
        "proc_efficiency_raw": "Q58A1",
        "proc_cost_raw": "Q58A2",
    },
    2020: {
        "weight_raw": "WT",
        "industry_raw": "D_IND",
        "industry_size_raw": "D_INDSIZE1",
        "it_org_any_raw": "Q41",
        "it_org_internal_raw": "Q41A1",
        "it_org_mixed_raw": "Q41A2",
        "it_org_outsource_raw": "Q41A3",
        "it_invest_share_raw": "Q40",
        "ai_use_raw": "Q33",
        "proc_improve_raw": "Q42A1",
        "decision_improve_raw": "Q42A3",
        "innov_outcome_raw": "Q42A5",
    },
    2021: {
        "weight_raw": "RIM_WT",
        "industry_raw": "D_IND",
        "industry_size_raw": "D_INDSIZE",
        "firm_size_raw": "D_SIZE",
        "it_org_any_raw": "Q44",
        "it_org_internal_raw": "Q44A1",
        "it_org_mixed_raw": "Q44A2",
        "it_org_outsource_raw": "Q44A3",
        "it_invest_share_raw": "Q43",
        "it_invest_share_cat_raw": "REQ43",
        "ai_use_raw": "Q36",
        "proc_improve_raw": "Q45A1",
        "decision_improve_raw": "Q45A3",
        "innov_outcome_raw": "Q45A5",
    },
    2022: {
        "weight_raw": "RIM_WT",
        "industry_raw": "D_IND",
        "industry_size_raw": "D_INDSIZE",
        "firm_size_raw": "D_SIZE",
        "it_org_any_raw": "Q44",
        "it_org_internal_raw": "Q44A1",
        "it_org_mixed_raw": "Q44A2",
        "it_org_outsource_raw": "Q44A3",
        "it_invest_share_raw": "Q43",
        "it_invest_share_cat_raw": "REQ43",
        "ai_use_raw": "Q36",
        "proc_improve_raw": "Q45A1",
        "decision_improve_raw": "Q45A3",
        "innov_outcome_raw": "Q45A5",
    },
    2023: {
        "weight_raw": "RIM_WT",
        "industry_raw": "D_IND",
        "industry_size_raw": "D_INDSIZE",
        "firm_size_raw": "D_SIZE",
        "it_org_any_raw": "Q34",
        "it_org_internal_raw": "Q34_1_1",
        "it_org_mixed_raw": "Q34_1_2",
        "it_org_outsource_raw": "Q34_1_3",
        "it_invest_share_raw": "Q33",
        "it_invest_share_cat_raw": "REQ33",
        "ai_use_raw": "Q28",
        "proc_improve_raw": "Q35_1",
        "decision_improve_raw": "Q35_3",
        "innov_outcome_raw": "Q35_5",
    },
    2024: {
        "weight_raw": "RIM_WT",
        "industry_raw": "D_IND",
        "industry_size_raw": "D_INDSIZE",
        "firm_size_raw": "D_SIZE",
        "it_org_any_raw": "Q34",
        "it_org_internal_raw": "Q34_1_1",
        "it_org_mixed_raw": "Q34_1_2",
        "it_org_outsource_raw": "Q34_1_3",
        "it_invest_share_raw": "Q33",
        "it_invest_share_cat_raw": "REQ33",
        "ai_use_raw": "Q28",
        "proc_improve_raw": "Q35_1",
        "decision_improve_raw": "Q35_3",
        "innov_outcome_raw": "Q35_5",
    },
}

TYPE_HINTS = {
    "weight_raw": "continuous_numeric",
    "industry_raw": "nominal_categorical",
    "industry_size_raw": "nominal_categorical",
    "firm_size_raw": "ordinal_likert_or_ordered_category",
    "it_org_any_raw": "binary_yes_no",
    "it_org_internal_raw": "binary_yes_no",
    "it_org_mixed_raw": "binary_yes_no",
    "it_org_outsource_raw": "binary_yes_no",
    "it_invest_share_raw": "continuous_numeric",
    "it_invest_share_cat_raw": "ordinal_likert_or_ordered_category",
    "ai_use_raw": "binary_yes_no",
    "proc_efficiency_raw": "ordinal_likert_or_ordered_category",
    "proc_cost_raw": "ordinal_likert_or_ordered_category",
    "proc_improve_raw": "ordinal_likert_or_ordered_category",
    "decision_improve_raw": "ordinal_likert_or_ordered_category",
    "innov_outcome_raw": "ordinal_likert_or_ordered_category",
}


@dataclass
class CodebookInfo:
    path: Path | None
    labels_by_var: dict[str, dict[str, str]]
    warnings: list[str]


def detect_encoding(path: Path) -> str:
    for encoding in ENCODING_CANDIDATES:
        try:
            pd.read_csv(path, encoding=encoding, nrows=0)
            return encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"인코딩 판별 실패: {path}")


def normalize_missing(value: Any) -> Any:
    if pd.isna(value):
        return pd.NA
    if isinstance(value, str):
        stripped = value.strip()
        if stripped in EMPTY_MARKERS or stripped == "":
            return pd.NA
        return stripped
    return value


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for col in result.columns:
        result[col] = result[col].map(normalize_missing)
    return result


def normalize_code_key(value: Any) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
        if math.isfinite(number) and number.is_integer():
            return str(int(number))
        return str(number)
    except Exception:
        return text


def safe_numeric(series: pd.Series, strip_percent: bool = False) -> pd.Series:
    text = series.map(lambda v: pd.NA if pd.isna(v) else str(v).strip())
    text = text.map(lambda v: pd.NA if pd.isna(v) else v.replace(",", ""))
    if strip_percent:
        text = text.map(lambda v: pd.NA if pd.isna(v) else v.replace("%", ""))
    text = text.map(lambda v: pd.NA if pd.isna(v) else re.sub(r"\s+", "", v))
    return pd.to_numeric(text, errors="coerce")


def maybe_integer(series: pd.Series) -> bool:
    non_missing = series.dropna()
    return non_missing.empty or non_missing.map(lambda x: float(x).is_integer()).all()


def as_numeric_if_possible(series: pd.Series) -> pd.Series:
    numeric = safe_numeric(series)
    if numeric.notna().sum() == series.notna().sum():
        return numeric.astype("Int64") if maybe_integer(numeric) else numeric
    return series.astype("string")


def discover_codebook(year: int) -> CodebookInfo:
    matches = sorted(RAW_DIR.glob(f"nia_{year}_codebook.*"))
    if not matches:
        return CodebookInfo(None, {}, [f"{year}년 코드북 파일을 찾지 못했습니다."])

    path = matches[0]
    try:
        if path.suffix.lower() == ".xlsx":
            excel = pd.ExcelFile(path)
            sheet = next((s for s in excel.sheet_names if "value" in s.lower() or "codebook" in s.lower()), excel.sheet_names[-1])
            raw = pd.read_excel(path, sheet_name=sheet)
        else:
            raw = pd.read_csv(path, encoding=detect_encoding(path))
    except Exception as exc:
        return CodebookInfo(path, {}, [f"{year}년 코드북 파싱 실패: {exc!r}"])

    if raw.shape[1] < 4:
        return CodebookInfo(path, {}, [f"{year}년 코드북 구조가 예상과 달라 값 레이블 파싱을 건너뛰었습니다."])

    raw = raw.iloc[:, :4].copy()
    raw.columns = ["var_name", "var_desc", "code", "label"]

    labels_by_var: dict[str, dict[str, str]] = {}
    current_var: str | None = None
    for _, row in raw.iterrows():
        if pd.notna(row["var_name"]):
            current_var = str(row["var_name"]).strip()
            labels_by_var.setdefault(current_var, {})
        if not current_var or pd.isna(row["code"]) or pd.isna(row["label"]):
            continue
        key = normalize_code_key(row["code"])
        if key:
            labels_by_var[current_var][key] = str(row["label"]).strip()
    return CodebookInfo(path, labels_by_var, [])


def get_series(df: pd.DataFrame, col: str) -> pd.Series:
    if col in df.columns:
        return df[col]
    return pd.Series(pd.NA, index=df.index, dtype="object")


def unique_profile(series: pd.Series, limit: int = 20) -> str:
    values = sorted({str(v) for v in series.dropna().tolist()})
    if not values:
        return ""
    if len(values) <= limit:
        return "|".join(values)
    return "|".join(values[:limit]) + f"|...(+{len(values) - limit})"


def summarize_labels(labels: dict[str, str]) -> str:
    if not labels:
        return ""
    return " / ".join(f"{k}:{v}" for k, v in list(labels.items())[:8])


def classify_variable(year: int, raw_col: str, series: pd.Series, codebook: CodebookInfo) -> dict[str, str]:
    source_var = SOURCE_VARIABLES[year].get(raw_col, raw_col)
    labels = codebook.labels_by_var.get(source_var, {})
    observed = sorted({normalize_code_key(v) for v in series.dropna().tolist() if normalize_code_key(v) is not None})
    warnings: list[str] = []
    inferred_type = TYPE_HINTS.get(raw_col, "unknown")

    if inferred_type == "binary_yes_no" and observed and not (set(observed).issubset({"0", "1"}) or set(observed).issubset({"1", "2"}) or labels):
        warnings.append("binary 후보이나 관측값 구조가 비정형")
    if inferred_type == "ordinal_likert_or_ordered_category" and not observed:
        warnings.append("비결측 값 없음")

    basis = []
    if labels:
        basis.append(f"코드북: {summarize_labels(labels)}")
    basis.append(f"관측값: {','.join(observed[:10])}" + (f" ...(+{len(observed)-10})" if len(observed) > 10 else ""))
    return {
        "year": str(year),
        "variable": raw_col,
        "raw_unique_values": unique_profile(series),
        "inferred_type": inferred_type,
        "mapping_basis": " ; ".join([b for b in basis if b]),
        "warnings": " | ".join(warnings),
    }


def classify_label(label: str) -> str | None:
    text = re.sub(r"\s+", " ", label).strip().lower()
    if any(token in text for token in ["모름", "무응답", "거절", "비해당", "unknown", "no response"]):
        return "missing"
    if any(token in text for token in ["전혀 효과 없음", "효과 없음", "아니오", "미보유", "not selected", "no"]):
        return "negative"
    if any(token in text for token in ["매우 효과 있음", "효과 있음", "예", "보유", "해당", "selected", "yes"]):
        return "positive"
    return None


def build_binary_mapping(year: int, raw_col: str, series: pd.Series, codebook: CodebookInfo) -> tuple[dict[str, Any], list[str], list[str], list[str]]:
    source_var = SOURCE_VARIABLES[year].get(raw_col, raw_col)
    labels = codebook.labels_by_var.get(source_var, {})
    mapping: dict[str, Any] = {}
    mapping_log: list[str] = []
    missing_log: list[str] = []
    warnings: list[str] = []

    for code, label in labels.items():
        label_class = classify_label(label)
        if label_class == "positive":
            mapping[code] = 1
            mapping_log.append(f"{source_var}: {code}({label}) -> 1")
        elif label_class == "negative":
            mapping[code] = 0
            mapping_log.append(f"{source_var}: {code}({label}) -> 0")
        elif label_class == "missing":
            mapping[code] = pd.NA
            missing_log.append(f"{source_var}: {code}({label}) -> 결측")

    observed = sorted({normalize_code_key(v) for v in series.dropna().tolist() if normalize_code_key(v) is not None})
    if set(observed).issubset({"0", "1"}) and not mapping:
        mapping = {"0": 0, "1": 1}
        mapping_log.append(f"{raw_col}: 관측값 {{0,1}} 유지")
    elif set(observed).issubset({"1", "2"}) and not labels:
        warnings.append(f"{raw_col}: 관측값이 {{1,2}}이지만 코드북 근거가 없어 자동 매핑하지 않았습니다.")

    # AI use special rule: code 3 is also treated as non-use (0), not missing.
    if raw_col == "ai_use_raw" and "3" in observed:
        mapping["3"] = 0
        mapping_log.append(f"{SOURCE_VARIABLES[year].get(raw_col, raw_col)}: 3 -> 0")
        missing_log = [item for item in missing_log if not item.startswith(f"{SOURCE_VARIABLES[year].get(raw_col, raw_col)}: 3(")]
    return mapping, mapping_log, missing_log, warnings


def apply_binary_mapping(series: pd.Series, mapping: dict[str, Any]) -> pd.Series:
    return series.map(normalize_code_key).map(mapping).astype("Int64")


def build_missing_code_map(year: int, raw_col: str, codebook: CodebookInfo) -> dict[str, str]:
    source_var = SOURCE_VARIABLES[year].get(raw_col, raw_col)
    labels = codebook.labels_by_var.get(source_var, {})
    return {code: label for code, label in labels.items() if classify_label(label) == "missing"}


def preserve_ordered_numeric(series: pd.Series, year: int, raw_col: str, codebook: CodebookInfo) -> tuple[pd.Series, list[str]]:
    numeric = safe_numeric(series)
    missing_codes = build_missing_code_map(year, raw_col, codebook)
    if missing_codes:
        numeric = numeric.mask(series.map(normalize_code_key).isin(missing_codes.keys()), pd.NA)
    warnings = []
    unexpected = sorted({str(v) for v in numeric.dropna().tolist() if v not in [1, 2, 3, 4, 5]})
    if unexpected:
        warnings.append(f"{raw_col}: 1~5 외 관측값 {', '.join(unexpected[:10])} 존재")
    return numeric.astype("Int64") if maybe_integer(numeric) else numeric, warnings


def add_profile_row(rows: list[dict[str, Any]], year: int, variable: str, raw_series: pd.Series, cleaned_series: pd.Series, inferred_type: str, notes: str) -> None:
    rows.append(
        {
            "year": year,
            "variable": variable,
            "raw_unique_values": unique_profile(raw_series),
            "raw_non_missing_n": int(raw_series.notna().sum()),
            "raw_missing_n": int(raw_series.isna().sum()),
            "cleaned_unique_values": unique_profile(cleaned_series),
            "cleaned_non_missing_n": int(cleaned_series.notna().sum()),
            "cleaned_missing_n": int(cleaned_series.isna().sum()),
            "inferred_type": inferred_type,
            "notes": notes,
        }
    )


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def derive_org_type(df: pd.DataFrame) -> pd.Series:
    internal = df["it_org_internal"].eq(1).fillna(False)
    mixed = df["it_org_mixed"].eq(1).fillna(False)
    outsource = df["it_org_outsource"].eq(1).fillna(False)
    any_no = df["it_org_any"].eq(0).fillna(False)

    result = pd.Series(pd.NA, index=df.index, dtype="Int64")
    count = internal.astype(int) + mixed.astype(int) + outsource.astype(int)
    result = result.mask((count == 0) & any_no, 0)
    result = result.mask(internal & ~mixed & ~outsource, 1)
    result = result.mask(~internal & mixed & ~outsource, 2)
    result = result.mask(~internal & ~mixed & outsource, 3)
    result = result.mask(count >= 2, 4)
    return result.astype("Int64")


def clean_one_year(year: int) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, str]]]:
    input_path = RENAME_DIR / f"nia_{year}_renamed.csv"
    output_path = CLEANED_DIR / f"nia_{year}_cleaned.csv"
    encoding = detect_encoding(input_path)

    raw_df = pd.read_csv(input_path, encoding=encoding, dtype=str, keep_default_na=False, na_filter=False)
    rows_before = len(raw_df)
    df = normalize_dataframe(raw_df)
    codebook = discover_codebook(year)

    if "year" not in df.columns:
        df["year"] = str(year)
    df["year"] = safe_numeric(df["year"]).astype("Int64")

    profile_rows: list[dict[str, Any]] = []
    classification_rows: list[dict[str, str]] = []
    warnings = list(codebook.warnings)
    binary_logs: list[str] = []
    missing_logs: list[str] = ['공통 결측 규칙: "", 공백, ".", "-", "--", "NA", "N/A", "None", "null", "unknown" -> 결측']
    action_logs: list[str] = []
    unresolved_logs: list[str] = []

    for raw_col in RAW_COLUMNS_BY_YEAR[year]:
        if raw_col == "year":
            continue
        classification_rows.append(classify_variable(year, raw_col, get_series(df, raw_col), codebook))

    cleaned = pd.DataFrame(index=df.index)
    cleaned["year"] = df["year"]
    cleaned["weight"] = safe_numeric(get_series(df, "weight_raw"))
    cleaned["industry"] = as_numeric_if_possible(get_series(df, "industry_raw"))
    cleaned["industry_size"] = as_numeric_if_possible(get_series(df, "industry_size_raw"))

    if "firm_size_raw" in df.columns:
        cleaned["firm_size"] = as_numeric_if_possible(df["firm_size_raw"])
    else:
        cleaned["firm_size"] = pd.Series(pd.NA, index=df.index, dtype="object")
        warnings.append("2020년 firm_size_raw가 없어 firm_size를 전체 결측으로 생성했습니다.")

    # binary concept variables
    for raw_col, clean_col in {
        "it_org_any_raw": "it_org_any",
        "it_org_internal_raw": "it_org_internal",
        "it_org_mixed_raw": "it_org_mixed",
        "it_org_outsource_raw": "it_org_outsource",
        "ai_use_raw": "ai_use",
    }.items():
        series = get_series(df, raw_col)
        mapping, map_logs, miss_logs, map_warnings = build_binary_mapping(year, raw_col, series, codebook)
        binary_logs.extend(map_logs)
        missing_logs.extend(miss_logs)
        warnings.extend(map_warnings)
        cleaned[clean_col] = apply_binary_mapping(series, mapping) if mapping else pd.Series(pd.NA, index=df.index, dtype="Int64")
        add_profile_row(profile_rows, year, raw_col, series, cleaned[clean_col], TYPE_HINTS.get(raw_col, "unknown"), "binary standardization")

    # organization hierarchy cleanup
    subs = ["it_org_internal", "it_org_mixed", "it_org_outsource"]
    sub_all_missing = cleaned[subs].isna().all(axis=1)
    fill_zero_mask = cleaned["it_org_any"].eq(0) & sub_all_missing
    if fill_zero_mask.any():
        for col in subs:
            cleaned.loc[fill_zero_mask, col] = 0
        action_logs.append(f"it_org_any==0 & 하위3문항 모두 결측인 {int(fill_zero_mask.sum())}건에 대해 하위 3문항을 0으로 채웠습니다.")

    any_yes_mask = cleaned["it_org_any"].eq(1)
    for col in subs:
        blank_under_yes = any_yes_mask & cleaned[col].isna()
        if blank_under_yes.any():
            cleaned.loc[blank_under_yes, col] = 0
            action_logs.append(f"it_org_any==1 이고 {col}가 결측인 {int(blank_under_yes.sum())}건에 대해 {col}=0으로 채웠습니다.")

    inconsistent_mask = cleaned["it_org_any"].eq(0) & cleaned[subs].eq(1).any(axis=1)
    if inconsistent_mask.any():
        cleaned.loc[inconsistent_mask, "it_org_any"] = 1
        action_logs.append(f"it_org_any==0인데 하위문항 중 1이 존재한 불일치 {int(inconsistent_mask.sum())}건은 하위문항 증거를 우선해 it_org_any=1로 보정했습니다.")

    cleaned["it_org_type"] = derive_org_type(cleaned)

    # investment share
    invest_raw = get_series(df, "it_invest_share_raw")
    invest_num = safe_numeric(invest_raw, strip_percent=True)
    invest_missing_codes = build_missing_code_map(year, "it_invest_share_raw", codebook)
    if invest_missing_codes:
        invest_num = invest_num.mask(invest_raw.map(normalize_code_key).isin(invest_missing_codes.keys()), pd.NA)
        missing_logs.extend([f"{SOURCE_VARIABLES[year]['it_invest_share_raw']}: {k}({v}) -> 결측" for k, v in invest_missing_codes.items()])
    cleaned["it_invest_share"] = invest_num
    add_profile_row(profile_rows, year, "it_invest_share_raw", invest_raw, cleaned["it_invest_share"], TYPE_HINTS["it_invest_share_raw"], "numeric conversion only")

    # outcomes
    if year == 2019:
        eff_binary, eff_warn = preserve_ordered_numeric(get_series(df, "proc_efficiency_raw"), year, "proc_efficiency_raw", codebook)
        cost_binary, cost_warn = preserve_ordered_numeric(get_series(df, "proc_cost_raw"), year, "proc_cost_raw", codebook)
        warnings.extend(eff_warn + cost_warn)
        proc = pd.Series(pd.NA, index=df.index, dtype="Float64")
        both_present = eff_binary.notna() & cost_binary.notna()
        only_eff = eff_binary.notna() & cost_binary.isna()
        only_cost = eff_binary.isna() & cost_binary.notna()
        proc = proc.mask(both_present, (eff_binary + cost_binary) / 2)
        proc = proc.mask(only_eff, eff_binary.astype("Float64"))
        proc = proc.mask(only_cost, cost_binary.astype("Float64"))
        proc = proc.round().astype("Int64")
        cleaned["proc_improve"] = proc
        cleaned["innov_outcome"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
        cleaned["decision_improve"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
        action_logs.append("2019년 proc_improve는 proc_efficiency_raw와 proc_cost_raw가 둘 다 있으면 평균 후 반올림하고, 하나만 있으면 해당 값을 사용해 생성했습니다.")
        add_profile_row(profile_rows, year, "proc_efficiency_raw", get_series(df, "proc_efficiency_raw"), eff_binary, TYPE_HINTS["proc_efficiency_raw"], "2019 proc_improve input, raw scale preserved")
        add_profile_row(profile_rows, year, "proc_cost_raw", get_series(df, "proc_cost_raw"), cost_binary, TYPE_HINTS["proc_cost_raw"], "2019 proc_improve input, raw scale preserved")
    else:
        for raw_col, clean_col in [
            ("proc_improve_raw", "proc_improve"),
            ("innov_outcome_raw", "innov_outcome"),
            ("decision_improve_raw", "decision_improve"),
        ]:
            ordered, warn = preserve_ordered_numeric(get_series(df, raw_col), year, raw_col, codebook)
            cleaned[clean_col] = ordered
            warnings.extend(warn)
            action_logs.append(f"{raw_col}는 raw 1~5 리커트 값을 그대로 유지하여 {clean_col}에 대입했습니다. 코드북상 명백한 결측코드만 제거했습니다.")
            add_profile_row(profile_rows, year, raw_col, get_series(df, raw_col), cleaned[clean_col], TYPE_HINTS[raw_col], f"raw Likert scale preserved in {clean_col}")

    for col in STANDARDIZED_COLUMNS:
        if col not in cleaned.columns:
            cleaned[col] = pd.Series(pd.NA, index=df.index, dtype="object")

    for col in ["year", "it_org_any", "it_org_internal", "it_org_mixed", "it_org_outsource", "it_org_type", "ai_use"]:
        cleaned[col] = cleaned[col].astype("Int64")

    # validation
    for col in ["it_org_any", "it_org_internal", "it_org_mixed", "it_org_outsource", "ai_use"]:
        bad = cleaned[col].dropna()
        if not bad.empty and not bad.isin([0, 1]).all():
            unresolved_logs.append(f"{col}: binary 변수에 0/1 외 값 존재")

    if year == 2020 and cleaned["firm_size"].notna().sum() > 0:
        unresolved_logs.append("2020 firm_size가 결측이어야 하는데 비결측이 존재합니다.")
    if any(col.endswith("_ord") for col in cleaned.columns):
        unresolved_logs.append("_ord 열이 생성되면 안 되는데 생성되었습니다.")
    if "it_invest_share_cat" in cleaned.columns:
        unresolved_logs.append("it_invest_share_cat가 cleaned 표준 변수에 포함되면 안 됩니다.")

    raw_output_columns = [col for col in RAW_COLUMNS_BY_YEAR[year] if col in df.columns and col != "year"]
    final_df = pd.concat([cleaned[STANDARDIZED_COLUMNS], df[raw_output_columns]], axis=1)
    final_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    for raw_col in raw_output_columns:
        add_profile_row(profile_rows, year, raw_col, df[raw_col], get_series(final_df, raw_col), TYPE_HINTS.get(raw_col, "unknown"), "raw preserved")

    return {
        "year": year,
        "input_file": input_path,
        "output_file": output_path,
        "codebook_file": str(codebook.path) if codebook.path else "찾지 못함",
        "rows_before": rows_before,
        "rows_after": len(final_df),
        "classification_summary": classification_rows,
        "missing_columns": [col for col in RAW_COLUMNS_BY_YEAR[year] if col not in df.columns],
        "standardized_columns": STANDARDIZED_COLUMNS,
        "binary_logs": dedupe(binary_logs),
        "missing_logs": dedupe(missing_logs),
        "action_logs": dedupe(action_logs),
        "warnings": dedupe(warnings),
        "unresolved": dedupe(unresolved_logs),
    }, profile_rows, classification_rows


def write_cleaning_log(results: list[dict[str, Any]]) -> None:
    lines: list[str] = []
    lines.append("NIA cleaned 파일 생성 로그")
    lines.append("=" * 96)
    for result in results:
        lines.append(f"연도: {result['year']}")
        lines.append(f"source file: {result['input_file']}")
        lines.append(f"matched codebook file: {result['codebook_file']}")
        lines.append(f"output file: {result['output_file']}")
        lines.append(f"row count before / after: {result['rows_before']} -> {result['rows_after']}")
        lines.append("변수 분류 요약:")
        for row in result["classification_summary"]:
            note = f" / 경고={row['warnings']}" if row["warnings"] else ""
            lines.append(f"  - {row['variable']}: {row['inferred_type']}{note}")
        lines.append(f"표준 변수 생성 결과: {', '.join(result['standardized_columns'])}")
        lines.append(f"누락 컬럼: {', '.join(result['missing_columns']) if result['missing_columns'] else '(없음)'}")
        lines.append("raw -> cleaned 매핑 / 처리:")
        if result["action_logs"]:
            lines.extend([f"  - {item}" for item in result["action_logs"]])
        else:
            lines.append("  - 없음")
        lines.append("binary 매핑 규칙:")
        if result["binary_logs"]:
            lines.extend([f"  - {item}" for item in result["binary_logs"]])
        else:
            lines.append("  - 없음")
        lines.append("결측 처리 규칙:")
        if result["missing_logs"]:
            lines.extend([f"  - {item}" for item in result["missing_logs"]])
        else:
            lines.append("  - 없음")
        lines.append("warnings:")
        if result["warnings"]:
            lines.extend([f"  - {item}" for item in result["warnings"]])
        else:
            lines.append("  - 없음")
        lines.append("unresolved cases:")
        if result["unresolved"]:
            lines.extend([f"  - {item}" for item in result["unresolved"]])
        else:
            lines.append("  - 없음")
        lines.append("-" * 96)
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    log_results: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    classification_rows: list[dict[str, str]] = []

    for year in range(2019, 2025):
        result, year_profiles, year_classifications = clean_one_year(year)
        log_results.append(result)
        profile_rows.extend(year_profiles)
        classification_rows.extend(year_classifications)
        print(
            f"[{year}] rows={result['rows_after']}, "
            f"missing_cols={len(result['missing_columns'])}, "
            f"warnings={len(result['warnings'])}, "
            f"unresolved={len(result['unresolved'])}"
        )

    write_cleaning_log(log_results)
    pd.DataFrame(profile_rows).to_csv(PROFILE_PATH, index=False, encoding="utf-8-sig")
    pd.DataFrame(classification_rows).to_csv(CLASSIFICATION_PATH, index=False, encoding="utf-8-sig")
    print(f"cleaning log saved to: {LOG_PATH}")
    print(f"value profile saved to: {PROFILE_PATH}")
    print(f"classification report saved to: {CLASSIFICATION_PATH}")


if __name__ == "__main__":
    main()
