from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "merged" / "nia_2020_2024_merged.csv"
OUTPUT_DIR = BASE_DIR / "output" / "figures"

FIG1_PATH = OUTPUT_DIR / "fig_selected_1_ai_use_by_it_org_type.png"
FIG2_PATH = OUTPUT_DIR / "fig_selected_2_proc_high_by_it_org_type.png"
SUMMARY_PATH = OUTPUT_DIR / "figure_summary_stats_selected.csv"
NOTES_PATH = OUTPUT_DIR / "figure_notes_selected.md"

GROUP_ORDER = [0, 1, 2, 3, 4]
GROUP_LABELS = {
    0: "No org",
    1: "Internal",
    2: "Mixed-duty",
    3: "Outsourced",
    4: "Multiple",
}


def load_data() -> pd.DataFrame:
    """Read the merged dataset and coerce analysis columns safely to numeric."""
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig", dtype=str, keep_default_na=False, na_filter=False)

    for col in ["it_org_type", "ai_use", "proc_improve"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace("", pd.NA), errors="coerce")
        else:
            df[col] = pd.NA

    df["proc_high"] = pd.NA
    valid_proc = df["proc_improve"].isin([1, 2, 3, 4, 5])
    df.loc[valid_proc & df["proc_improve"].isin([4, 5]), "proc_high"] = 1
    df.loc[valid_proc & df["proc_improve"].isin([1, 2, 3]), "proc_high"] = 0
    df["proc_high"] = pd.to_numeric(df["proc_high"], errors="coerce")
    return df


def build_group_summary(df: pd.DataFrame, outcome_col: str, figure_id: str, variable_label: str) -> tuple[pd.DataFrame, int, list[str]]:
    """Create grouped N / positive count / percentage table in fixed category order."""
    work = df[df["it_org_type"].notna()].copy()
    work = work[work["it_org_type"].isin(GROUP_ORDER)]
    work = work[work[outcome_col].notna()]

    total_valid_n = len(work)
    group_stats = (
        work.groupby("it_org_type", dropna=False)[outcome_col]
        .agg(valid_n="count", positive_n="sum")
        .reset_index()
    )

    template = pd.DataFrame({"group_code": GROUP_ORDER})
    summary = template.merge(group_stats, how="left", left_on="group_code", right_on="it_org_type").drop(columns=["it_org_type"])
    summary["valid_n"] = summary["valid_n"].fillna(0).astype(int)
    summary["positive_n"] = summary["positive_n"].fillna(0).astype(int)
    summary["group_code"] = summary["group_code"].astype(int)
    summary["percentage"] = summary.apply(
        lambda row: (row["positive_n"] / row["valid_n"] * 100) if row["valid_n"] > 0 else 0.0,
        axis=1,
    )
    summary["group_label"] = summary["group_code"].map(GROUP_LABELS)
    summary["figure_id"] = figure_id
    summary["variable"] = variable_label

    absent_groups = summary.loc[summary["valid_n"] == 0, "group_label"].tolist()
    summary = summary[
        ["figure_id", "variable", "group_code", "group_label", "valid_n", "positive_n", "percentage"]
    ]
    return summary, total_valid_n, absent_groups


def draw_bar_chart(summary: pd.DataFrame, title: str, y_label: str, output_path: Path) -> None:
    """Draw a single academic-style bar chart with percentage labels."""
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_labels = summary["group_label"].tolist()
    y_values = summary["percentage"].tolist()
    bars = ax.bar(x_labels, y_values, color="#4C78A8", edgecolor="black", linewidth=0.8, width=0.65)

    ax.set_title(title, fontsize=13, pad=12)
    ax.set_xlabel("Informationization organization type", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_ylim(0, max(y_values + [5]) * 1.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(axis="x", labelrotation=0)

    for bar, pct in zip(bars, y_values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(y_values + [5]) * 0.02,
            f"{pct:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_notes(
    fig1_summary: pd.DataFrame,
    fig2_summary: pd.DataFrame,
    fig1_valid_n: int,
    fig2_valid_n: int,
    fig1_absent: list[str],
    fig2_absent: list[str],
) -> None:
    """Write short Korean interpretation notes for both figures."""
    fig1_sorted = fig1_summary.sort_values("percentage", ascending=False)
    fig2_sorted = fig2_summary.sort_values("percentage", ascending=False)

    fig1_top = fig1_sorted.iloc[0]["group_label"]
    fig1_bottom = fig1_sorted.iloc[-1]["group_label"]
    fig2_top = fig2_sorted.iloc[0]["group_label"]
    fig2_bottom = fig2_sorted.iloc[-1]["group_label"]

    lines: list[str] = []
    lines.append("# Figure Notes")
    lines.append("")
    lines.append("## 그림 1. 정보화 전담조직 보유 형태별 AI 이용 비율")
    lines.append(
        f"{fig1_top} 집단의 AI 이용 비율이 상대적으로 높고, {fig1_bottom} 집단은 비교적 낮게 나타난다. "
        "다만 이는 단순 집단 비교 결과이므로 다른 기업 특성이나 연도 차이를 통제한 인과적 해석으로 볼 수는 없다."
    )
    lines.append(f"- 유효 표본수: {fig1_valid_n:,}")
    if fig1_absent:
        lines.append(f"- 참고: 다음 범주는 유효 관측치가 없어 0%로 표시됨: {', '.join(fig1_absent)}")
    lines.append("- 주의: 본 그림은 기술통계적 group comparison이며, 인과효과를 의미하지 않음.")
    lines.append("")
    lines.append("## 그림 2. 정보화 전담조직 보유 형태별 프로세스 개선 상위응답 비율")
    lines.append(
        f"{fig2_top} 집단에서 프로세스 개선 상위응답 비율이 상대적으로 높고, {fig2_bottom} 집단은 비교적 낮게 보인다. "
        "하지만 이 역시 단순 분포 비교이므로 전담조직 보유 형태의 효과로 직접 해석하기에는 주의가 필요하다."
    )
    lines.append(f"- 유효 표본수: {fig2_valid_n:,}")
    if fig2_absent:
        lines.append(f"- 참고: 다음 범주는 유효 관측치가 없어 0%로 표시됨: {', '.join(fig2_absent)}")
    lines.append("- 주의: 본 그림은 기술통계적 group comparison이며, 인과효과를 의미하지 않음.")
    lines.append("")

    NOTES_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    # Figure 1: AI use rate by organization type
    fig1_df = df[df["it_org_type"].notna() & df["ai_use"].notna()].copy()
    fig1_summary, fig1_valid_n, fig1_absent = build_group_summary(
        fig1_df,
        outcome_col="ai_use",
        figure_id="fig_selected_1",
        variable_label="ai_use",
    )
    draw_bar_chart(
        fig1_summary,
        title="AI use rate by informationization organization type",
        y_label="AI use rate (%)",
        output_path=FIG1_PATH,
    )

    # Figure 2: high process improvement rate by organization type
    fig2_df = df[df["it_org_type"].notna() & df["proc_improve"].notna()].copy()
    fig2_df = fig2_df[fig2_df["proc_high"].notna()].copy()
    fig2_summary, fig2_valid_n, fig2_absent = build_group_summary(
        fig2_df,
        outcome_col="proc_high",
        figure_id="fig_selected_2",
        variable_label="proc_high",
    )
    draw_bar_chart(
        fig2_summary,
        title="High process improvement rate by informationization organization type",
        y_label="High process improvement rate (%)",
        output_path=FIG2_PATH,
    )

    summary_all = pd.concat([fig1_summary, fig2_summary], ignore_index=True)
    summary_all.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    write_notes(fig1_summary, fig2_summary, fig1_valid_n, fig2_valid_n, fig1_absent, fig2_absent)

    print(f"Figure 1 saved to: {FIG1_PATH}")
    print(f"Figure 2 saved to: {FIG2_PATH}")
    print(f"Summary CSV saved to: {SUMMARY_PATH}")
    print(f"Notes file saved to: {NOTES_PATH}")


if __name__ == "__main__":
    main()
