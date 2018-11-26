select id,doc_footer,judge_result from judgment_new_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" limit 100;
无结果；


create table casedate_error_uuid_old as 
SELECT * from judgment_new_v2 where SUBSTR(casedate,1,4) > 2018 ;

#32


create table casedate_error_uuid_2018 as 
SELECT id,uuid,caseid,casedate from judgment_new_v2 where casedate > "2018-07-27" ;


create  table judgment_new_v2_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer
-- create  table civil_etl_v2_800w_01_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
-- create  table civil_etl_v2_800w_02_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;


create table judgment_new_v2_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;


select id,party_info,court_idea,judge_type from judgment_new_v2 where id < 100

update judgment_new_v2 a ,casedate_error_uuid_old b set a.casedate = b.casedate where a.uuid = b.uuid;
select * from judgment_new_v2_court_cate_judge_footer where court_cate = "最高" limit 100;
