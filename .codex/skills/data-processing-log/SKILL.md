---
name: data-processing-log
description: 데이터 전처리 진행시, 작업  결과를 로그로 정리해서 알려주는 스킬
when_to_use: 사용자가 데이터 전처리/처리를 요청 하여 데이터 처리를 수행한 이후, 결과를 알려주는 응답의 맨 마지막에 해당 로그표를 출력한다.
---

# Data Processing Log

## 목적
데이터 전처리 및 처리 작업 이후, 사용자가 결과를 한눈에 파악하기 좋도록 로그표를 응답의 맨 마지막에 출력한다.

## 사용 방법
전처리 결과를 아래와 같은 column의 표로 정리한다 : 
- 파일명
- 변수명
- 처리단계
- 처리 전 상태
- 처리 내용
- 처리 이유
- 처리 후 상태
- 관측치 변화 (N)
- 비고

## 예시 
아래를 마크다운 표 형식으로 출력한다 : 

파일명	변수명	처리단계	처리 전 상태	처리 내용	처리 이유	처리 후 상태	관측치 변화 (N)	비고
nia_2024_featured.csv	it_org_type	feature engineering	원천 변수 3개 조합	규칙 기반 범주 변수 생성	연구용 파생변수 추가	0~4 범주형	row 수 변화 없음	기존 열과 재계산 결과 일치
nia_2024_featured.csv	it_invest_sum	feature engineering	0/1 더미 8개	합계 변수 생성	연구용 파생변수 추가	0~8 정수	row 수 변화 없음	결측 처리 0건
nia_2024_featured.csv	it_invest_high	feature engineering	it_invest_share numeric	<=3은 0, >=4는 1	연구용 파생변수 추가	0/1/NA	row 수 변화 없음	std4 사용 안 함
nia_2024_featured.csv	ai_use_sum	feature engineering	0/1 더미 10개	합계 변수 생성	연구용 파생변수 추가	0~10 정수	row 수 변화 없음	결측 처리 0건
nia_2024_featured.csv	ai_impl_sum	feature engineering	0/1 더미 6개	합계 변수 생성	연구용 파생변수 추가	0~6 정수	row 수 변화 없음	결측 처리 0건
nia_2024_featured.csv	ai_purpose_sum	feature engineering	0/1 더미 10개	합계 변수 생성	연구용 파생변수 추가	0~10 정수	row 수 변화 없음	결측 처리 0건
nia_2024_featured.csv	effect_average	feature engineering	1~5 리커트 6개	평균 변수 생성	연구용 파생변수 추가	1~5 평균값	row 수 변화 없음	반올림 없음
