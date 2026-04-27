#!/usr/bin/env python3
"""NIA 2024 cleaned 파일에 연구용 파생변수를 추가해 featured 파일을 만듭니다.

주의:
- 입력 cleaned 파일은 수정하지 않습니다.
- 기존 열은 유지하고, 파생변수 7개를 연관 변수 주변에 배치합니다.
- 단, 입력 파일에 같은 이름의 파생변수가 이미 있으면 중복 열을 만들지 않고
  규칙대로 다시 계산한 열을 지정 위치에 배치합니다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "working" / "cleaned" / "nia_2024_cleaned.csv"
OUTPUT_PATH = BASE_DIR / "working" / "featured" / "nia_2024_featured.csv"
LOG_PATH = BASE_DIR / "working" / "featured" / "feature_engineering_log_2024.txt"
SUMMARY_PATH = BASE_DIR / "working" / "featured" / "feature_engineering_summary_2024.md"

FEATURE_COLUMNS = [
    "it_org_type",
    "it_invest_sum",
    "it_invest_high",
    "ai_use_sum",
    "ai_impl_sum",
    "ai_purpose_sum",
    "effect_average",
]

FEATURE_PLACEMENT = {
    "it_org_type": {"anchor": "it_org_any", "where": "after"},
    "it_invest_sum": {"anchor": "it_invest_any", "where": "after"},
    "it_invest_high": {"anchor": "it_invest_share_std4", "where": "after"},
    "ai_use_sum": {"anchor": "ai_use", "where": "after"},
    "ai_impl_sum": {"anchor": "ai_impl_inhouse_dev_raw", "where": "before"},
    "ai_purpose_sum": {"anchor": "ai_purpose_marketing_sales", "where": "before"},
    "effect_average": {"anchor": "effect_competitiveness", "where": "after"},
}

IT_ORG_COMPONENTS = ["it_org_internal", "it_org_mixed", "it_org_outsource"]
IT_INVEST_COMPONENTS = [
    "it_invest_hardware",
    "it_invest_software",
    "it_invest_sys_op",
    "it_invest_infra",
    "it_invest_op_salary",
    "it_invest_new_tech",
    "it_invest_rnd",
    "it_invest_tech_train",
]
AI_USE_COMPONENTS = [
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
]
AI_IMPL_COMPONENTS = [
    "ai_impl_inhouse_dev",
    "ai_impl_modify_commercial",
    "ai_impl_modify_open_source",
    "ai_impl_buy_commercial",
    "ai_impl_vendor_contract",
    "ai_impl_other",
]
AI_PURPOSE_COMPONENTS = [
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
]
EFFECT_COMPONENTS = [
    "effect_proc_improve",
    "effect_innov_outcome",
    "effect_decision_improve",
    "effect_internal_cohesion",
    "effect_stakeholders",
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
    """원본 값을 임의 결측/숫자로 바꾸지 않도록 문자열로 읽습니다."""
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


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """문자열 숫자를 안전하게 numeric으로 변환합니다."""
    cleaned = (
        series.astype("string")
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
    )
    cleaned = cleaned.mask(cleaned == "", pd.NA)
    return pd.to_numeric(cleaned, errors="coerce")


def numeric_frame(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """여러 입력 열을 numeric DataFrame으로 변환합니다. 없는 열은 NA로 만듭니다."""
    result = pd.DataFrame(index=df.index)
    for column in columns:
        if column in df.columns:
            result[column] = to_numeric_safe(df[column])
        else:
            result[column] = pd.NA
    return result


def make_it_org_type(df: pd.DataFrame) -> pd.Series:
    """정보화 조직 유형을 세 하위 이진 변수 조합으로 생성합니다."""
    components = numeric_frame(df, IT_ORG_COMPONENTS)
    complete = components.notna().all(axis=1)
    count_ones = (components == 1).sum(axis=1)
    all_zero = (components == 0).all(axis=1)

    result = pd.Series(pd.NA, index=df.index, dtype="Int64")
    result.loc[complete & all_zero] = 0
    result.loc[complete & (count_ones >= 2)] = 4
    result.loc[complete & (count_ones == 1) & (components["it_org_internal"] == 1)] = 1
    result.loc[complete & (count_ones == 1) & (components["it_org_mixed"] == 1)] = 2
    result.loc[complete & (count_ones == 1) & (components["it_org_outsource"] == 1)] = 3
    return result


def safe_row_sum(df: pd.DataFrame, columns: list[str]) -> tuple[pd.Series, int]:
    """모든 구성 변수가 존재할 때만 행별 합계를 계산합니다."""
    values = numeric_frame(df, columns)
    missing_rows = values.isna().any(axis=1)
    result = values.sum(axis=1).astype("Int64")
    result.loc[missing_rows] = pd.NA
    return result, int(missing_rows.sum())


def safe_row_mean(df: pd.DataFrame, columns: list[str]) -> tuple[pd.Series, int]:
    """모든 구성 변수가 존재할 때만 행별 평균을 계산합니다."""
    values = numeric_frame(df, columns)
    missing_rows = values.isna().any(axis=1)
    result = values.mean(axis=1).astype("Float64")
    result.loc[missing_rows] = pd.NA
    return result, int(missing_rows.sum())


def make_it_invest_high(df: pd.DataFrame) -> tuple[pd.Series, int]:
    """it_invest_share 기준으로 high 투자 여부를 생성합니다."""
    share = to_numeric_safe(df["it_invest_share"]) if "it_invest_share" in df.columns else pd.Series(pd.NA, index=df.index)
    result = pd.Series(pd.NA, index=df.index, dtype="Int64")
    result.loc[share <= 3] = 0
    result.loc[share >= 4] = 1
    ambiguous = share.notna() & (share > 3) & (share < 4)
    return result, int(ambiguous.sum())


def compare_existing_feature(df: pd.DataFrame, feature_name: str, new_series: pd.Series) -> str:
    """이미 존재하는 파생변수와 새 계산 결과가 같은지 비교합니다."""
    if feature_name not in df.columns:
        return "기존 열 없음"
    old = to_numeric_safe(df[feature_name])
    new = pd.to_numeric(new_series, errors="coerce")
    same = old.fillna(-999999999).equals(new.fillna(-999999999))
    return "기존 열과 재계산 결과 일치" if same else "기존 열과 재계산 결과 불일치"


def validate_feature_ranges(feature_df: pd.DataFrame, input_rows: int, output_rows: int) -> dict[str, bool]:
    """파생변수 값 범위와 row 수를 검증합니다."""
    validations = {
        "row_count_same": input_rows == output_rows,
        "it_org_type_valid": feature_df["it_org_type"].dropna().isin([0, 1, 2, 3, 4]).all(),
        "it_invest_sum_range": feature_df["it_invest_sum"].dropna().between(0, 8).all(),
        "it_invest_high_valid": feature_df["it_invest_high"].dropna().isin([0, 1]).all(),
        "ai_use_sum_range": feature_df["ai_use_sum"].dropna().between(0, 10).all(),
        "ai_impl_sum_range": feature_df["ai_impl_sum"].dropna().between(0, 6).all(),
        "ai_purpose_sum_range": feature_df["ai_purpose_sum"].dropna().between(0, 10).all(),
        "effect_average_range": feature_df["effect_average"].dropna().between(1, 5).all(),
    }
    return {key: bool(value) for key, value in validations.items()}


def place_feature_columns(
    df: pd.DataFrame,
    feature_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, str]]:
    """파생변수를 지정된 앵커 열 주변에 배치합니다."""
    base_df = df.drop(columns=[column for column in FEATURE_COLUMNS if column in df.columns])
    before_map: dict[str, list[str]] = {}
    after_map: dict[str, list[str]] = {}
    placement_notes: dict[str, str] = {}

    for feature in FEATURE_COLUMNS:
        placement = FEATURE_PLACEMENT[feature]
        anchor = placement["anchor"]
        where = placement["where"]
        target_map = before_map if where == "before" else after_map
        target_map.setdefault(anchor, []).append(feature)

    output_parts: list[pd.DataFrame] = []
    placed: set[str] = set()

    for column in base_df.columns:
        for feature in before_map.get(column, []):
            output_parts.append(feature_df[[feature]])
            placed.add(feature)
            placement_notes[feature] = f"{column} 좌측에 배치"

        output_parts.append(base_df[[column]])

        for feature in after_map.get(column, []):
            output_parts.append(feature_df[[feature]])
            placed.add(feature)
            placement_notes[feature] = f"{column} 우측에 배치"

    unplaced_features = [feature for feature in FEATURE_COLUMNS if feature not in placed]
    for feature in unplaced_features:
        output_parts.append(feature_df[[feature]])
        anchor = FEATURE_PLACEMENT[feature]["anchor"]
        placement_notes[feature] = f"앵커 열 {anchor} 없음: 파일 맨 뒤에 배치"

    return pd.concat(output_parts, axis=1), placement_notes


def validate_feature_positions(output_df: pd.DataFrame) -> dict[str, bool]:
    """요청한 파생변수 위치가 맞는지 검증합니다."""
    cols = output_df.columns.tolist()

    def right_of(feature: str, anchor: str) -> bool:
        return feature in cols and anchor in cols and cols.index(feature) == cols.index(anchor) + 1

    def left_of(feature: str, anchor: str) -> bool:
        return feature in cols and anchor in cols and cols.index(feature) + 1 == cols.index(anchor)

    return {
        "it_org_type_right_of_it_org_any": right_of("it_org_type", "it_org_any"),
        "it_invest_sum_right_of_it_invest_any": right_of("it_invest_sum", "it_invest_any"),
        "it_invest_high_right_of_it_invest_share_std4": right_of("it_invest_high", "it_invest_share_std4"),
        "ai_use_sum_right_of_ai_use": right_of("ai_use_sum", "ai_use"),
        "ai_impl_sum_left_of_ai_impl_inhouse_dev_raw": left_of("ai_impl_sum", "ai_impl_inhouse_dev_raw"),
        "ai_purpose_sum_left_of_ai_purpose_marketing_sales": left_of("ai_purpose_sum", "ai_purpose_marketing_sales"),
        "effect_average_right_of_effect_competitiveness": right_of("effect_average", "effect_competitiveness"),
    }


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


def build_feature_summary(missing_counts: dict[str, int], existing_notes: dict[str, str]) -> pd.DataFrame:
    """요청 형식의 feature engineering summary 표를 생성합니다."""
    rows = [
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "it_org_type",
            "처리단계": "feature engineering",
            "처리 전 상태": "원천 변수 3개 조합",
            "처리 내용": "규칙 기반 범주 변수 생성",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "0~4 범주형",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": existing_notes.get("it_org_type", "2개 이상 1이면 4 우선"),
        },
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "it_invest_sum",
            "처리단계": "feature engineering",
            "처리 전 상태": "0/1 더미 8개",
            "처리 내용": "8개 투자항목 합계 변수 생성",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "0~8 정수",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": f"하나라도 결측이면 NA; 결측 처리 {missing_counts['it_invest_sum']}건",
        },
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "it_invest_high",
            "처리단계": "feature engineering",
            "처리 전 상태": "it_invest_share numeric",
            "처리 내용": "it_invest_share<=3이면 0, >=4이면 1",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "0/1/NA",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": "it_invest_share_std4 사용 안 함",
        },
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "ai_use_sum",
            "처리단계": "feature engineering",
            "처리 전 상태": "0/1 더미 10개",
            "처리 내용": "10개 AI 이용유형 합계 변수 생성",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "0~10 정수",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": f"하나라도 결측이면 NA; 결측 처리 {missing_counts['ai_use_sum']}건",
        },
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "ai_impl_sum",
            "처리단계": "feature engineering",
            "처리 전 상태": "0/1 더미 6개",
            "처리 내용": "6개 AI 이용형태 합계 변수 생성",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "0~6 정수",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": f"하나라도 결측이면 NA; 결측 처리 {missing_counts['ai_impl_sum']}건",
        },
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "ai_purpose_sum",
            "처리단계": "feature engineering",
            "처리 전 상태": "0/1 더미 10개",
            "처리 내용": "10개 AI 이용목적 합계 변수 생성",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "0~10 정수",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": f"하나라도 결측이면 NA; 결측 처리 {missing_counts['ai_purpose_sum']}건",
        },
        {
            "파일명": "nia_2024_featured.csv",
            "변수명": "effect_average",
            "처리단계": "feature engineering",
            "처리 전 상태": "1~5 리커트 6개",
            "처리 내용": "6개 효과 변수 평균 생성",
            "처리 이유": "연구용 파생변수 추가",
            "처리 후 상태": "1~5 평균값",
            "관측치 변화 (N)": "row 수 변화 없음",
            "비고": f"소수점 반올림 없음; 결측 처리 {missing_counts['effect_average']}건",
        },
    ]
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
    missing_counts: dict[str, int],
    existing_notes: dict[str, str],
    placement_notes: dict[str, str],
    ambiguous_invest_high: int,
    validations: dict[str, bool],
    warnings: list[str],
) -> None:
    """feature engineering 결과 로그를 한글로 작성합니다."""
    validation_lines = [f"- {key}: {'통과' if value else '실패'}" for key, value in validations.items()]
    lines = [
        "NIA 2024 feature engineering 로그",
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
        "[생성한 파생변수 목록]",
        "\n".join(f"- {column}" for column in FEATURE_COLUMNS),
        "",
        "[각 파생변수 생성 규칙]",
        "- it_org_type: internal/mixed/outsource 세 변수를 조합. 2개 이상 1이면 4를 최우선 적용, 모두 0이면 0.",
        "- it_invest_sum: 투자 하위항목 8개가 모두 존재할 때만 합계 계산.",
        "- it_invest_high: it_invest_share <= 3이면 0, it_invest_share >= 4이면 1. it_invest_share_std4는 사용하지 않음.",
        "- ai_use_sum: AI 이용 세부유형 10개가 모두 존재할 때만 합계 계산.",
        "- ai_impl_sum: AI 이용형태 6개가 모두 존재할 때만 합계 계산.",
        "- ai_purpose_sum: AI 이용목적 10개가 모두 존재할 때만 합계 계산.",
        "- effect_average: 효과 변수 6개가 모두 존재할 때만 평균 계산. 반올림하지 않음.",
        "",
        "[결측 처리 규칙]",
        "- 파생변수 계산에 필요한 입력값 중 하나라도 결측이면 해당 파생변수는 NA로 둠.",
        "- it_org_type은 세 이진변수 조합으로 계산하되, 세 값 중 필요한 값이 결측이면 NA.",
        f"- it_invest_sum 결측 처리 건수: {missing_counts['it_invest_sum']}",
        f"- ai_use_sum 결측 처리 건수: {missing_counts['ai_use_sum']}",
        f"- ai_impl_sum 결측 처리 건수: {missing_counts['ai_impl_sum']}",
        f"- ai_purpose_sum 결측 처리 건수: {missing_counts['ai_purpose_sum']}",
        f"- effect_average 결측 처리 건수: {missing_counts['effect_average']}",
        f"- it_invest_high에서 3초과 4미만이라 규칙상 NA 처리된 건수: {ambiguous_invest_high}",
        "",
        "[기존 동일 이름 파생변수 처리]",
        "\n".join(f"- {name}: {note}" for name, note in existing_notes.items()) if existing_notes else "- 없음",
        "",
        "[파생변수 배치]",
        "\n".join(f"- {name}: {note}" for name, note in placement_notes.items()),
        "",
        "[값 범위 검증 결과]",
        "\n".join(validation_lines),
        "",
        "[특이사항 / 경고사항]",
        "\n".join(f"- {warning}" for warning in warnings) if warnings else "- 없음",
    ]
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    df, input_encoding = load_csv_safely(INPUT_PATH)

    feature_df = pd.DataFrame(index=df.index)
    feature_df["it_org_type"] = make_it_org_type(df)
    feature_df["it_invest_sum"], invest_missing = safe_row_sum(df, IT_INVEST_COMPONENTS)
    feature_df["it_invest_high"], ambiguous_invest_high = make_it_invest_high(df)
    feature_df["ai_use_sum"], ai_use_missing = safe_row_sum(df, AI_USE_COMPONENTS)
    feature_df["ai_impl_sum"], ai_impl_missing = safe_row_sum(df, AI_IMPL_COMPONENTS)
    feature_df["ai_purpose_sum"], ai_purpose_missing = safe_row_sum(df, AI_PURPOSE_COMPONENTS)
    feature_df["effect_average"], effect_missing = safe_row_mean(df, EFFECT_COMPONENTS)

    missing_counts = {
        "it_invest_sum": invest_missing,
        "ai_use_sum": ai_use_missing,
        "ai_impl_sum": ai_impl_missing,
        "ai_purpose_sum": ai_purpose_missing,
        "effect_average": effect_missing,
    }
    existing_notes = {
        column: compare_existing_feature(df, column, feature_df[column])
        for column in FEATURE_COLUMNS
        if column in df.columns
    }

    # 같은 이름의 파생변수가 이미 있으면 기존 위치에서는 제거하고 지정 위치에 재배치합니다.
    output_df, placement_notes = place_feature_columns(df, feature_df.loc[:, FEATURE_COLUMNS])

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

    validations = validate_feature_ranges(feature_df, len(df), len(output_df))
    validations["all_existing_columns_preserved_except_feature_reposition"] = all(
        column in output_df.columns for column in df.columns if column not in FEATURE_COLUMNS
    )
    validations.update(validate_feature_positions(output_df))
    validations["output_utf8_readable"] = len(output_check.columns) == len(output_df.columns)

    warnings = []
    for feature, count in missing_counts.items():
        if count > 0:
            warnings.append(f"{feature}: 구성 변수 중 결측이 있어 {count}건을 NA로 처리했습니다.")
    if ambiguous_invest_high > 0:
        warnings.append(f"it_invest_high: it_invest_share가 3초과 4미만인 {ambiguous_invest_high}건은 명시 규칙 밖이라 NA로 처리했습니다.")
    for feature, note in existing_notes.items():
        warnings.append(f"{feature}: 입력 파일에 이미 존재하여 재계산 후 지정 위치로 재배치했습니다. {note}.")

    write_korean_log(
        input_shape=df.shape,
        output_shape=output_df.shape,
        input_encoding=input_encoding,
        missing_counts=missing_counts,
        existing_notes=existing_notes,
        placement_notes=placement_notes,
        ambiguous_invest_high=ambiguous_invest_high,
        validations=validations,
        warnings=warnings,
    )

    summary_df = build_feature_summary(missing_counts, existing_notes)
    summary_markdown = dataframe_to_markdown(summary_df)
    SUMMARY_PATH.write_text(summary_markdown + "\n", encoding="utf-8")

    print(f"featured 파일 생성 완료: {OUTPUT_PATH}")
    print(f"로그 파일 생성 완료: {LOG_PATH}")
    print(f"요약표 생성 완료: {SUMMARY_PATH}")
    print(f"입력 행 수: {len(df)}, 출력 행 수: {len(output_df)}")
    print(f"입력 열 수: {df.shape[1]}, 출력 열 수: {output_df.shape[1]}")
    print("")
    print(summary_markdown)


if __name__ == "__main__":
    main()
