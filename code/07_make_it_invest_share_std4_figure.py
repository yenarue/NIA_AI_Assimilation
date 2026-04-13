from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "merged" / "nia_2020_2024_merged.csv"
OUTPUT_DIR = BASE_DIR / "output" / "figures"
FIGURE_PATH = OUTPUT_DIR / "fig_it_invest_share_std4_distribution.png"
SUMMARY_PATH = OUTPUT_DIR / "fig_it_invest_share_std4_summary.csv"
NOTES_PATH = OUTPUT_DIR / "fig_it_invest_share_std4_notes.md"

CATEGORY_ORDER = [1, 2, 3, 4]
CATEGORY_LABELS = {
    1: "1% or less",
    2: ">1% to <5%",
    3: ">5% to <10%",
    4: "10% or more",
}
STANDARD_MISSING = {
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


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    mpl_config_dir = OUTPUT_DIR / ".mplconfig"
    mpl_config_dir.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(mpl_config_dir)


ensure_output_dir()
import matplotlib.pyplot as plt  # noqa: E402  pylint: disable=wrong-import-position


def clean_string(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    text = str(value).strip()
    if text in STANDARD_MISSING:
        return pd.NA
    return text


def safe_numeric(series: pd.Series) -> pd.Series:
    cleaned = (
        series.map(clean_string)
        .astype("string")
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    cleaned = cleaned.replace({"": pd.NA})
    return pd.to_numeric(cleaned, errors="coerce")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT_PATH, dtype=str, keep_default_na=False)
    df["it_invest_share_std4"] = safe_numeric(df["it_invest_share_std4"])
    return df


def build_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    valid = df[df["it_invest_share_std4"].isin(CATEGORY_ORDER)].copy()
    valid_n = len(valid)
    rows: list[dict[str, object]] = []

    for code in CATEGORY_ORDER:
        count = int((valid["it_invest_share_std4"] == code).sum())
        percentage = (count / valid_n * 100) if valid_n else 0.0
        rows.append(
            {
                "category_code": code,
                "category_label": CATEGORY_LABELS[code],
                "count": count,
                "percentage": percentage,
                "valid_n": valid_n,
            }
        )

    return pd.DataFrame(rows), valid_n


def set_plot_style() -> None:
    plt.style.use("default")
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#333333",
            "axes.labelcolor": "#222222",
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "xtick.color": "#222222",
            "ytick.color": "#222222",
            "font.size": 10,
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
        }
    )


def draw_figure(summary_df: pd.DataFrame) -> None:
    set_plot_style()
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    counts = summary_df["count"].tolist()
    labels = summary_df["category_label"].tolist()
    percentages = summary_df["percentage"].tolist()

    bars = ax.bar(labels, counts, color="#5B84B1", edgecolor="#355C7D", width=0.65)
    ax.set_xlabel("Standardized investment share category")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of standardized informationization investment share")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)

    upper = max(counts + [0]) * 1.15 + 1
    ax.set_ylim(0, upper)
    offset = upper * 0.01
    for bar, count, pct in zip(bars, counts, percentages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + offset,
            f"{count:,}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.savefig(FIGURE_PATH, dpi=300)
    plt.close(fig)


def write_notes(summary_df: pd.DataFrame, valid_n: int) -> None:
    top_two = summary_df.sort_values("count", ascending=False).head(2)["category_label"].tolist()
    lines = [
        "# Figure Note",
        "",
        "## 그림. 표준화된 정보화 투자 비중 분포",
        f"- 표준화된 정보화 투자 비중 분포를 보면 기업들은 상대적으로 낮은 투자 비중 구간에 더 많이 집중되어 있으며, 특히 `{', '.join(top_two)}` 범주에 관측치가 많이 분포한다. 반면 높은 투자 비중 범주로 갈수록 기업 수는 상대적으로 적어, 정보화 투자 강도가 오른쪽으로 치우친 분포를 가질 가능성을 시사한다.",
        f"- 유효 표본 수: {valid_n:,}",
        "- 이 그림은 분포 점검을 위한 기술통계 결과이며, 인과적 근거를 제공하지 않는다.",
    ]
    NOTES_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = load_data()
    summary_df, valid_n = build_summary(df)
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")
    draw_figure(summary_df)
    write_notes(summary_df, valid_n)

    print(f"Saved figure: {FIGURE_PATH}")
    print(f"Saved summary CSV: {SUMMARY_PATH}")
    print(f"Saved notes markdown: {NOTES_PATH}")


if __name__ == "__main__":
    main()
