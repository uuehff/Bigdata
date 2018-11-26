select id,title,doc_footer,judge_result from adjudication_civil_etl_v2 
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%"  limit 100;
无结果；

select id,uuid,doc_footer,judge_result,court_idea from adjudication_civil_etl_v2 
where doc_footer like "%?%" or judge_result like "%?%" or court_idea like "%?%"  limit 100;
有结果；
select * from adjudication_civil_etl_v2 
where doc_footer like "%?%" or judge_result like "%?%" or court_idea like "%?%"  limit 100;


select id,doc_footer,judge_result from adjudication_xingshi_etl_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；

select id,doc_footer,judge_result,court_idea from adjudication_xingshi_etl_v2  
where court_idea like "%?%"  limit 100;
有结果；

create table casedate_error_uuid_old_xingshi as 
SELECT * from adjudication_xingshi_etl_v2 where SUBSTR(casedate,1,4) > 2018 ;
#6

create table casedate_error_uuid_old_civil as 
SELECT * from adjudication_civil_etl_v2 where SUBSTR(casedate,1,4) > 2018 ;
#53


create table casedate_error_uuid_xingshi_2018 as 
SELECT id,uuid,caseid,casedate from adjudication_xingshi_etl_v2 where casedate > "2018-07-27" ;
1;
create table casedate_error_uuid_civil_2018 as 
SELECT id,uuid,caseid,casedate from adjudication_civil_etl_v2 where casedate > "2018-07-27" ;
6;

-- SELECT id,uuid,caseid,casedate from adjudication_civil_etl_v2 where CHAR_LENGTH(casedate) > 1 and CHAR_LENGTH(casedate) < 5 ;
-- 

create  table adjudication_civil_etl_v2_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer
create  table adjudication_xingshi_etl_v2_judge_footer like laws_doc_administration.administration_etl_v2_court_cate_judge_footer

create table adjudication_xingshi_etl_v2_lawyer_id like adjudication_civil_etl_v2_lawyer_id;


update adjudication_civil_etl_v2 a ,casedate_error_uuid_old_civil b set a.casedate = b.casedate where a.uuid = b.uuid;
update adjudication_xingshi_etl_v2 a ,casedate_error_uuid_old_xingshi b set a.casedate = b.casedate where a.uuid = b.uuid;


select * from adjudication_civil_etl_v2_court_cate_judge_footer where uuid = "ec637a8a8a0f35fd9ec5723e498a74b9"

select id,doc_footer,judge_result,court_idea from adjudication_xingshi_etl_v2 where court_idea like "%?%"  limit 100;
