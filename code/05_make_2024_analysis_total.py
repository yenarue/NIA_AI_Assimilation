#!/usr/bin/env python3
"""NIA 2024 cleaned 파일에서 분석용 total 데이터셋을 생성합니다.

주의:
- 입력 cleaned 파일은 수정하지 않습니다.
- 새 파생변수는 만들지 않습니다.
- cleaned 파일에 실제로 존재하는 변수만 사용합니다.
- 제외 규칙에 따라 raw/text/불필요 변수를 제거하고 열 순서만 정리합니다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "working" / "featured" / "nia_2024_featured.csv"
OUTPUT_PATH = BASE_DIR / "working" / "analysis" / "nia_2024_analysis_total.csv"
LOG_PATH = BASE_DIR / "working" / "analysis" / "analysis_total_log_2024.txt"
SUMMARY_PATH = BASE_DIR / "working" / "analysis" / "analysis_total_summary_2024.md"

EXACT_EXCLUDE = {"it_invest_any"}

EXPECTED_ORDER = [
    "year",
    "industry",
    "industry_size",
    "firm_size",
    "it_org_any",
    "it_org_internal",
    "it_org_mixed",
    "it_org_outsource",
    "it_org_type",
    "it_invest_sum",
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
    "it_invest_high",
    "ai_use",
    "ai_use_sum",
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
    "ai_impl_sum",
    "ai_impl_inhouse_dev",
    "ai_impl_modify_commercial",
    "ai_impl_modify_open_source",
    "ai_impl_buy_commercial",
    "ai_impl_vendor_contract",
    "ai_impl_other",
    "ai_purpose_sum",
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
    "effect_proc_improve",
    "effect_internal_cohesion",
    "effect_decision_improve",
    "effect_stakeholders",
    "effect_innov_outcome",
    "effect_competitiveness",
    "effect_average",
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
    """값을 임의 변환하지 않도록 문자열로 읽습니다."""
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


def exclusion_reason(column: str) -> str | None:
    """제외 규칙에 걸리는지와 그 사유를 반환합니다."""
    if column in EXACT_EXCLUDE:
        return "정확히 제외할 변수"
    if column.endswith("_raw"):
        return "이름이 _raw로 끝나는 변수"
    if column.endswith("_other_text"):
        return "이름이 _other_text로 끝나는 변수"
    return None


def drop_excluded_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """제외 규칙을 적용해 analysis_total에 포함할 열만 남깁니다."""
    removed = {
        column: reason
        for column in df.columns
        if (reason := exclusion_reason(column)) is not None
    }
    kept_columns = [column for column in df.columns if column not in removed]
    return df.loc[:, kept_columns].copy(), removed


def reorder_analysis_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """기대 순서에 있는 열을 앞에 놓고 나머지 clean 변수는 뒤에 유지합니다."""
    ordered_front = [column for column in EXPECTED_ORDER if column in df.columns]
    remaining = [column for column in df.columns if column not in ordered_front]
    return df.loc[:, ordered_front + remaining], [column for column in EXPECTED_ORDER if column not in df.columns]


def validate_analysis_total(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    removed_columns: dict[str, str],
) -> dict[str, bool]:
    """analysis_total 생성 결과를 검증합니다."""
    output_columns = output_df.columns.tolist()
    return {
        "row_count_same": len(input_df) == len(output_df),
        "it_invest_any_removed": "it_invest_any" not in output_columns,
        "raw_columns_removed": not any(column.endswith("_raw") for column in output_columns),
        "other_text_columns_removed": not any(column.endswith("_other_text") for column in output_columns),
        "removed_columns_absent": all(column not in output_columns for column in removed_columns),
        "no_duplicate_columns": not output_df.columns.duplicated().any(),
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


def build_analysis_summary(
    *,
    removed_columns: dict[str, str],
    kept_core_columns: list[str],
    missing_expected_columns: list[str],
) -> pd.DataFrame:
    """요청 형식의 analysis_total summary 표를 생성합니다."""
    rows: list[dict[str, str]] = []

    for column, reason in removed_columns.items():
        before = "raw 변수 존재" if column.endswith("_raw") else "text 변수 존재" if column.endswith("_other_text") else "clean 변수 존재"
        rows.append(
            {
                "파일명": "nia_2024_cleaned.csv",
                "변수명": column,
                "처리단계": "analysis_total",
                "처리 전 상태": before,
                "처리 내용": "제외",
                "처리 이유": "분석용 total 파일 구성",
                "처리 후 상태": "제거됨",
                "관측치 변화 (N)": "row 수 변화 없음",
                "비고": reason,
            }
        )

    for column in kept_core_columns:
        rows.append(
            {
                "파일명": "nia_2024_analysis_total.csv",
                "변수명": column,
                "처리단계": "analysis_total",
                "처리 전 상태": "clean 변수 존재",
                "처리 내용": "유지 및 열 순서 재정렬",
                "처리 이유": "분석용 total 파일 구성",
                "처리 후 상태": "유지됨",
                "관측치 변화 (N)": "row 수 변화 없음",
                "비고": "핵심 분석 변수",
            }
        )

    for column in missing_expected_columns:
        rows.append(
            {
                "파일명": "nia_2024_cleaned.csv",
                "변수명": column,
                "처리단계": "analysis_total",
                "처리 전 상태": "입력 파일에 없음",
                "처리 내용": "건너뜀",
                "처리 이유": "새 파생변수 생성 금지",
                "처리 후 상태": "미포함",
                "관측치 변화 (N)": "row 수 변화 없음",
                "비고": "기대 변수지만 cleaned 파일에 없음",
            }
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
    removed_columns: dict[str, str],
    kept_core_columns: list[str],
    missing_expected_columns: list[str],
    validations: dict[str, bool],
    warnings: list[str],
) -> None:
    """analysis_total 처리 로그를 한글로 저장합니다."""
    validation_lines = [f"- {key}: {'통과' if value else '실패'}" for key, value in validations.items()]
    removed_lines = [f"- {column}: {reason}" for column, reason in removed_columns.items()]

    lines = [
        "NIA 2024 analysis_total 생성 로그",
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
        "[제거한 변수 목록]",
        "\n".join(removed_lines) if removed_lines else "- 없음",
        "",
        "[유지한 핵심 변수 목록]",
        "\n".join(f"- {column}" for column in kept_core_columns) if kept_core_columns else "- 없음",
        "",
        "[제외 규칙 적용 결과]",
        f"- 정확히 제외한 변수 수: {sum(reason == '정확히 제외할 변수' for reason in removed_columns.values())}",
        f"- _raw 패턴 제외 변수 수: {sum(reason == '이름이 _raw로 끝나는 변수' for reason in removed_columns.values())}",
        f"- _other_text 패턴 제외 변수 수: {sum(reason == '이름이 _other_text로 끝나는 변수' for reason in removed_columns.values())}",
        "",
        "[기대 변수 중 입력 파일에 없어 건너뛴 변수]",
        "\n".join(f"- {column}" for column in missing_expected_columns) if missing_expected_columns else "- 없음",
        "",
        "[검증 결과]",
        "\n".join(validation_lines),
        "",
        "[특이사항 / 경고사항]",
        "\n".join(f"- {warning}" for warning in warnings) if warnings else "- 없음",
    ]
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_df, input_encoding = load_csv_safely(INPUT_PATH)
    filtered_df, removed_columns = drop_excluded_columns(input_df)
    output_df, missing_expected_columns = reorder_analysis_columns(filtered_df)

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

    validations = validate_analysis_total(input_df, output_df, removed_columns)
    validations["expected_existing_columns_kept"] = all(
        column in output_df.columns
        for column in EXPECTED_ORDER
        if column in filtered_df.columns
    )
    validations["output_utf8_readable"] = len(output_check.columns) == len(output_df.columns)

    kept_core_columns = [column for column in EXPECTED_ORDER if column in output_df.columns]
    warnings = []
    if missing_expected_columns:
        warnings.append("기대 변수 중 일부가 cleaned 파일에 없어 생성하지 않고 건너뛰었습니다.")
    if "weight" in missing_expected_columns:
        warnings.append("weight clean 변수는 현재 cleaned 파일에 없으며, weight_raw는 _raw 제외 규칙으로 제거되었습니다.")

    write_korean_log(
        input_shape=input_df.shape,
        output_shape=output_df.shape,
        input_encoding=input_encoding,
        removed_columns=removed_columns,
        kept_core_columns=kept_core_columns,
        missing_expected_columns=missing_expected_columns,
        validations=validations,
        warnings=warnings,
    )

    summary_df = build_analysis_summary(
        removed_columns=removed_columns,
        kept_core_columns=kept_core_columns,
        missing_expected_columns=missing_expected_columns,
    )
    summary_markdown = dataframe_to_markdown(summary_df)
    SUMMARY_PATH.write_text(summary_markdown + "\n", encoding="utf-8")

    print(f"analysis_total 파일 생성 완료: {OUTPUT_PATH}")
    print(f"로그 파일 생성 완료: {LOG_PATH}")
    print(f"요약표 생성 완료: {SUMMARY_PATH}")
    print(f"입력 행 수: {len(input_df)}, 출력 행 수: {len(output_df)}")
    print(f"입력 열 수: {input_df.shape[1]}, 출력 열 수: {output_df.shape[1]}")
    print("")
    print(summary_markdown)


if __name__ == "__main__":
    main()
