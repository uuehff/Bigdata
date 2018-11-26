select id,doc_footer,judge_result from judgment_zhangye_400w_v2_01  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；
select id,doc_footer,judge_result from judgment_zhangye_400w_v3_03  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；

=======================================================
judgment_zhangye_civil_v2_result
judgment_zhangye_civil_v3_result
judgment_zhangye_xingshi_v2_result
judgment_zhangye_xingshi_v3_result
judgment_zhangye_xingzheng_v2_result
judgment_zhangye_xingzheng_v3_result
judgment_zhangye_zhixing_v2_result
judgment_zhangye_zhixing_v3_result



create table casedate_error_uuid_civil_2018 as 
SELECT id,uuid,caseid,casedate from judgment_zhangye_civil_v2_result where casedate > "2018-07-27" ;
空
SELECT id,uuid,caseid,casedate from judgment_zhangye_civil_v3_result where casedate > "2018-07-27" ;
空
.
.
.
create table casedate_error_uuid_civil_2018 as 
SELECT id,uuid,caseid,casedate from judgment_zhangye_zhixing_v3_result where casedate > "2018-07-27" ;
空
都为空；


==========================================
select table_name 
from information_schema.tables 
where table_schema='laws_doc_zhangye_v2' and table_name like "%result"
judgment_zhangye_civil_v2_result
judgment_zhangye_civil_v3_result
judgment_zhangye_xingshi_v2_result
judgment_zhangye_xingshi_v3_result
judgment_zhangye_xingzheng_v2_result
judgment_zhangye_xingzheng_v3_result
judgment_zhangye_zhixing_v2_result
judgment_zhangye_zhixing_v3_result


create table casedate_error_uuid_old_civil_v2_result as 
SELECT * from judgment_zhangye_civil_v2_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_civil_v3_result as 
SELECT * from judgment_zhangye_civil_v3_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_xingshi_v2_result as 
SELECT * from judgment_zhangye_xingshi_v2_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_xingshi_v3_result as 
SELECT * from judgment_zhangye_xingshi_v3_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_xingzheng_v2_result as 
SELECT * from judgment_zhangye_xingzheng_v2_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_xingzheng_v3_result as 
SELECT * from judgment_zhangye_xingzheng_v3_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_zhixing_v2_result as 
SELECT * from judgment_zhangye_zhixing_v2_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；
create table casedate_error_uuid_old_zhixing_v3_result as 
SELECT * from judgment_zhangye_zhixing_v3_result where SUBSTR(casedate,1,4) > 2018 ;
无结果；

==============================================================
judgment_zhangye_civil_v2_result
judgment_zhangye_civil_v3_result
judgment_zhangye_xingshi_v2_result
judgment_zhangye_xingshi_v3_result
judgment_zhangye_xingzheng_v2_result
judgment_zhangye_xingzheng_v3_result
judgment_zhangye_zhixing_v2_result
judgment_zhangye_zhixing_v3_result


create  table judgment_zhangye_civil_v2_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_civil_v3_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_xingshi_v2_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_xingshi_v3_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_xingzheng_v2_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_xingzheng_v3_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_zhixing_v2_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment_zhangye_zhixing_v3_result_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;

select max(id) from judgment_zhangye_civil_v2_result;
#7647111
select max(id) from judgment_zhangye_civil_v3_result;
#8606165
select min(id),max(id) from judgment_zhangye_xingshi_v2_result;
15,7644815
select min(id),max(id) from judgment_zhangye_xingshi_v3_result;
33,8606017
select max(id) from judgment_zhangye_xingzheng_v2_result;
7638999
select max(id) from judgment_zhangye_xingzheng_v3_result;
8606332
select max(id) from judgment_zhangye_zhixing_v2_result;
7641569
select max(id) from judgment_zhangye_zhixing_v3_result;
8606933

=======================================
create table judgment_zhangye_civil_v2_v3_result_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;
create table judgment_zhangye_xingshi_v2_v3_result_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;
create table judgment_zhangye_xingzheng_v2_v3_result_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;
create table judgment_zhangye_zhixing_v2_v3_result_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;
==========================================================






