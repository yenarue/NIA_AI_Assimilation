# Table 7. 진단 및 검증 요약표

| 진단 항목 | 대상 모형/변수 | 진단 방법 | 주요 결과 | 판단 | 대응 | 보고 위치 |
| --- | --- | --- | --- | --- | --- | --- |
| 이분산 | 주모형 H1, 주모형 H3, effect_average 강건성 DV 모형 | Breusch-Pagan test, White test, 잔차-적합값 그림 | BP 유의 모형 3개, White 유의 모형 3개 | 이분산 가능성 고려 필요 | 주요 회귀표에서 HC3 robust standard error 사용 | 본문 진단 요약 및 부록 Table 7A |
| 다중공선성 | 주모형 H3 및 확장모형 D 설계행렬 | Variance Inflation Factor (VIF) | 주모형 최대 VIF=4.047 (it_org_any:ai_use_sum); 확장모형 최대 VIF=9.178 (it_invest_sum) | 일부 변수 주의 | 확장모형은 부록용 탐색분석으로 제시하고 핵심 해석은 주모형 중심 | 부록 VIF 진단표 |
| 과분산 | ai_use_sum | 분산/평균 비율, Poisson Pearson chi-square / df | 평균=0.877, 분산/평균=1.826, Pearson chi2/df=1.738 | 과분산 가능성 있음 | Poisson과 Negative Binomial 대안모형 함께 검토 | 대안모형 및 진단 요약 |
| 평행추세 | 2024년 기업 단면자료 구조 | 연도 변수 및 반복 기업 ID 구조 확인 | 적용하지 않음 | 평행추세 검정 해당 없음 | 단면자료 기반 예비적 연관성 분석으로 해석 제한 | 본문 한계 및 확인 필요 사항 |
| 순서형 DV 대응 | effect_proc_improve | OLS 주모형과 Ordered Logit 대안모형 비교 | Ordered Logit 대안모형을 별도 노트북에서 검토 | 순서형 척도 특성 반영 필요 | 종속변수 effect_proc_improve가 순서형이므로 Ordered Logit 대안모형을 별도 검토 | 대안모형/강건성 분석 표 |