| 파일명 | 변수명 | 처리단계 | 처리 전 상태 | 처리 내용 | 처리 이유 | 처리 후 상태 | 관측치 변화 (N) | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nia_2024_cleaned.csv | year | clean | 연속형/범주형 숫자 문자열 | year를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | industry | clean | 연속형/범주형 숫자 문자열 | industry_raw를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | industry_size | clean | 연속형/범주형 숫자 문자열 | industry_size_raw를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | firm_size | clean | 연속형/범주형 숫자 문자열 | firm_size_raw를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | region | clean | 연속형/범주형 숫자 문자열 | region_raw를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | firm_type | clean | 연속형/범주형 숫자 문자열 | firm_type_raw를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | weight | clean | 연속형/범주형 숫자 문자열 | weight_raw를 numeric으로 변환 | 분석용 숫자 변수 생성 | numeric/NA | 변화 없음 | 통제변수 및 가중치 유지 |
| nia_2024_cleaned.csv | it_org_any | clean | 1/2 응답 | it_org_any_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 1/2 yes-no 변환 |
| nia_2024_cleaned.csv | it_invest_any | clean | 1/2 응답 | it_invest_any_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 분산 없음 가능성 |
| nia_2024_cleaned.csv | mgmt_sys_any | clean | 1/2 응답 | mgmt_sys_any_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 1/2 yes-no 변환 |
| nia_2024_cleaned.csv | iot_use_any | clean | 1/2 응답 | iot_use_any_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 1/2 yes-no 변환 |
| nia_2024_cleaned.csv | cloud_use_any | clean | 1/2 응답 | cloud_use_any_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 1/2 yes-no 변환 |
| nia_2024_cleaned.csv | data_analysis_use_any | clean | 1/2 응답 | data_analysis_use_any_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 1/2 yes-no 변환 |
| nia_2024_cleaned.csv | ai_use | clean | 1/2 응답 | ai_use_raw: 1->1, 2->0, 그 외 NA | yes/no 문항을 0/1 분석 변수로 변환 | 0/1/NA numeric | 변화 없음 | 1/2 yes-no 변환 |
| nia_2024_cleaned.csv | it_org_internal | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_org_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 5853건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_org_mixed | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_org_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 5853건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_org_outsource | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_org_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 5853건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_hardware | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_software | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_sys_op | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_infra | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_op_salary | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_new_tech | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_rnd | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_invest_tech_train | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 it_invest_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 0건; 공백->NA 0건 |
| nia_2024_cleaned.csv | mgmt_sys_erp | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 mgmt_sys_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2484건; 공백->NA 0건 |
| nia_2024_cleaned.csv | mgmt_sys_crm | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 mgmt_sys_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2484건; 공백->NA 0건 |
| nia_2024_cleaned.csv | mgmt_sys_scm | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 mgmt_sys_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2484건; 공백->NA 0건 |
| nia_2024_cleaned.csv | mgmt_sys_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 mgmt_sys_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2484건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_security | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_customer_service | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_payment | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_production_process | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_logistics_inventory | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_energy_management | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_smart_building_office | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | iot_use_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 iot_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 4898건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_email | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_office_software | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_finance_accounting_app | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_erp | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_crm | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_security_software | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_collaboration_software | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_database_hosting | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_file_storage | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_computing_capacity | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_app_dev_test_deploy | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | cloud_use_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 cloud_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 2778건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_public_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_transaction_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_customer_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_social_media_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_web_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_sensor_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_location_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_satellite_data | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | data_analysis_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 data_analysis_use_any_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 6137건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_doc_info_collect | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_task_automation | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_decision_support | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_speech_to_text | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_gen_summarize_edit | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_image_video_recognition | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_ml_data_analysis | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_text_language_analysis | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_autonomous_mobility | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_use_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_marketing_sales | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_prod_service_improve | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_biz_process_org | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_logistics | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_security | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_accounting_finance | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_rnd_innovation | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_cost_reduction | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_customer_demand | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_purpose_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_impl_inhouse_dev | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_impl_modify_commercial | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_impl_modify_open_source | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_impl_buy_commercial | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_impl_vendor_contract | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | ai_impl_other | clean | 0/1/공백 혼재 | 1->1, 0->0, 공백은 ai_use_raw 비해당이면 0, 해당이면 NA | 비해당 응답을 결측이 아니라 0으로 해석 | 0/1/NA numeric | 변화 없음 | 상위문항 기반 처리; 공백->0 7139건; 공백->NA 0건 |
| nia_2024_cleaned.csv | it_org_type | clean | it_org_internal/mixed/outsource 0/1 조합 | 세 하위항목 조합으로 0~4 유형 생성 | 정보화 조직 유형 분석 변수 생성 | 0/1/2/3/4/NA numeric | 변화 없음 | 0=모두 0, 1=internal only, 2=mixed only, 3=outsource only, 4=둘 이상 |
| nia_2024_cleaned.csv | it_invest_share | clean | 숫자 문자열, 쉼표/공백/% 가능 | 쉼표, 공백, % 제거 후 numeric 변환 | 원 raw 값을 그대로 쓰는 투자비중 분석 변수 생성 | numeric/NA | 변화 없음 | it_invest_share_pct 생성 안 함 |
| nia_2024_cleaned.csv | it_invest_share_std4 | clean | it_invest_share_recoded_raw | it_invest_share_recoded_raw를 numeric으로 변환해 그대로 매핑 | 코드북의 REQ33 4범주 recoding 값을 표준화 변수로 사용 | 1/2/3/4/NA numeric | 변화 없음 | 1~4 외 값->NA 0건 |
| nia_2024_cleaned.csv | effect_proc_improve | clean | 1~5 리커트 | effect_proc_improve_raw를 1~5 numeric으로 유지 | midpoint 3을 포함한 순서형 응답 보존 | 1~5 numeric | 변화 없음 | 3은 정상 응답값, 이진화 없음 |
| nia_2024_cleaned.csv | effect_internal_cohesion | clean | 1~5 리커트 | effect_internal_cohesion_raw를 1~5 numeric으로 유지 | midpoint 3을 포함한 순서형 응답 보존 | 1~5 numeric | 변화 없음 | 3은 정상 응답값, 이진화 없음 |
| nia_2024_cleaned.csv | effect_decision_improve | clean | 1~5 리커트 | effect_decision_improve_raw를 1~5 numeric으로 유지 | midpoint 3을 포함한 순서형 응답 보존 | 1~5 numeric | 변화 없음 | 3은 정상 응답값, 이진화 없음 |
| nia_2024_cleaned.csv | effect_stakeholders | clean | 1~5 리커트 | effect_stakeholders_raw를 1~5 numeric으로 유지 | midpoint 3을 포함한 순서형 응답 보존 | 1~5 numeric | 변화 없음 | 3은 정상 응답값, 이진화 없음 |
| nia_2024_cleaned.csv | effect_innov_outcome | clean | 1~5 리커트 | effect_innov_outcome_raw를 1~5 numeric으로 유지 | midpoint 3을 포함한 순서형 응답 보존 | 1~5 numeric | 변화 없음 | 3은 정상 응답값, 이진화 없음 |
| nia_2024_cleaned.csv | effect_competitiveness | clean | 1~5 리커트 | effect_competitiveness_raw를 1~5 numeric으로 유지 | midpoint 3을 포함한 순서형 응답 보존 | 1~5 numeric | 변화 없음 | 3은 정상 응답값, 이진화 없음 |
| nia_2024_cleaned.csv | mgmt_sys_other_text | clean | 텍스트+공백 | mgmt_sys_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12009건 |
| nia_2024_cleaned.csv | iot_use_other_text | clean | 텍스트+공백 | iot_use_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12161건 |
| nia_2024_cleaned.csv | cloud_use_other_text | clean | 텍스트+공백 | cloud_use_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12203건 |
| nia_2024_cleaned.csv | data_analysis_other_text | clean | 텍스트+공백 | data_analysis_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12099건 |
| nia_2024_cleaned.csv | ai_use_other_text | clean | 텍스트+공백 | ai_use_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12172건 |
| nia_2024_cleaned.csv | ai_purpose_other_text | clean | 텍스트+공백 | ai_purpose_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12203건 |
| nia_2024_cleaned.csv | ai_impl_other_text | clean | 텍스트+공백 | ai_impl_other_text_raw의 공백/빈 문자열을 NA로 처리하고 텍스트는 유지 | 기타 텍스트 응답을 분석 가능한 clean 텍스트 열로 분리 | text/NA | 변화 없음 | clean 텍스트 열 생성; 공백->NA 12194건 |
| nia_2024_cleaned.csv | mgmt_sys_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
| nia_2024_cleaned.csv | iot_use_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
| nia_2024_cleaned.csv | cloud_use_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
| nia_2024_cleaned.csv | data_analysis_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
| nia_2024_cleaned.csv | ai_use_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
| nia_2024_cleaned.csv | ai_purpose_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
| nia_2024_cleaned.csv | ai_impl_other_text_raw | clean | 텍스트+공백 | raw 텍스트 열도 뒤쪽에 보존 | 원천 응답 추적 가능성 유지 | text/NA | 변화 없음 | raw 열 보존 |
