# 분포 확인 그림 해석 메모

- 사용 데이터 파일: `working/analysis/nia_2024_analysis_total.csv`
- 전체 N: 12,203

## Figure 1. fig1_effect_proc_improve_distribution.png
- 프로세스 개선 효과는 4점 응답이 49.5%로 가장 많고, 4점 이상 응답은 74.7%로 전반적으로 높은 값에 집중되어 있다. 그림 생성 시 제외된 결측은 0건이다.

## Figure 2. fig2_effect_by_it_org_boxplot.png
- 정보화 담당 체계 보유 기업의 프로세스 개선 효과 평균은 4.100점, 미보유 기업은 3.838점으로 보유 기업이 0.262점 높다. 그림 생성 시 제외된 결측은 0건이다.

## Figure 3. fig3_ai_use_sum_by_it_org.png
- 정보화 담당 체계 보유 기업의 AI 활용 유형 개수 평균은 1.022개, 미보유 기업은 0.720개로 보유 기업이 0.302개 높다. 그림 생성 시 제외된 결측은 0건이다.

## Figure 4. fig4_interaction_it_org_ai_use_effect.png
- AI 활용 유형 0개 집단에서 정보화 담당 체계 보유-미보유 평균 차이는 0.130점이고, 2개 이상 집단에서는 0.397점으로 나타났다. 이는 AI 활용 수준별로 정보화 담당 체계와 프로세스 개선 효과의 관계가 달라지는지 시각적으로 점검하기 위한 결과이며, 제외된 결측은 0건이다.

## Figure A1. figA1_ai_use_sum_distribution.png
- AI 활용 유형 개수는 0개가 58.5%로 가장 많고 평균은 0.877개이다. 분산/평균 비율은 1.826로 1보다 커 카운트형 대안모형 검토가 필요하며, 제외된 결측은 0건이다.

## Figure A2. figA2_it_invest_sum_distribution.png
- 정보화 투자 항목 개수는 3개가 26.6%로 가장 높은 비중을 보이며, 평균은 3.201개이다. 그림 생성 시 제외된 결측은 0건이다.

## Figure A3. figA3_firm_size_distribution.png
- 기업 규모는 10-49명 기업이 46.4%로 가장 많고, 249명 이하 기업이 전체의 77.4%를 차지한다. 그림 생성 시 제외된 결측은 0건이다.

## Figure A4. figA4_industry_distribution.png
- 업종별로는 제조업이 22.7%로 가장 많고, 상위 3개 업종의 합계 비중은 45.2%이다. 그림 생성 시 제외된 결측은 0건이다.

## 확인 필요 사항
- 요청 변수 8개가 모두 존재하며, 코드북에서 firm_size와 industry 라벨을 확인했다.
