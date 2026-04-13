from __future__ import annotations

import math
import os
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "merged" / "nia_2020_2024_merged.csv"
OUTPUT_DIR = BASE_DIR / "output" / "figures"
SUMMARY_PATH = OUTPUT_DIR / "figure_summary_stats_week6.csv"
NOTES_PATH = OUTPUT_DIR / "figure_notes_week6.md"

FIG1_PATH = OUTPUT_DIR / "fig1_proc_improve_distribution.png"
FIG2_PATH = OUTPUT_DIR / "fig2_ai_use_by_it_org_type.png"
FIG3_PATH = OUTPUT_DIR / "fig3_proc_high_by_it_org_type.png"
FIG4_PATH = OUTPUT_DIR / "fig4_hist_it_invest_share_pct.png"

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
GROUP_ORDER = [0, 1, 2, 3, 4]
GROUP_LABELS = {
    0: "None",
    1: "Internal",
    2: "Mixed-duty",
    3: "Outsourced",
    4: "Multiple",
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
    for column in df.columns:
        df[column] = df[column].map(clean_string)

    numeric_columns = ["year", "it_org_type", "ai_use", "proc_improve", "it_invest_share_pct"]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = safe_numeric(df[column])

    df["proc_high"] = pd.NA
    valid_proc = df["proc_improve"].isin([1, 2, 3, 4, 5])
    df.loc[valid_proc & df["proc_improve"].isin([4, 5]), "proc_high"] = 1
    df.loc[valid_proc & df["proc_improve"].isin([1, 2, 3]), "proc_high"] = 0
    df["proc_high"] = pd.to_numeric(df["proc_high"], errors="coerce")
    return df


def set_clean_style() -> None:
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


def build_proc_distribution(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[df["proc_improve"].isin([1, 2, 3, 4, 5])].copy()
    valid_n = len(valid)
    rows: list[dict[str, object]] = []
    for code in [1, 2, 3, 4, 5]:
        count = int((valid["proc_improve"] == code).sum())
        percentage = (count / valid_n * 100) if valid_n else math.nan
        rows.append(
            {
                "figure_id": "fig1",
                "variable": "proc_improve",
                "group_code": code,
                "group_label": str(code),
                "valid_n": valid_n,
                "positive_n": count,
                "percentage": percentage,
                "notes": "Distribution across response categories 1-5",
            }
        )
    return pd.DataFrame(rows), valid_n


def build_group_rate(df: pd.DataFrame, outcome_col: str, figure_id: str) -> tuple[pd.DataFrame, int, list[str]]:
    valid = df[df["it_org_type"].isin(GROUP_ORDER) & df[outcome_col].isin([0, 1])].copy()
    total_valid_n = len(valid)
    missing_groups: list[str] = []
    rows: list[dict[str, object]] = []

    for code in GROUP_ORDER:
        label = GROUP_LABELS[code]
        group_df = valid[valid["it_org_type"] == code]
        valid_n = len(group_df)
        positive_n = int((group_df[outcome_col] == 1).sum())
        percentage = (positive_n / valid_n * 100) if valid_n else math.nan
        if valid_n == 0:
            missing_groups.append(label)
        rows.append(
            {
                "figure_id": figure_id,
                "variable": outcome_col,
                "group_code": code,
                "group_label": label,
                "valid_n": valid_n,
                "positive_n": positive_n,
                "percentage": percentage,
                "notes": "",
            }
        )
    return pd.DataFrame(rows), total_valid_n, missing_groups


def build_hist_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, int, float | None]:
    valid = df["it_invest_share_pct"].dropna().astype(float)
    valid_n = len(valid)
    if valid_n == 0:
        row = {
            "figure_id": "fig4",
            "variable": "it_invest_share_pct",
            "group_code": pd.NA,
            "group_label": "overall",
            "valid_n": 0,
            "positive_n": pd.NA,
            "percentage": pd.NA,
            "count": 0,
            "mean": pd.NA,
            "median": pd.NA,
            "p25": pd.NA,
            "p75": pd.NA,
            "min": pd.NA,
            "max": pd.NA,
            "p95": pd.NA,
            "p99": pd.NA,
            "notes": "No valid observations for histogram",
        }
        return pd.DataFrame([row]), 0, None

    p25 = float(valid.quantile(0.25))
    median = float(valid.quantile(0.50))
    p75 = float(valid.quantile(0.75))
    p95 = float(valid.quantile(0.95))
    p99 = float(valid.quantile(0.99))
    max_value = float(valid.max())
    display_cap = p99 if p99 > 0 and max_value > p99 * 1.2 else None
    note = "Histogram uses full x-axis range"
    if display_cap is not None:
        note = f"Display-only x-axis capped at 99th percentile ({display_cap:.2f})"

    row = {
        "figure_id": "fig4",
        "variable": "it_invest_share_pct",
        "group_code": pd.NA,
        "group_label": "overall",
        "valid_n": valid_n,
        "positive_n": pd.NA,
        "percentage": pd.NA,
        "count": valid_n,
        "mean": float(valid.mean()),
        "median": median,
        "p25": p25,
        "p75": p75,
        "min": float(valid.min()),
        "max": max_value,
        "p95": p95,
        "p99": p99,
        "notes": note,
    }
    return pd.DataFrame([row]), valid_n, display_cap


def add_bar_labels(ax: plt.Axes, values: list[float], suffix: str = "%") -> None:
    upper = ax.get_ylim()[1]
    offset = upper * 0.015
    for index, value in enumerate(values):
        if pd.isna(value):
            continue
        ax.text(index, value + offset, f"{value:.1f}{suffix}", ha="center", va="bottom", fontsize=10)


def draw_distribution_bar(summary_df: pd.DataFrame, output_path: Path) -> None:
    set_clean_style()
    fig, ax = plt.subplots(figsize=(8, 5))
    x_labels = summary_df["group_label"].tolist()
    percentages = summary_df["percentage"].fillna(0).tolist()
    bars = ax.bar(x_labels, percentages, color="#4C78A8", edgecolor="#2F4B6C", width=0.65)
    ax.set_xlabel("proc_improve response category")
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Distribution of proc_improve")
    ax.set_ylim(0, max(percentages + [0]) * 1.18 + 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    add_bar_labels(ax, percentages)
    for bar in bars:
        bar.set_linewidth(0.8)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def draw_group_rate_bar(summary_df: pd.DataFrame, output_path: Path, title: str, y_label: str) -> None:
    set_clean_style()
    fig, ax = plt.subplots(figsize=(8.5, 5))
    plot_df = summary_df.copy()
    percentages = plot_df["percentage"].fillna(0).tolist()
    bars = ax.bar(plot_df["group_label"], percentages, color="#6BA292", edgecolor="#3E6A5D", width=0.65)
    ax.set_xlabel("Informationization organization type")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_ylim(0, max(percentages + [0]) * 1.18 + 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    add_bar_labels(ax, percentages)
    for bar in bars:
        bar.set_linewidth(0.8)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def draw_histogram(df: pd.DataFrame, output_path: Path, display_cap: float | None) -> None:
    set_clean_style()
    valid = df["it_invest_share_pct"].dropna().astype(float)
    plot_values = valid[valid <= display_cap] if display_cap is not None else valid

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.hist(plot_values, bins=30, color="#D98E73", edgecolor="#8C4C33")
    ax.set_xlabel("Informationization investment share (%)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of informationization investment share")
    if display_cap is not None:
        ax.set_xlim(left=0, right=display_cap)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def write_notes(
    fig1_df: pd.DataFrame,
    fig2_df: pd.DataFrame,
    fig3_df: pd.DataFrame,
    fig4_df: pd.DataFrame,
    fig1_valid_n: int,
    fig2_valid_n: int,
    fig3_valid_n: int,
    fig4_valid_n: int,
    fig2_missing_groups: list[str],
    fig3_missing_groups: list[str],
    display_cap: float | None,
) -> None:
    fig1_top = fig1_df.sort_values("percentage", ascending=False).head(2)["group_label"].tolist()
    fig2_top = fig2_df.sort_values("percentage", ascending=False).head(2)["group_label"].tolist()
    fig3_top = fig3_df.sort_values("percentage", ascending=False).head(2)["group_label"].tolist()

    lines = [
        "# Week 6 Figure Notes",
        "",
        "## 그림 1. proc_improve 전체 분포",
        f"- `proc_improve` 응답은 상위 범주에 상대적으로 더 많이 분포하는지 확인하기 위한 기술통계 그림이다. 이번 데이터에서는 상위 비중이 큰 범주가 `{', '.join(fig1_top)}`로 나타났으며, 전반적인 응답 집중 구간을 점검하는 용도로 해석하는 것이 적절하다.",
        f"- 유효 표본 수: {fig1_valid_n:,}",
        "- 이 그림은 분포 점검을 위한 기술통계 결과이며, 인과관계를 보여주지 않는다.",
        "",
        "## 그림 2. 정보화 전담조직 보유 형태별 AI 이용 비율",
        f"- 조직 보유 형태별 AI 이용률을 비교한 결과, 상대적으로 높은 집단은 `{', '.join(fig2_top)}`로 나타났다. 다만 집단 간 차이는 구성비와 응답 분포의 영향을 함께 받을 수 있으므로 서술적 비교 수준에서만 해석해야 한다.",
        f"- 유효 표본 수: {fig2_valid_n:,}",
        "- 이 그림은 집단 간 기술통계 비교이며, 인과적 효과를 의미하지 않는다.",
    ]
    if fig2_missing_groups:
        lines.append(f"- 주의: 다음 조직 유형은 유효 관측치가 없어 막대가 0으로 표시되었다: {', '.join(fig2_missing_groups)}")
    lines.extend(
        [
            "",
            "## 그림 3. 정보화 전담조직 보유 형태별 프로세스 개선 상위응답 비율",
            f"- `proc_improve`의 상위응답(4~5점) 비율을 비교한 결과, 상대적으로 높은 집단은 `{', '.join(fig3_top)}`로 확인된다. 이는 예비적 집단 비교 결과이며, 다른 기업 특성 통제 전 단계의 분포 확인으로 이해하는 것이 적절하다.",
            f"- 유효 표본 수: {fig3_valid_n:,}",
            "- 이 그림은 집단 간 기술통계 비교이며, 인과적 증거가 아니다.",
        ]
    )
    if fig3_missing_groups:
        lines.append(f"- 주의: 다음 조직 유형은 유효 관측치가 없어 막대가 0으로 표시되었다: {', '.join(fig3_missing_groups)}")

    hist_note = fig4_df.iloc[0]["notes"]
    lines.extend(
        [
            "",
            "## 그림 4. 정보화 투자 비중 분포",
            "- 정보화 투자 비중은 우측 꼬리가 긴 분포를 보일 가능성이 있어, 평균뿐 아니라 중앙값과 분위수를 함께 확인할 필요가 있다. 히스토그램은 값의 집중 구간과 상위 꼬리의 존재 여부를 시각적으로 점검하기 위한 용도이다.",
            f"- 유효 표본 수: {fig4_valid_n:,}",
            "- 이 그림은 분포 점검을 위한 기술통계 결과이며, 인과관계를 보여주지 않는다.",
        ]
    )
    if display_cap is not None:
        lines.append(f"- 표시 범위 조정: 가독성을 위해 x축을 99백분위수({display_cap:.2f})까지로 제한했으며, 이는 표시용 조정일 뿐 원자료 자체는 변경하지 않았다.")
    else:
        lines.append("- 표시 범위 조정: 히스토그램은 전체 관측 범위를 그대로 사용했다.")
    if isinstance(hist_note, str) and hist_note:
        lines.append(f"- 요약 메모: {hist_note}")

    NOTES_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = load_data()

    fig1_df, fig1_valid_n = build_proc_distribution(df)
    fig2_df, fig2_valid_n, fig2_missing_groups = build_group_rate(df, "ai_use", "fig2")
    fig3_df, fig3_valid_n, fig3_missing_groups = build_group_rate(df, "proc_high", "fig3")
    fig4_df, fig4_valid_n, display_cap = build_hist_summary(df)

    summary_columns = [
        "figure_id",
        "variable",
        "group_code",
        "group_label",
        "valid_n",
        "positive_n",
        "percentage",
        "count",
        "mean",
        "median",
        "p25",
        "p75",
        "min",
        "max",
        "p95",
        "p99",
        "notes",
    ]

    for column in summary_columns:
        for frame in [fig1_df, fig2_df, fig3_df, fig4_df]:
            if column not in frame.columns:
                frame[column] = pd.NA
    summary_df = pd.concat([fig1_df[summary_columns], fig2_df[summary_columns], fig3_df[summary_columns], fig4_df[summary_columns]], ignore_index=True)
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    draw_distribution_bar(fig1_df, FIG1_PATH)
    draw_group_rate_bar(fig2_df, FIG2_PATH, "AI use rate by informationization organization type", "AI use rate (%)")
    draw_group_rate_bar(
        fig3_df,
        FIG3_PATH,
        "High process improvement rate by informationization organization type",
        "High proc_improve rate (%)",
    )
    draw_histogram(df, FIG4_PATH, display_cap)

    write_notes(
        fig1_df,
        fig2_df,
        fig3_df,
        fig4_df,
        fig1_valid_n,
        fig2_valid_n,
        fig3_valid_n,
        fig4_valid_n,
        fig2_missing_groups,
        fig3_missing_groups,
        display_cap,
    )

    print(f"Saved Figure 1: {FIG1_PATH}")
    print(f"Saved Figure 2: {FIG2_PATH}")
    print(f"Saved Figure 3: {FIG3_PATH}")
    print(f"Saved Figure 4: {FIG4_PATH}")
    print(f"Saved summary CSV: {SUMMARY_PATH}")
    print(f"Saved notes markdown: {NOTES_PATH}")


if __name__ == "__main__":
    main()
