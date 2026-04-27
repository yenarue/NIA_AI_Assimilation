#!/usr/bin/env python3
"""NIA 2024 renamed 파일을 연구용 cleaned 파일로 변환합니다.

주의:
- 이 스크립트는 2024년 단일 연도 clean 단계만 수행합니다.
- 입력 renamed 파일은 덮어쓰지 않습니다.
- midpoint(3)는 결측 처리하지 않고, effect_* 변수는 1~5 값을 유지합니다.
- it_invest_share_pct 및 _ord 계열 파생열은 생성하지 않습니다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "working" / "rename" / "nia_2024_renamed.csv"
OUTPUT_PATH = BASE_DIR / "working" / "cleaned" / "nia_2024_cleaned.csv"
LOG_PATH = BASE_DIR / "working" / "cleaned" / "cleaning_log_2024.txt"
SUMMARY_PATH = BASE_DIR / "working" / "cleaned" / "cleaning_summary_2024.md"


CONTROL_MAPPING = {
    "year": "year",
    "industry_raw": "industry",
    "industry_size_raw": "industry_size",
    "firm_size_raw": "firm_size",
}

YESNO_MAPPING = {
    "it_org_any_raw": "it_org_any",
    "it_invest_any_raw": "it_invest_any",
    "ai_use_raw": "ai_use",
}

IT_ORG_CHILD_MAPPING = {
    "it_org_internal_raw": "it_org_internal",
    "it_org_mixed_raw": "it_org_mixed",
    "it_org_outsource_raw": "it_org_outsource",
}

IT_INVEST_CHILD_MAPPING = {
    "it_invest_hardware_raw": "it_invest_hardware",
    "it_invest_software_raw": "it_invest_software",
    "it_invest_sys_op_raw": "it_invest_sys_op",
    "it_invest_infra_raw": "it_invest_infra",
    "it_invest_op_salary_raw": "it_invest_op_salary",
    "it_invest_new_tech_raw": "it_invest_new_tech",
    "it_invest_rnd_raw": "it_invest_rnd",
    "it_invest_tech_train_raw": "it_invest_tech_train",
}

AI_USE_DETAIL_MAPPING = {
    "ai_use_doc_info_collect_raw": "ai_use_doc_info_collect",
    "ai_use_task_automation_raw": "ai_use_task_automation",
    "ai_use_decision_support_raw": "ai_use_decision_support",
    "ai_use_speech_to_text_raw": "ai_use_speech_to_text",
    "ai_use_gen_summarize_edit_raw": "ai_use_gen_summarize_edit",
    "ai_use_image_video_recognition_raw": "ai_use_image_video_recognition",
    "ai_use_ml_data_analysis_raw": "ai_use_ml_data_analysis",
    "ai_use_text_language_analysis_raw": "ai_use_text_language_analysis",
    "ai_use_autonomous_mobility_raw": "ai_use_autonomous_mobility",
    "ai_use_other_raw": "ai_use_other",
}

AI_PURPOSE_MAPPING = {
    "ai_purpose_marketing_sales_raw": "ai_purpose_marketing_sales",
    "ai_purpose_prod_service_improve_raw": "ai_purpose_prod_service_improve",
    "ai_purpose_biz_process_org_raw": "ai_purpose_biz_process_org",
    "ai_purpose_logistics_raw": "ai_purpose_logistics",
    "ai_purpose_security_raw": "ai_purpose_security",
    "ai_purpose_accounting_finance_raw": "ai_purpose_accounting_finance",
    "ai_purpose_rnd_innovation_raw": "ai_purpose_rnd_innovation",
    "ai_purpose_cost_reduction_raw": "ai_purpose_cost_reduction",
    "ai_purpose_customer_demand_raw": "ai_purpose_customer_demand",
    "ai_purpose_other_raw": "ai_purpose_other",
}

AI_IMPL_MAPPING = {
    "ai_impl_inhouse_dev_raw": "ai_impl_inhouse_dev",
    "ai_impl_modify_commercial_raw": "ai_impl_modify_commercial",
    "ai_impl_modify_open_source_raw": "ai_impl_modify_open_source",
    "ai_impl_buy_commercial_raw": "ai_impl_buy_commercial",
    "ai_impl_vendor_contract_raw": "ai_impl_vendor_contract",
    "ai_impl_other_raw": "ai_impl_other",
}

EFFECT_MAPPING = {
    "effect_proc_improve_raw": "effect_proc_improve",
    "effect_internal_cohesion_raw": "effect_internal_cohesion",
    "effect_decision_improve_raw": "effect_decision_improve",
    "effect_stakeholders_raw": "effect_stakeholders",
    "effect_innov_outcome_raw": "effect_innov_outcome",
    "effect_competitiveness_raw": "effect_competitiveness",
}

TEXT_RAW_COLUMNS = [
    "ai_use_other_text_raw",
    "ai_purpose_other_text_raw",
    "ai_impl_other_text_raw",
]

TEXT_CLEAN_MAPPING = {
    "ai_use_other_text_raw": "ai_use_other_text",
    "ai_purpose_other_text_raw": "ai_purpose_other_text",
    "ai_impl_other_text_raw": "ai_impl_other_text",
}

CLEAN_COLUMN_ORDER = [
    "year",
    "industry",
    "industry_size",
    "firm_size",
    "it_org_any",
    "it_org_internal",
    "it_org_mixed",
    "it_org_outsource",
    "it_org_type",
    "it_invest_any",
    "it_invest_hardware",
    "it_invest_software",
    "it_invest_sys_op",
    "it_invest_infra",
    "it_invest_op_salary",
    "it_invest_new_tech",
    "it_invest_rnd",
    "it_invest_tech_train",
    "it_invest_share",
    "it_invest_share_std4",
    "ai_use",
    "ai_use_doc_info_collect",
    "ai_use_task_automation",
    "ai_use_decision_support",
    "ai_use_speech_to_text",
    "ai_use_gen_summarize_edit",
    "ai_use_image_video_recognition",
    "ai_use_ml_data_analysis",
    "ai_use_text_language_analysis",
    "ai_use_autonomous_mobility",
    "ai_use_other",
    "ai_use_other_text",
    "ai_purpose_marketing_sales",
    "ai_purpose_prod_service_improve",
    "ai_purpose_biz_process_org",
    "ai_purpose_logistics",
    "ai_purpose_security",
    "ai_purpose_accounting_finance",
    "ai_purpose_rnd_innovation",
    "ai_purpose_cost_reduction",
    "ai_purpose_customer_demand",
    "ai_purpose_other",
    "ai_purpose_other_text",
    "ai_impl_inhouse_dev",
    "ai_impl_modify_commercial",
    "ai_impl_modify_open_source",
    "ai_impl_buy_commercial",
    "ai_impl_vendor_contract",
    "ai_impl_other",
    "ai_impl_other_text",
    "effect_proc_improve",
    "effect_internal_cohesion",
    "effect_decision_improve",
    "effect_stakeholders",
    "effect_innov_outcome",
    "effect_competitiveness",
]


def detect_encoding(path: Path) -> str:
    """CSV 파일 인코딩을 후보군에서 탐지합니다."""
    raw_bytes = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp949", "euc-kr", "latin1"):
        try:
            raw_bytes.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeError(f"사용 가능한 인코딩을 찾지 못했습니다: {path}")


def load_csv_safely(path: Path) -> tuple[pd.DataFrame, str]:
    """원본 값을 임의 숫자/결측으로 바꾸지 않도록 문자열로 읽습니다."""
    encoding = detect_encoding(path)
    df = pd.read_csv(
        path,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        low_memory=False,
    )
    return df, encoding


def safe_strip(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """문자열 열의 앞뒤 공백을 제거하고, 공백 문자열 개수를 기록합니다."""
    stripped = df.copy()
    blank_counts = {}
    for column in stripped.columns:
        series = stripped[column].astype("string")
        stripped[column] = series.str.strip()
        blank_counts[column] = int((stripped[column] == "").sum())
    return stripped, blank_counts


def empty_series(index: pd.Index, dtype: str = "Float64") -> pd.Series:
    """없는 입력 변수를 처리할 때 사용할 NA 시리즈를 만듭니다."""
    return pd.Series(pd.NA, index=index, dtype=dtype)


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """쉼표, 공백, % 기호를 제거한 뒤 numeric으로 안전하게 변환합니다."""
    cleaned = (
        series.astype("string")
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
    )
    cleaned = cleaned.mask(cleaned == "", pd.NA)
    return pd.to_numeric(cleaned, errors="coerce")


def clean_binary_from_raw(series: pd.Series) -> pd.Series:
    """상위 yes/no 문항을 1->1, 2->0, 그 외 NA로 변환합니다."""
    numeric = to_numeric_safe(series)
    result = pd.Series(pd.NA, index=series.index, dtype="Int64")
    result.loc[numeric == 1] = 1
    result.loc[numeric == 2] = 0
    return result


def clean_zero_one(series: pd.Series) -> pd.Series:
    """0/1 하위 문항을 numeric 0/1/NA로 변환합니다."""
    numeric = to_numeric_safe(series)
    result = pd.Series(pd.NA, index=series.index, dtype="Int64")
    result.loc[numeric == 1] = 1
    result.loc[numeric == 0] = 0
    return result


def fill_blank_as_zero_when_not_applicable(
    raw_series: pd.Series,
    parent_clean: pd.Series,
) -> tuple[pd.Series, dict[str, int]]:
    """공백을 상위문항 비해당(parent=0)이면 0, 해당(parent=1)이면 NA로 처리합니다."""
    stripped = raw_series.astype("string").str.strip()
    blank_mask = stripped == ""
    result = clean_zero_one(stripped)

    blank_to_zero = blank_mask & (parent_clean == 0)
    blank_to_na_warning = blank_mask & (parent_clean == 1)
    result.loc[blank_to_zero] = 0
    result.loc[blank_to_na_warning] = pd.NA

    stats = {
        "blank_total": int(blank_mask.sum()),
        "blank_to_zero": int(blank_to_zero.sum()),
        "blank_to_na_warning": int(blank_to_na_warning.sum()),
        "invalid_to_na": int((~blank_mask & result.isna()).sum()),
    }
    return result.astype("Int64"), stats


def make_it_org_type(df: pd.DataFrame) -> pd.Series:
    """정보화 조직 유형을 하위 3개 clean 변수로 생성합니다."""
    child_cols = ["it_org_internal", "it_org_mixed", "it_org_outsource"]
    child = df[child_cols]
    result = pd.Series(pd.NA, index=df.index, dtype="Int64")
    complete = child.notna().all(axis=1)
    count_ones = child.sum(axis=1, skipna=False)

    result.loc[complete & (count_ones == 0)] = 0
    result.loc[complete & (df["it_org_internal"] == 1) & (count_ones == 1)] = 1
    result.loc[complete & (df["it_org_mixed"] == 1) & (count_ones == 1)] = 2
    result.loc[complete & (df["it_org_outsource"] == 1) & (count_ones == 1)] = 3
    result.loc[complete & (count_ones >= 2)] = 4
    return result


def cap_std4(series: pd.Series) -> pd.Series:
    """numeric 값을 기준으로 4 초과는 모두 4로 상한 처리합니다."""
    result = series.astype("Float64").copy()
    result.loc[result > 4] = 4
    return result


def clean_text_raw_columns(raw_df: pd.DataFrame) -> pd.DataFrame:
    """기타 텍스트 raw 열의 공백/빈 문자열을 NA로 처리합니다."""
    result = raw_df.copy()
    for column in TEXT_RAW_COLUMNS:
        if column in result.columns:
            result[column] = result[column].astype("string").str.strip().mask(lambda s: s == "", pd.NA)
    return result


def clean_text_from_raw(series: pd.Series) -> pd.Series:
    """텍스트 clean 열을 생성합니다. 공백은 NA, 텍스트는 원문을 유지합니다."""
    stripped = series.astype("string").str.strip()
    return stripped.mask(stripped == "", pd.NA)


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = [markdown_escape(column) for column in df.columns]
    rows = [[markdown_escape(value) for value in row] for row in df.itertuples(index=False, name=None)]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def add_summary_row(
    rows: list[dict[str, str]],
    *,
    variable: str,
    before: str,
    action: str,
    reason: str,
    after: str,
    note: str,
    file_name: str = "nia_2024_cleaned.csv",
) -> None:
    rows.append(
        {
            "파일명": file_name,
            "변수명": variable,
            "처리단계": "clean",
            "처리 전 상태": before,
            "처리 내용": action,
            "처리 이유": reason,
            "처리 후 상태": after,
            "관측치 변화 (N)": "변화 없음",
            "비고": note,
        }
    )


def build_cleaning_summary(
    *,
    blank_zero_stats: dict[str, dict[str, int]],
    text_blank_counts: dict[str, int],
    invest_any_no_variance: bool,
    capped_count: int,
) -> pd.DataFrame:
    """요청 형식의 cleaning summary 표를 생성합니다."""
    rows: list[dict[str, str]] = []

    for raw, clean in CONTROL_MAPPING.items():
        add_summary_row(
            rows,
            variable=clean,
            before="연속형/범주형 숫자 문자열",
            action=f"{raw}를 numeric으로 변환",
            reason="분석용 숫자 변수 생성",
            after="numeric/NA",
            note="통제변수 및 가중치 유지",
        )

    for raw, clean in YESNO_MAPPING.items():
        note = "분산 없음 가능성" if raw == "it_invest_any_raw" and invest_any_no_variance else "1/2 yes-no 변환"
        add_summary_row(
            rows,
            variable=clean,
            before="1/2 응답",
            action=f"{raw}: 1->1, 2->0, 그 외 NA",
            reason="yes/no 문항을 0/1 분석 변수로 변환",
            after="0/1/NA numeric",
            note=note,
        )

    for mapping, parent, label in [
        (IT_ORG_CHILD_MAPPING, "it_org_any_raw", "상위문항 기반 처리"),
        (AI_USE_DETAIL_MAPPING, "ai_use_raw", "상위문항 기반 처리"),
        (AI_PURPOSE_MAPPING, "ai_use_raw", "상위문항 기반 처리"),
        (AI_IMPL_MAPPING, "ai_use_raw", "상위문항 기반 처리"),
    ]:
        for raw, clean in mapping.items():
            stats = blank_zero_stats.get(raw, {})
            add_summary_row(
                rows,
                variable=clean,
                before="0/1/공백 혼재",
                action=f"1->1, 0->0, 공백은 {parent} 비해당이면 0, 해당이면 NA",
                reason="비해당 응답을 결측이 아니라 0으로 해석",
                after="0/1/NA numeric",
                note=f"{label}; 공백->0 {stats.get('blank_to_zero', 0)}건; 공백->NA {stats.get('blank_to_na_warning', 0)}건",
            )

    add_summary_row(
        rows,
        variable="it_org_type",
        before="it_org_internal/mixed/outsource 0/1 조합",
        action="세 하위항목 조합으로 0~4 유형 생성",
        reason="정보화 조직 유형 분석 변수 생성",
        after="0/1/2/3/4/NA numeric",
        note="0=모두 0, 1=internal only, 2=mixed only, 3=outsource only, 4=둘 이상",
    )

    for raw, clean in IT_INVEST_CHILD_MAPPING.items():
        add_summary_row(
            rows,
            variable=clean,
            before="0/1/공백 혼재",
            action=f"{raw}: 1->1, 0->0, 공백/그 외 NA",
            reason="투자 하위항목을 0/1 분석 변수로 변환",
            after="0/1/NA numeric",
            note="공백은 NA",
        )

    add_summary_row(
        rows,
        variable="it_invest_share",
        before="숫자 문자열, 쉼표/공백/% 가능",
        action="쉼표, 공백, % 제거 후 numeric 변환",
        reason="원 raw 값을 그대로 쓰는 투자비중 분석 변수 생성",
        after="numeric/NA",
        note="it_invest_share_pct 생성 안 함",
    )
    add_summary_row(
        rows,
        variable="it_invest_share_std4",
        before="it_invest_share_raw numeric",
        action="1,2,3,4는 유지하고 4 초과 값은 모두 4로 치환",
        reason="4 초과 값을 상한 4로 표준화",
        after="1/2/3/4/NA numeric",
        note=f"4 초과->4 {capped_count}건",
    )

    for raw, clean in EFFECT_MAPPING.items():
        add_summary_row(
            rows,
            variable=clean,
            before="1~5 리커트",
            action=f"{raw}를 1~5 numeric으로 유지",
            reason="midpoint 3을 포함한 순서형 응답 보존",
            after="1~5 numeric",
            note="3은 정상 응답값, 이진화 없음",
        )

    for raw, clean in TEXT_CLEAN_MAPPING.items():
        add_summary_row(
            rows,
            variable=clean,
            before="텍스트+공백",
            action=f"{raw}의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지",
            reason="기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리",
            after="text/NA",
            note=f"clean 텍스트 열 생성; 공백->NA {text_blank_counts.get(raw, 0)}건",
            file_name="nia_2024_cleaned.csv",
        )

    for raw in TEXT_RAW_COLUMNS:
        add_summary_row(
            rows,
            variable=raw,
            before="텍스트+공백",
            action="raw 텍스트 열도 뒤쪽에 보존",
            reason="원천 응답 추적 가능성 유지",
            after="text/NA",
            note="raw 열 보존",
            file_name="nia_2024_cleaned.csv",
        )

    columns = [
        "파일명",
        "변수명",
        "처리단계",
        "처리 전 상태",
        "처리 내용",
        "처리 이유",
        "처리 후 상태",
        "관측치 변화 (N)",
        "비고",
    ]
    return pd.DataFrame(rows, columns=columns)


def write_korean_log(
    *,
    input_shape: tuple[int, int],
    output_shape: tuple[int, int],
    input_encoding: str,
    missing_columns: list[str],
    blank_zero_stats: dict[str, dict[str, int]],
    blank_to_na_vars: dict[str, int],
    text_blank_counts: dict[str, int],
    kept_vars: list[str],
    invest_any_no_variance: bool,
    invest_share_failed: int,
    capped_count: int,
    validation: dict[str, bool],
    warnings: list[str],
) -> None:
    """cleaning 처리 로그를 한글로 작성합니다."""
    blank_zero_lines = [
        f"- {var}: 공백->0 {stats['blank_to_zero']}건"
        for var, stats in blank_zero_stats.items()
        if stats["blank_to_zero"] > 0
    ]
    blank_na_lines = [
        f"- {var}: 공백->NA {count}건"
        for var, count in blank_to_na_vars.items()
        if count > 0
    ]
    text_na_lines = [
        f"- {var}: 텍스트 공백->NA {count}건"
        for var, count in text_blank_counts.items()
    ]

    validation_lines = [
        f"- {key}: {'통과' if value else '실패'}"
        for key, value in validation.items()
    ]

    lines = [
        "NIA 2024 cleaning 처리 로그",
        "",
        "[파일 경로]",
        f"- 입력 파일 경로: {INPUT_PATH}",
        f"- 출력 파일 경로: {OUTPUT_PATH}",
        "",
        "[행/열 수]",
        f"- 입력 행 수: {input_shape[0]}",
        f"- 입력 열 수: {input_shape[1]}",
        f"- 출력 행 수: {output_shape[0]}",
        f"- 출력 열 수: {output_shape[1]}",
        f"- 입력 인코딩: {input_encoding}",
        f"- 출력 인코딩: utf-8",
        "",
        "[변수군별 처리 규칙]",
        "- 정보화 전담 인력: it_org_any_raw는 1->1, 2->0, 그 외 NA. 하위항목 공백은 it_org_any=0이면 0, it_org_any=1이면 NA.",
        "- it_org_type: 내부/겸직/외주 하위항목 조합으로 0~4 생성.",
        "- 정보화 투자: it_invest_any_raw는 1->1, 2->0, 그 외 NA. 하위 투자항목은 1/0 numeric, 공백은 NA.",
        "- AI 이용 여부: ai_use_raw는 1->1, 2->0, 그 외 NA.",
        "- AI 세부유형/목적/형태: 공백은 ai_use=0이면 0, ai_use=1이면 NA.",
        "- 기타 텍스트: 공백/빈 문자열은 NA, 텍스트는 유지. *_other_text clean 열을 생성하고 *_other_text_raw도 뒤쪽에 보존.",
        "- 효과 변수: 1,2,3,4,5를 numeric으로 유지. midpoint 3은 정상 응답값이며 결측 처리하지 않음.",
        "- 통제변수: year, industry, industry_size, firm_size는 numeric 유지.",
        "- 가중치: weight clean 변수는 생성하지 않고 weight_raw를 raw 열로만 보존.",
        "",
        "[공백 -> 0 처리한 변수들]",
        "\n".join(blank_zero_lines) if blank_zero_lines else "- 없음",
        "",
        "[공백 -> NA 처리한 변수들]",
        "\n".join(blank_na_lines + text_na_lines) if blank_na_lines or text_na_lines else "- 없음",
        "",
        "[그대로 유지한 변수들]",
        "\n".join(f"- {var}" for var in kept_vars),
        "",
        "[it_invest_share 처리 규칙]",
        "- it_invest_share_raw에서 쉼표, 공백, % 기호를 제거한 뒤 numeric으로 변환.",
        "- 변환된 numeric 값을 it_invest_share로 그대로 사용.",
        f"- 변환 실패로 NA 처리된 건수: {invest_share_failed}",
        "- it_invest_share_pct 열은 생성하지 않음.",
        "",
        "[it_invest_share_std4 처리 규칙]",
        "- it_invest_share_raw를 numeric으로 변환한 값을 기준으로 생성.",
        "- 값이 1,2,3,4이면 그대로 유지.",
        "- 값이 4 초과이면 모두 4로 치환.",
        "- 값이 결측이면 결측 유지.",
        f"- 4 초과 값을 4로 치환한 건수: {capped_count}",
        "",
        "[이상치/경고]",
        "\n".join(f"- {warning}" for warning in warnings) if warnings else "- 없음",
        "- it_invest_any_raw는 모든 관측치가 1만 존재하여 분산 없음 가능성이 있습니다." if invest_any_no_variance else "- it_invest_any_raw 분산 없음 가능성은 발견되지 않았습니다.",
        "- 누락된 입력 열: " + (", ".join(missing_columns) if missing_columns else "없음"),
        "",
        "[검증 결과]",
        "\n".join(validation_lines),
        f"- row 수 변화 없음 확인: {'통과' if validation['row_count_same'] else '실패'}",
    ]

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_df, input_encoding = load_csv_safely(INPUT_PATH)
    stripped_df, blank_counts = safe_strip(input_df)
    missing_columns = []
    clean_df = pd.DataFrame(index=stripped_df.index)

    all_needed_columns = (
        list(CONTROL_MAPPING)
        + list(YESNO_MAPPING)
        + list(IT_ORG_CHILD_MAPPING)
        + list(IT_INVEST_CHILD_MAPPING)
        + ["it_invest_share_raw"]
        + list(AI_USE_DETAIL_MAPPING)
        + list(AI_PURPOSE_MAPPING)
        + list(AI_IMPL_MAPPING)
        + list(EFFECT_MAPPING)
        + list(TEXT_CLEAN_MAPPING)
    )
    missing_columns = [column for column in all_needed_columns if column not in stripped_df.columns]

    for raw, clean in CONTROL_MAPPING.items():
        clean_df[clean] = to_numeric_safe(stripped_df[raw]) if raw in stripped_df.columns else empty_series(stripped_df.index)

    for raw, clean in YESNO_MAPPING.items():
        clean_df[clean] = clean_binary_from_raw(stripped_df[raw]) if raw in stripped_df.columns else empty_series(stripped_df.index, "Int64")

    blank_zero_stats: dict[str, dict[str, int]] = {}
    blank_to_na_vars: dict[str, int] = {}

    for raw, clean in IT_ORG_CHILD_MAPPING.items():
        if raw in stripped_df.columns:
            clean_df[clean], stats = fill_blank_as_zero_when_not_applicable(stripped_df[raw], clean_df["it_org_any"])
            blank_zero_stats[raw] = stats
            blank_to_na_vars[raw] = stats["blank_to_na_warning"]
        else:
            clean_df[clean] = empty_series(stripped_df.index, "Int64")

    clean_df["it_org_type"] = make_it_org_type(clean_df)

    for raw, clean in IT_INVEST_CHILD_MAPPING.items():
        clean_df[clean] = clean_zero_one(stripped_df[raw]) if raw in stripped_df.columns else empty_series(stripped_df.index, "Int64")

    invest_share_numeric = (
        to_numeric_safe(stripped_df["it_invest_share_raw"])
        if "it_invest_share_raw" in stripped_df.columns
        else empty_series(stripped_df.index)
    )
    clean_df["it_invest_share"] = invest_share_numeric.astype("Float64")
    clean_df["it_invest_share_std4"] = cap_std4(invest_share_numeric)

    for mapping in [AI_USE_DETAIL_MAPPING, AI_PURPOSE_MAPPING, AI_IMPL_MAPPING]:
        for raw, clean in mapping.items():
            if raw in stripped_df.columns:
                clean_df[clean], stats = fill_blank_as_zero_when_not_applicable(stripped_df[raw], clean_df["ai_use"])
                blank_zero_stats[raw] = stats
                blank_to_na_vars[raw] = stats["blank_to_na_warning"]
            else:
                clean_df[clean] = empty_series(stripped_df.index, "Int64")

    for raw, clean in TEXT_CLEAN_MAPPING.items():
        clean_df[clean] = clean_text_from_raw(stripped_df[raw]) if raw in stripped_df.columns else empty_series(stripped_df.index, "string")

    for raw, clean in EFFECT_MAPPING.items():
        clean_df[clean] = to_numeric_safe(stripped_df[raw]).astype("Int64") if raw in stripped_df.columns else empty_series(stripped_df.index, "Int64")

    clean_df = clean_df.loc[:, CLEAN_COLUMN_ORDER]

    raw_column_order = [column for column in stripped_df.columns if column.endswith("_raw")]
    raw_df = clean_text_raw_columns(stripped_df.loc[:, raw_column_order])
    output_df = pd.concat([clean_df, raw_df], axis=1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    output_check = pd.read_csv(
        OUTPUT_PATH,
        encoding="utf-8",
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        low_memory=False,
    )

    text_blank_counts = {column: blank_counts.get(column, 0) for column in TEXT_RAW_COLUMNS if column in stripped_df.columns}
    raw_it_invest_any_values = set(stripped_df["it_invest_any_raw"].dropna().unique()) if "it_invest_any_raw" in stripped_df.columns else set()
    invest_any_no_variance = raw_it_invest_any_values == {"1"}
    invest_share_failed = int((stripped_df.get("it_invest_share_raw", pd.Series("", index=stripped_df.index)).astype("string").str.strip() != "").sum() - clean_df["it_invest_share"].notna().sum())
    capped_count = int((invest_share_numeric > 4).sum())

    warnings = []
    for var, count in blank_to_na_vars.items():
        if count > 0:
            warnings.append(f"{var}: 상위문항이 해당(1)인데 공백인 값 {count}건은 NA로 유지했습니다.")
    if missing_columns:
        warnings.append("일부 입력 열이 없어 해당 clean 변수는 NA로 생성했습니다.")
    if invest_any_no_variance:
        warnings.append("it_invest_any_raw가 모두 1로만 존재합니다.")

    raw_columns_preserved = output_df.columns.tolist()[len(CLEAN_COLUMN_ORDER):] == raw_column_order
    validation = {
        "row_count_same": len(output_df) == len(input_df),
        "it_org_any_zero_children_zero_or_valid": bool(
            clean_df.loc[clean_df["it_org_any"] == 0, ["it_org_internal", "it_org_mixed", "it_org_outsource"]]
            .isin([0])
            .all()
            .all()
        ),
        "ai_use_zero_blanks_to_zero": all(
            stats["blank_to_zero"] == stats["blank_total"]
            for var, stats in blank_zero_stats.items()
            if var.startswith("ai_") and stats["blank_total"] > 0
        ),
        "text_blanks_to_na": all(raw_df[column].isna().sum() == blank_counts.get(column, 0) for column in TEXT_RAW_COLUMNS if column in raw_df.columns),
        "clean_text_columns_created": all(clean in output_df.columns for clean in TEXT_CLEAN_MAPPING.values()),
        "clean_text_blanks_to_na": all(clean_df[clean].isna().sum() == blank_counts.get(raw, 0) for raw, clean in TEXT_CLEAN_MAPPING.items() if clean in clean_df.columns),
        "effect_values_1_to_5": all(clean_df[clean].dropna().isin([1, 2, 3, 4, 5]).all() for clean in EFFECT_MAPPING.values()),
        "it_invest_share_numeric": pd.api.types.is_numeric_dtype(clean_df["it_invest_share"]),
        "it_invest_share_std4_valid": clean_df["it_invest_share_std4"].dropna().isin([1, 2, 3, 4]).all(),
        "it_invest_share_std4_cap_applied": bool((clean_df.loc[invest_share_numeric > 4, "it_invest_share_std4"] == 4).all()),
        "no_it_invest_share_pct": "it_invest_share_pct" not in output_df.columns,
        "raw_columns_preserved_after_clean": raw_columns_preserved,
        "output_utf8_readable": len(output_check.columns) == len(output_df.columns),
    }

    kept_vars = list(EFFECT_MAPPING.values()) + ["year", "industry", "industry_size", "firm_size", "weight_raw"]
    write_korean_log(
        input_shape=input_df.shape,
        output_shape=output_df.shape,
        input_encoding=input_encoding,
        missing_columns=missing_columns,
        blank_zero_stats=blank_zero_stats,
        blank_to_na_vars=blank_to_na_vars,
        text_blank_counts=text_blank_counts,
        kept_vars=kept_vars,
        invest_any_no_variance=invest_any_no_variance,
        invest_share_failed=invest_share_failed,
        capped_count=capped_count,
        validation=validation,
        warnings=warnings,
    )

    summary_df = build_cleaning_summary(
        blank_zero_stats=blank_zero_stats,
        text_blank_counts=text_blank_counts,
        invest_any_no_variance=invest_any_no_variance,
        capped_count=capped_count,
    )
    summary_markdown = dataframe_to_markdown(summary_df)
    SUMMARY_PATH.write_text(summary_markdown + "\n", encoding="utf-8")

    print(f"cleaned 파일 생성 완료: {OUTPUT_PATH}")
    print(f"로그 파일 생성 완료: {LOG_PATH}")
    print(f"요약표 생성 완료: {SUMMARY_PATH}")
    print(f"입력 행 수: {len(input_df)}, 출력 행 수: {len(output_df)}")
    print(f"입력 열 수: {input_df.shape[1]}, 출력 열 수: {output_df.shape[1]}")
    print("")
    print(summary_markdown)


if __name__ == "__main__":
    main()
