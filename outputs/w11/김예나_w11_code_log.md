# 11주차 작업 로그

기준 기간: 2026-05-11 ~ 2026-05-17

| 날짜 | 작업 영역 | 주요 파일/폴더 | 처리단계 | 작업 내용 | 산출물/결과 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-05-11 | 기초 분포/기술통계 | `outputs/06_distribution_figures` | descriptive analysis | 핵심 변수 분포, 산업/기업규모/지역/기업유형 빈도, DMI 구성요소 기술통계 정리 | CSV/XLSX 표 및 분포 그림 갱신 | 11주차 분석 표·그림의 기초 통계 자료 |
| 2026-05-11 | 모델 진단 | `outputs/10_model_diagnostics` | diagnostics | VIF, 이분산성 검정, 모형 적합도, 잔차 진단 그림 생성 | `model_diagnostics_summary.xlsx`, VIF/진단표, 잔차 그림 | Table 2 VIF 및 모형 신뢰성 점검 근거 |
| 2026-05-16 | 본분석 모델 | `outputs/08_main_model` | main model | H1~H3 및 통합모형 재추정, 핵심 계수·적합도 표 정리 | `main_model_summary.xlsx`, `main_model_results_wide.csv/xlsx` | Table 3 재계산의 기반 |
| 2026-05-16 | 대안/강건성 분석 | `outputs/09_alternative_robustness_models` | robustness | Weighted OLS, binary logit, ordered logit, 대안 DV/AI 측정치 결과 정리 | 강건성 표, 적합도 표, 해석 메모 | Table 6·7 작성 근거 |
| 2026-05-17 | 예비 연관성 표 | `outputs/07_preliminary_association` | preliminary tables | 상관관계, 교차표, 그룹 평균, 보조 기술통계 갱신 | `preliminary_association_summary.xlsx`, `auxiliary_descriptive_stats.*` | 본문/부록용 사전 점검 표 |
| 2026-05-17 | 11주차 본문 표 | `outputs/w11` | manuscript tables | Table 2~7용 상관/VIF, 본분석, 기업규모 이질성, 산업 이질성, 강건성, 대안 DV 표 생성 | `table2_corr_vif`, `table3_main_models`, `table4~7` CSV/Markdown/TXT/XLSX | 11주차 핵심 산출물 |
| 2026-05-17 | 11주차 그림 | `outputs/w11/figures` | manuscript figures | AI×IT조직 예측값 그림, AI×DMI 한계효과 그림 생성 | `figure1_ai_itorg_predicted.png/pdf`, `figure2_ai_dmi_marginal_effect.png/pdf` | 본문 Figure 1~2 후보 |
| 2026-05-17 | 해석 메모 정리 | `outputs/w11` | interpretation | 표별 해석 문장과 manuscript interpretation 작성 | `*_interpretation.txt`, `*_markdown.txt`, `*_model_summaries.txt` | 논문 작성에 바로 붙일 수 있는 문장 초안 |

## 요약

이번 주 작업의 중심은 11주차 원고용 Table 2~7과 Figure 1~2를 재계산·정리하고, 본분석/강건성/이질성 분석 결과를 해석 메모까지 연결한 것이다. 특히 `outputs/w11/`에 11주차 전용 산출물이 모여 있어 제출·공유용 로그의 기준 폴더로 사용할 수 있다.
