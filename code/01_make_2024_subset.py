#!/usr/bin/env python3
"""NIA 2024 raw 데이터에서 연구용 subset CSV를 생성합니다.

주의:
- 이 스크립트는 subset 추출만 수행합니다.
- 변수명 변경, 값 recoding, clean 처리, 결측값 규칙 적용, 파생변수 생성은 하지 않습니다.
- 추가 생성 열은 year=2024 하나뿐입니다.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "raw" / "nia_2024_raw.csv"
CODEBOOK_PATH = BASE_DIR / "raw" / "nia_2024_codebook.csv"
OUTPUT_PATH = BASE_DIR / "working" / "subset" / "nia_2024_subset.csv"
LOG_PATH = BASE_DIR / "working" / "subset" / "subset_extraction_log_2024.txt"

REQUESTED_COLUMNS = [
    "Q34",
    "Q34_1_1",
    "Q34_1_2",
    "Q34_1_3",
    "Q32",
    "Q32_1",
    "Q32_2",
    "Q32_3",
    "Q32_4",
    "Q32_5",
    "Q32_6",
    "Q32_7",
    "Q32_8",
    "Q33",
    "REQ33",
    "Q28",
    "Q28_1",
    "Q28_2",
    "Q28_3",
    "Q28_4",
    "Q28_5",
    "Q28_6",
    "Q28_7",
    "Q28_8",
    "Q28_9",
    "Q28_10",
    "Q28_10_ETC",
    "Q29_1",
    "Q29_2",
    "Q29_3",
    "Q29_4",
    "Q29_5",
    "Q29_6",
    "Q29_7",
    "Q29_8",
    "Q29_9",
    "Q29_10",
    "Q29_10_ETC",
    "Q30_1",
    "Q30_2",
    "Q30_3",
    "Q30_4",
    "Q30_5",
    "Q30_6",
    "Q30_6_ETC",
    "Q35_1",
    "Q35_3",
    "Q35_5",
    "Q35_2",
    "Q35_4",
    "Q35_6",
    "D_SIZE",
    "D_IND",
    "D_INDSIZE",
    "RIM_WT",
]


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

    # latin1은 모든 byte를 디코딩할 수 있어 보통 여기까지 오지 않습니다.
    raise UnicodeError(f"사용 가능한 인코딩을 찾지 못했습니다: {path}")


def load_csv_safely(path: Path) -> tuple[pd.DataFrame, str]:
    """원본 값을 임의 변환하지 않도록 모든 값을 문자열로 읽습니다."""
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


def read_codebook_variables(path: Path) -> tuple[set[str], str | None]:
    """코드북의 변수명 목록을 참고용으로 읽습니다. 실패해도 subset 생성은 계속합니다."""
    if not path.exists():
        return set(), None

    encoding = detect_encoding(path)
    codebook = pd.read_csv(
        path,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        low_memory=False,
    )

    first_col = codebook.columns[0]
    variables = {
        value
        for value in codebook[first_col].tolist()
        if value and value != "변수명"
    }
    return variables, encoding


def extract_columns_with_logging(
    df: pd.DataFrame,
    requested_columns: Iterable[str],
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """요청 컬럼 순서를 유지하면서 존재하는 컬럼만 추출하고 year 열을 추가합니다."""
    requested = list(requested_columns)
    extracted_columns = [column for column in requested if column in df.columns]
    missing_columns = [column for column in requested if column not in df.columns]

    subset = df.loc[:, extracted_columns].copy()
    subset["year"] = "2024"

    return subset, extracted_columns, missing_columns


def format_list(values: Iterable[str]) -> str:
    """로그 파일에서 사람이 보기 쉽도록 목록을 한 줄씩 출력합니다."""
    values = list(values)
    if not values:
        return "- 없음"
    return "\n".join(f"- {value}" for value in values)


def write_log(
    *,
    input_path: Path,
    output_path: Path,
    requested_columns: list[str],
    extracted_columns: list[str],
    missing_columns: list[str],
    original_row_count: int,
    output_row_count: int,
    original_column_count: int,
    output_column_count: int,
    input_encoding: str,
    output_encoding: str,
    year_added: bool,
    codebook_path: Path,
    codebook_encoding: str | None,
    requested_missing_from_codebook: list[str],
    validation_results: dict[str, bool],
) -> None:
    """subset 추출 결과와 검증 결과를 한글 로그로 저장합니다."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "NIA 2024 subset 추출 로그",
        "",
        "[파일 경로]",
        f"- input file path: {input_path}",
        f"- output file path: {output_path}",
        f"- codebook file path: {codebook_path}",
        "",
        "[컬럼 추출 결과]",
        "- requested columns:",
        format_list(requested_columns),
        "- extracted columns:",
        format_list(extracted_columns),
        "- missing columns:",
        format_list(missing_columns),
        "",
        "[행/열 개수]",
        f"- original row count: {original_row_count}",
        f"- output row count: {output_row_count}",
        f"- original column count: {original_column_count}",
        f"- output column count: {output_column_count}",
        "",
        "[인코딩]",
        f"- 사용한 인코딩(input): {input_encoding}",
        f"- 저장 인코딩(output): {output_encoding}",
        f"- 코드북 인코딩(참고): {codebook_encoding or '확인 불가'}",
        "",
        "[year 열]",
        f"- year column 추가 여부: {'예' if year_added else '아니오'}",
        "",
        "[코드북 교차 확인(참고)]",
        "- 코드북에서 찾지 못한 요청 컬럼:",
        format_list(requested_missing_from_codebook),
        "",
        "[검증 결과]",
        f"- output row count == original row count: {'통과' if validation_results['row_count_match'] else '실패'}",
        f"- 추출 컬럼 순서가 요청 순서와 일치: {'통과' if validation_results['column_order_match'] else '실패'}",
        f"- missing columns 로그 기록 여부: {'통과' if validation_results['missing_columns_logged'] else '실패'}",
        f"- year 열 추가 여부: {'통과' if validation_results['year_column_added'] else '실패'}",
        f"- 원본 값 변경 없음: {'통과' if validation_results['values_unchanged'] else '실패'}",
        "",
        "[주의]",
        "- 이 스크립트는 subset 추출만 수행했습니다.",
        "- 변수명 rename, 값 recoding, clean 처리, 결측값 규칙 적용, 추가 파생변수 생성은 수행하지 않았습니다.",
    ]

    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """raw CSV를 읽고 요청한 컬럼만 subset CSV로 저장합니다."""
    df, input_encoding = load_csv_safely(INPUT_PATH)
    original_row_count = len(df)
    original_column_count = len(df.columns)

    codebook_variables, codebook_encoding = read_codebook_variables(CODEBOOK_PATH)
    requested_missing_from_codebook = [
        column for column in REQUESTED_COLUMNS if codebook_variables and column not in codebook_variables
    ]

    subset, extracted_columns, missing_columns = extract_columns_with_logging(
        df,
        REQUESTED_COLUMNS,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    # 저장 후 다시 읽어 row/column/value 보존 상태를 확인합니다.
    output_df = pd.read_csv(
        OUTPUT_PATH,
        encoding="utf-8",
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        low_memory=False,
    )
    expected_columns = extracted_columns + ["year"]

    validation_results = {
        "row_count_match": len(output_df) == original_row_count,
        "column_order_match": output_df.columns.tolist() == expected_columns,
        "missing_columns_logged": isinstance(missing_columns, list),
        "year_column_added": "year" in output_df.columns and (output_df["year"] == "2024").all(),
        "values_unchanged": output_df.loc[:, extracted_columns].equals(df.loc[:, extracted_columns]),
    }

    write_log(
        input_path=INPUT_PATH,
        output_path=OUTPUT_PATH,
        requested_columns=REQUESTED_COLUMNS,
        extracted_columns=extracted_columns,
        missing_columns=missing_columns,
        original_row_count=original_row_count,
        output_row_count=len(output_df),
        original_column_count=original_column_count,
        output_column_count=len(output_df.columns),
        input_encoding=input_encoding,
        output_encoding="utf-8",
        year_added=validation_results["year_column_added"],
        codebook_path=CODEBOOK_PATH,
        codebook_encoding=codebook_encoding,
        requested_missing_from_codebook=requested_missing_from_codebook,
        validation_results=validation_results,
    )

    print(f"subset 파일 생성 완료: {OUTPUT_PATH}")
    print(f"로그 파일 생성 완료: {LOG_PATH}")
    print(f"원본 행 수: {original_row_count}, 출력 행 수: {len(output_df)}")
    print(f"추출 컬럼 수: {len(extracted_columns)}, 누락 컬럼 수: {len(missing_columns)}")


if __name__ == "__main__":
    main()
