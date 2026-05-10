| 파일명 | 변수명 | 처리단계 | 처리 전 상태 | 처리 내용 | 처리 이유 | 처리 후 상태 | 관측치 변화 (N) | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nia_2024_featured.csv | it_org_type | feature engineering | 원천 변수 3개 조합 | 규칙 기반 범주 변수 생성 | 연구용 파생변수 추가 | 0~4 범주형 | row 수 변화 없음 | 기존 열과 재계산 결과 일치 |
| nia_2024_featured.csv | it_invest_sum | feature engineering | 0/1 더미 8개 | 8개 투자항목 합계 변수 생성 | 연구용 파생변수 추가 | 0~8 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | it_invest_high | feature engineering | it_invest_share numeric | it_invest_share<=3이면 0, >=4이면 1 | 연구용 파생변수 추가 | 0/1/NA | row 수 변화 없음 | it_invest_share_std4 사용 안 함 |
| nia_2024_featured.csv | mgmt_sys_sum | feature engineering | 0/1 더미 4개 | mgmt_sys_any를 제외한 4개 경영정보시스템 하위항목 합계 변수 생성 | 디지털 관리 인프라 이용 폭 측정 | 0~4 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | iot_use_sum | feature engineering | 0/1 더미 8개 | iot_use_any를 제외한 8개 IoT 이용유형 합계 변수 생성 | IoT 이용 폭 측정 | 0~8 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | cloud_use_sum | feature engineering | 0/1 더미 12개 | cloud_use_any를 제외한 12개 클라우드 이용유형 합계 변수 생성 | 클라우드 이용 폭 측정 | 0~12 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | data_analysis_sum | feature engineering | 0/1 더미 9개 | data_analysis_use_any를 제외한 9개 데이터 분석 유형 합계 변수 생성 | 데이터 분석 활용 폭 측정 | 0~9 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | dmi | feature engineering | mgmt_sys_sum, iot_use_sum, cloud_use_sum, data_analysis_sum | 네 개 디지털 관리/기술 활용 합계 변수를 합산 | Digital Management Infrastructure 종합 지표 생성 | 0~33 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | ai_use_sum | feature engineering | 0/1 더미 10개 | 10개 AI 이용유형 합계 변수 생성 | 연구용 파생변수 추가 | 0~10 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | ai_impl_sum | feature engineering | 0/1 더미 6개 | 6개 AI 이용형태 합계 변수 생성 | 연구용 파생변수 추가 | 0~6 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | ai_purpose_sum | feature engineering | 0/1 더미 10개 | 10개 AI 이용목적 합계 변수 생성 | 연구용 파생변수 추가 | 0~10 정수 | row 수 변화 없음 | 하나라도 결측이면 NA; 결측 처리 0건 |
| nia_2024_featured.csv | effect_average | feature engineering | 1~5 리커트 6개 | 6개 효과 변수 평균 생성 | 연구용 파생변수 추가 | 1~5 평균값 | row 수 변화 없음 | 소수점 반올림 없음; 결측 처리 0건 |
