from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CANDIDATES = [
    BASE_DIR / "working" / "merged" / "nia_2020_2024_merged.csv",
    BASE_DIR / "merged" / "nia_2020_2024_merged.csv",
]
TARGET_COLUMN = "it_org_type"
MISSING_VALUES = {"", "NA", "N/A", "na", "n/a", "null", "NULL", "None", "none", "."}


def resolve_input_path() -> Path:
    for path in INPUT_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "nia_2020_2024_merged.csv 파일을 찾지 못했습니다. "
        f"확인한 경로: {', '.join(str(path) for path in INPUT_CANDIDATES)}"
    )


def normalize(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if text in MISSING_VALUES:
        return None
    return text


def load_column(path: Path, column_name: str) -> list[str | None]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or column_name not in reader.fieldnames:
            raise KeyError(f"'{column_name}' 변수가 데이터에 없습니다.")
        return [normalize(row.get(column_name)) for row in reader]


def describe_categorical(values: list[str | None]) -> dict[str, object]:
    non_missing = [value for value in values if value is not None]
    counts = Counter(non_missing)
    top, freq = (None, 0)
    if counts:
        top, freq = counts.most_common(1)[0]

    return {
        "count": len(non_missing),
        "unique": len(counts),
        "top": top,
        "freq": freq,
        "missing": len(values) - len(non_missing),
    }


def format_value_count_label(value: str | None) -> str:
    return "NaN" if value is None else value


def print_value_counts(values: list[str | None]) -> None:
    counts = Counter(values)
    for value, count in counts.most_common():
        print(f"{format_value_count_label(value)}\t{count}")


def main() -> None:
    input_path = resolve_input_path()
    values = load_column(input_path, TARGET_COLUMN)
    summary = describe_categorical(values)

    print(f"Input file: {input_path}")
    print(f"Variable: {TARGET_COLUMN}")
    print()
    print("[describe]")
    for key in ["count", "unique", "top", "freq", "missing"]:
        print(f"{key}\t{summary[key]}")
    print()
    print("[value_counts(dropna=False)]")
    print_value_counts(values)


if __name__ == "__main__":
    main()
