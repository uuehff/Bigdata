select id,doc_footer,judge_result from judgment_etl_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
有结果；

select id,doc_footer,judge_result from judgment_etl_v2  
where judge_result like "%u3000%" limit 100;
有结果；
select id,court_idea,doc_footer,judge_result from judgment_etl_v2  
where court_idea like "%u3000%" limit 100;
有结果；
======================================
select id,doc_footer,judge_result from judgment2_etl_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；



create table casedate_error_uuid_old_judgment as 
SELECT * from judgment_etl_v2 where SUBSTR(casedate,1,4) > 2018 ;
#5

create table casedate_error_uuid_old_judgment2 as 
SELECT * from judgment2_etl_v2 where SUBSTR(casedate,1,4) > 2018 ;
#无结果

create table casedate_error_uuid_2018 as 
SELECT id,uuid,caseid,casedate from judgment_etl_v2 where casedate > "2018-07-27" ;
26
create table casedate_error_uuid_2018_2 as 
SELECT id,uuid,caseid,casedate from judgment2_etl_v2 where casedate > "2018-07-27" ;
0



-- SELECT id,uuid,caseid,casedate from judgment_etl_v2 where CHAR_LENGTH(casedate) > 1 and CHAR_LENGTH(casedate) < 5 ;
-- 

select id,uuid_old,doc_footer,judge_result,court_idea from judgment_etl_v2  
where judge_type = "判决" and (judge_result like "%u3000%" or court_idea like "%u3000%") limit 100;

select id,uuid_old,doc_footer,judge_result,court_idea from judgment_etl_v2  
where judge_type = "判决" and doc_footer like "%u3000%" limit 100;


select count(*) from judgment_etl_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%";
#2039503

select * from judgment_etl_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 10;



update judgment_etl_v2 a,doc_footer_u3000 b set 
a.court_idea = b.court_idea,
a.judge_result = b.judge_result,
a.doc_footer = b.doc_footer where a.uuid = b.uuid;


create  table judgment_etl_v2_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;
create  table judgment2_etl_v2_court_cate_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer;

create table judgment_etl_v2_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;
create table judgment2_etl_v2_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;


update judgment_etl_v2 a ,casedate_error_uuid_old_judgment b set a.casedate = b.casedate where a.uuid = b.uuid;

create table a as SELECT id ,uuid,type from judgment2_etl_v2 WHERE id < 5;
create table b as SELECT id ,uuid,type from judgment2_etl_v2 WHERE id < 5;
create table c as SELECT id ,uuid,type from judgment2_etl_v2 WHERE id < 5;
create table d as SELECT id ,uuid,type from judgment2_etl_v2 WHERE id < 5;

select * from judgment_etl_v2_court_cate_judge_footer where court_cate = "最高" limit 100;
