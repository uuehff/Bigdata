create table judgment_zhangye_400w_v2_01 like laws_doc_implement.implement_civil_etl_v2;


create table judgment_zhangye_civil_v2 like judgment_zhangye_400w_v2_01;
create table judgment_zhangye_xingshi_v2 like judgment_zhangye_civil_v2;
create table judgment_zhangye_xingzheng_v2 like judgment_zhangye_civil_v2;
create table judgment_zhangye_zhixing_v2 like judgment_zhangye_civil_v2;



create table judgment_zhangye_xingshi_v2_result like tt;
create table judgment_zhangye_civil_v2_result like tt;
create table judgment_zhangye_xingzheng_v2_result like tt;
create table judgment_zhangye_zhixing_v2_result like tt;



create table uuid_law_id_zhangye_xingshi_v2 like laws_doc_new.judgment_new_uuid_law_id_v2;
create table uuid_law_id_zhangye_civil_v2 like laws_doc_new.judgment_new_uuid_law_id_v2;
create table uuid_law_id_zhangye_xingzheng_v2 like laws_doc_new.judgment_new_uuid_law_id_v2;
create table uuid_law_id_zhangye_zhixing_v2 like laws_doc_new.judgment_new_uuid_law_id_v2;



create table judgment_zhangye_400w_v3_01 like judgment_zhangye_400w_v2_01;
create table judgment_zhangye_400w_v3_02 like judgment_zhangye_400w_v2_01;
create table judgment_zhangye_400w_v3_03 like judgment_zhangye_400w_v2_01;

create table v3_01_uuid as select uuid,uuid_old from judgment_zhangye_400w_v3_01;


create table judgment_zhangye_civil_v3 like judgment_zhangye_civil_v2_result;
create table judgment_zhangye_xingshi_v3 like judgment_zhangye_civil_v3;
create table judgment_zhangye_xingzheng_v3 like judgment_zhangye_civil_v3;
create table judgment_zhangye_zhixing_v3 like judgment_zhangye_civil_v3;

create table judgment_zhangye_xingshi_v3_result like judgment_zhangye_xingshi_v2_result;
create table judgment_zhangye_civil_v3_result like judgment_zhangye_xingshi_v2_result;
create table judgment_zhangye_xingzheng_v3_result like judgment_zhangye_xingshi_v2_result;
create table judgment_zhangye_zhixing_v3_result like judgment_zhangye_xingshi_v2_result;


create table uuid_law_id_zhangye_xingshi_v3 like uuid_law_id_zhangye_xingshi_v2;
create table uuid_law_id_zhangye_civil_v3 like uuid_law_id_zhangye_xingshi_v2;
create table uuid_law_id_zhangye_xingzheng_v3 like uuid_law_id_zhangye_xingshi_v2;
create table uuid_law_id_zhangye_zhixing_v3 like uuid_law_id_zhangye_xingshi_v2;

===================================================
select max(id) from judgment_zhangye_civil_v2_result;

select * from judgment_zhangye_xingzheng_v3_result where uuid = "00012cf3-00db-430d-92df-a7f400350cc3"