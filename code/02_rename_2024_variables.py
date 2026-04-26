#!/usr/bin/env python3
"""NIA 2024 subset 파일의 열 이름만 연구용 변수명으로 변경합니다.

주의:
- 이 스크립트는 rename만 수행합니다.
- 값 recoding, 결측 처리, clean 처리, 파생변수 생성, 변수 조합은 하지 않습니다.
- 입력 파일은 수정하지 않고 새 CSV 파일로 저장합니다.
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "working" / "subset" / "nia_2024_subset.csv"
OUTPUT_PATH = BASE_DIR / "working" / "rename" / "nia_2024_renamed.csv"
LOG_PATH = BASE_DIR / "working" / "rename" / "rename_log_2024.txt"
SUMMARY_PATH = BASE_DIR / "working" / "rename" / "rename_summary_2024.md"

RENAME_MAPPING = OrderedDict(
    [
        ("Q34", "it_org_any_raw"),
        ("Q34_1_1", "it_org_internal_raw"),
        ("Q34_1_2", "it_org_mixed_raw"),
        ("Q34_1_3", "it_org_outsource_raw"),

        ("Q32", "it_invest_any_raw"),
        ("Q32_1", "it_invest_hardware_raw"),
        ("Q32_2", "it_invest_software_raw"),
        ("Q32_3", "it_invest_sys_op_raw"),
        ("Q32_4", "it_invest_infra_raw"),
        ("Q32_5", "it_invest_op_salary_raw"),
        ("Q32_6", "it_invest_new_tech_raw"),
        ("Q32_7", "it_invest_rnd_raw"),
        ("Q32_8", "it_invest_tech_train_raw"),

        ("Q33", "it_invest_share_raw"),

        ("Q28", "ai_use_raw"),
        ("Q28_1", "ai_use_doc_info_collect_raw"),
        ("Q28_2", "ai_use_task_automation_raw"),
        ("Q28_3", "ai_use_decision_support_raw"),
        ("Q28_4", "ai_use_speech_to_text_raw"),
        ("Q28_5", "ai_use_gen_summarize_edit_raw"),
        ("Q28_6", "ai_use_image_video_recognition_raw"),
        ("Q28_7", "ai_use_ml_data_analysis_raw"),
        ("Q28_8", "ai_use_text_language_analysis_raw"),
        ("Q28_9", "ai_use_autonomous_mobility_raw"),
        ("Q28_10", "ai_use_other_raw"),
        ("Q28_10_ETC", "ai_use_other_text_raw"),

        ("Q29_1", "ai_purpose_marketing_sales_raw"),
        ("Q29_2", "ai_purpose_prod_service_improve_raw"),
        ("Q29_3", "ai_purpose_biz_process_org_raw"),
        ("Q29_4", "ai_purpose_logistics_raw"),
        ("Q29_5", "ai_purpose_security_raw"),
        ("Q29_6", "ai_purpose_accounting_finance_raw"),
        ("Q29_7", "ai_purpose_rnd_innovation_raw"),
        ("Q29_8", "ai_purpose_cost_reduction_raw"),
        ("Q29_9", "ai_purpose_customer_demand_raw"),
        ("Q29_10", "ai_purpose_other_raw"),
        ("Q29_10_ETC", "ai_purpose_other_text_raw"),

        ("Q30_1", "ai_impl_inhouse_dev_raw"),
        ("Q30_2", "ai_impl_modify_commercial_raw"),
        ("Q30_3", "ai_impl_modify_open_source_raw"),
        ("Q30_4", "ai_impl_buy_commercial_raw"),
        ("Q30_5", "ai_impl_vendor_contract_raw"),
        ("Q30_6", "ai_impl_other_raw"),
        ("Q30_6_ETC", "ai_impl_other_text_raw"),

        ("Q35_1", "effect_proc_improve_raw"),
        ("Q35_2", "effect_internal_cohesion_raw"),
        ("Q35_3", "effect_decision_improve_raw"),
        ("Q35_4", "effect_stakeholders_raw"),
        ("Q35_5", "effect_innov_outcome_raw"),
        ("Q35_6", "effect_competitiveness_raw"),

        ("D_SIZE", "firm_size_raw"),
        ("D_IND", "industry_raw"),
        ("D_INDSIZE", "industry_size_raw"),
        ("RIM_WT", "weight_raw"),
        ("year", "year"),
    ]
)


def detect_encoding(path: Path) -> str:
    """CSV 파일을 안전하게 읽기 위한 인코딩을 후보군에서 탐지합니다."""
    candidates = ("utf-8-sig", "utf-8", "cp949", "euc-kr", "latin1")
    raw_bytes = path.read_bytes()

    for encoding in candidates:
        try:
            raw_bytes.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue

    raise UnicodeError(f"사용 가능한 인코딩을 찾지 못했습니다: {path}")


def load_csv_safely(path: Path) -> tuple[pd.DataFrame, str]:
    """값을 바꾸지 않도록 모든 값을 문자열로 읽습니다."""
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


def apply_rename_mapping(
    df: pd.DataFrame,
    rename_mapping: OrderedDict[str, str],
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """입력에 존재하는 매핑 대상 열만 rename합니다."""
    existing_source_columns = [source for source in rename_mapping if source in df.columns]
    missing_source_columns = [source for source in rename_mapping if source not in df.columns]
    applicable_mapping = {
        source: rename_mapping[source]
        for source in existing_source_columns
    }

    # 요청된 매핑 대상 열과 year만 유지합니다.
    kept_columns = existing_source_columns.copy()
    if "year" in df.columns:
        kept_columns.append("year")

    renamed = df.loc[:, kept_columns].rename(columns=applicable_mapping)
    return renamed, existing_source_columns, missing_source_columns


def reorder_columns(
    df: pd.DataFrame,
    rename_mapping: OrderedDict[str, str],
    existing_source_columns: Iterable[str],
) -> pd.DataFrame:
    """출력 열 순서를 year, rename 매핑표 순서로 맞춥니다."""
    ordered_columns = []
    if "year" in df.columns:
        ordered_columns.append("year")

    ordered_columns.extend(
        rename_mapping[source]
        for source in existing_source_columns
        if rename_mapping[source] in df.columns
    )

    return df.loc[:, ordered_columns]


def format_list(values: Iterable[str]) -> str:
    """로그에서 목록을 보기 쉽게 한 줄씩 작성합니다."""
    values = list(values)
    if not values:
        return "- 없음"
    return "\n".join(f"- {value}" for value in values)


def write_korean_log(
    *,
    input_path: Path,
    output_path: Path,
    input_shape: tuple[int, int],
    output_shape: tuple[int, int],
    requested_columns: list[str],
    renamed_pairs: list[tuple[str, str]],
    missing_columns: list[str],
    year_kept: bool,
    values_unchanged: bool,
    input_encoding: str,
    output_encoding: str,
    warnings: list[str],
) -> None:
    """rename 작업 결과를 한글 로그로 저장합니다."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    renamed_lines = [f"- {source} -> {target}" for source, target in renamed_pairs]

    lines = [
        "NIA 2024 rename 처리 로그",
        "",
        "[파일 경로]",
        f"- 입력 파일 경로: {input_path}",
        f"- 출력 파일 경로: {output_path}",
        "",
        "[행/열 수]",
        f"- 입력 파일 행 수: {input_shape[0]}",
        f"- 입력 파일 열 수: {input_shape[1]}",
        f"- 출력 파일 행 수: {output_shape[0]}",
        f"- 출력 파일 열 수: {output_shape[1]}",
        "",
        "[요청된 rename 대상 열 목록]",
        format_list(requested_columns),
        "",
        "[실제로 rename된 열 목록]",
        "\n".join(renamed_lines) if renamed_lines else "- 없음",
        "",
        "[누락된 열 목록]",
        format_list(missing_columns),
        "",
        "[year 열]",
        f"- year 열 유지 여부: {'예' if year_kept else '아니오'}",
        "",
        "[값 변경 확인]",
        f"- 값 변경 없음 확인 여부: {'예' if values_unchanged else '아니오'}",
        "",
        "[인코딩]",
        f"- 입력 파일 인코딩: {input_encoding}",
        f"- 출력 파일 저장 인코딩: {output_encoding}",
        "",
        "[특이사항 / 경고사항]",
        format_list(warnings),
        "",
        "[주의]",
        "- 이 스크립트는 열 이름 변경만 수행했습니다.",
        "- 값 recoding, 결측 처리, 파생변수 생성, 변수 조합, clean 처리는 수행하지 않았습니다.",
    ]

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_escape(value: object) -> str:
    """마크다운 표에서 파이프 문자가 표 구조를 깨지 않도록 처리합니다."""
    return str(value).replace("|", "\\|")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """외부 tabulate 의존성 없이 간단한 markdown 표를 생성합니다."""
    headers = [markdown_escape(column) for column in df.columns]
    rows = [
        [markdown_escape(value) for value in row]
        for row in df.itertuples(index=False, name=None)
    ]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def build_rename_summary_table(
    *,
    rename_mapping: OrderedDict[str, str],
    existing_source_columns: list[str],
    missing_columns: list[str],
    year_kept: bool,
) -> pd.DataFrame:
    """요청 형식에 맞춘 rename 처리 결과 요약표를 만듭니다."""
    existing_set = set(existing_source_columns)
    missing_set = set(missing_columns)
    rows = []

    if year_kept:
        rows.append(
            {
                "파일명": "nia_2024_renamed.csv",
                "변수명": "year",
                "처리단계": "rename",
                "처리 전 상태": "기존 year 열",
                "처리 내용": "year 열 이름 및 값 유지",
                "처리 이유": "연도 식별 열 유지",
                "처리 후 상태": "year",
                "관측치 변화 (N)": "변화 없음",
                "비고": "year 유지",
            }
        )

    for source, target in rename_mapping.items():
        if source in existing_set:
            rows.append(
                {
                    "파일명": "nia_2024_subset.csv",
                    "변수명": source,
                    "처리단계": "rename",
                    "처리 전 상태": f"원본 열 이름 {source}",
                    "처리 내용": f"{source} -> {target} 로 열 이름 변경",
                    "처리 이유": "연구용 변수명 체계 통일",
                    "처리 후 상태": target,
                    "관측치 변화 (N)": "변화 없음",
                    "비고": "rename 완료",
                }
            )
        elif source in missing_set:
            rows.append(
                {
                    "파일명": "nia_2024_subset.csv",
                    "변수명": source,
                    "처리단계": "rename",
                    "처리 전 상태": f"입력 파일에 {source} 열 없음",
                    "처리 내용": "rename 건너뜀",
                    "처리 이유": "입력 파일에 해당 열이 없어 작업 실패 없이 누락 기록",
                    "처리 후 상태": "누락",
                    "관측치 변화 (N)": "변화 없음",
                    "비고": "누락된 열",
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


def verify_values_unchanged(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    rename_mapping: OrderedDict[str, str],
    existing_source_columns: list[str],
) -> bool:
    """rename 전후 값이 같은지 원본 열과 변경 후 열을 1:1로 비교합니다."""
    for source in existing_source_columns:
        target = rename_mapping[source]
        if not input_df[source].equals(output_df[target]):
            return False

    if "year" in input_df.columns:
        return input_df["year"].equals(output_df["year"])

    return True


def main() -> None:
    """subset CSV를 읽어 rename CSV, 로그, 요약표를 생성합니다."""
    input_df, input_encoding = load_csv_safely(INPUT_PATH)
    input_shape = input_df.shape

    renamed_df, existing_source_columns, missing_columns = apply_rename_mapping(
        input_df,
        RENAME_MAPPING,
    )
    renamed_df = reorder_columns(
        renamed_df,
        RENAME_MAPPING,
        existing_source_columns,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    renamed_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    # 저장된 utf-8 출력 파일을 다시 읽어 검증합니다.
    output_df = pd.read_csv(
        OUTPUT_PATH,
        encoding="utf-8",
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        low_memory=False,
    )

    renamed_pairs = [
        (source, RENAME_MAPPING[source])
        for source in existing_source_columns
    ]
    expected_columns = ["year"] if "year" in input_df.columns else []
    expected_columns.extend(RENAME_MAPPING[source] for source in existing_source_columns)

    row_count_match = len(input_df) == len(output_df)
    renamed_columns_correct = output_df.columns.tolist() == expected_columns
    year_kept = "year" in input_df.columns and "year" in output_df.columns
    values_unchanged = verify_values_unchanged(
        input_df,
        output_df,
        RENAME_MAPPING,
        existing_source_columns,
    )

    warnings = []
    if missing_columns:
        warnings.append("입력 파일에 없는 rename 대상 열이 있어 해당 열은 건너뛰었습니다.")
    if not year_kept:
        warnings.append("입력 파일에 year 열이 없어 출력 파일에도 year 열을 유지하지 못했습니다.")
    if not row_count_match:
        warnings.append("입력 파일과 출력 파일의 행 수가 다릅니다.")
    if not renamed_columns_correct:
        warnings.append("출력 파일 열 이름 또는 열 순서가 예상과 다릅니다.")
    if not values_unchanged:
        warnings.append("값 변경 없음 검증이 실패했습니다.")
    if not warnings:
        warnings.append("특이사항 없음")

    write_korean_log(
        input_path=INPUT_PATH,
        output_path=OUTPUT_PATH,
        input_shape=input_shape,
        output_shape=output_df.shape,
        requested_columns=list(RENAME_MAPPING.keys()),
        renamed_pairs=renamed_pairs,
        missing_columns=missing_columns,
        year_kept=year_kept,
        values_unchanged=values_unchanged,
        input_encoding=input_encoding,
        output_encoding="utf-8",
        warnings=warnings,
    )

    summary_df = build_rename_summary_table(
        rename_mapping=RENAME_MAPPING,
        existing_source_columns=existing_source_columns,
        missing_columns=missing_columns,
        year_kept=year_kept,
    )
    summary_markdown = dataframe_to_markdown(summary_df)
    SUMMARY_PATH.write_text(summary_markdown + "\n", encoding="utf-8")

    print(f"rename 파일 생성 완료: {OUTPUT_PATH}")
    print(f"로그 파일 생성 완료: {LOG_PATH}")
    print(f"요약표 생성 완료: {SUMMARY_PATH}")
    print(f"입력 행 수: {len(input_df)}, 출력 행 수: {len(output_df)}")
    print(f"rename 완료 열 수: {len(existing_source_columns)}, 누락 열 수: {len(missing_columns)}")
    print("")
    print(summary_markdown)


if __name__ == "__main__":
    main()
