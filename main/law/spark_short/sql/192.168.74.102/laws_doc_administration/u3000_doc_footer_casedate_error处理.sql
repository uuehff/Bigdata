select id,doc_footer,judge_result from administration_etl_v2  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；


create table casedate_error_uuid_old as 
SELECT * from administration_etl_v2 where SUBSTR(casedate,1,4) > 2018 ;
#1

create table casedate_error_uuid_2018 as 
SELECT id,uuid,caseid,casedate from administration_etl_v2 where casedate > "2018-07-27" ;
1

-- SELECT id,uuid,caseid,casedate from administration_etl_v2 where CHAR_LENGTH(casedate) > 1 and CHAR_LENGTH(casedate) < 5 ;
-- 

select * from administration_etl_v2 where court_idea like "%书记员%" limit 100

create table judge_footer_judge_result_court_idea like administration_etl_v2;
create table administration_etl_v2_judge_footer like judge_footer_judge_result_court_idea;

select * from administration_etl_v2_court_cate_judge_footer where court_cate is null limit 100



create table administration_etl_v2_lawyer_id like laws_doc_adjudication.adjudication_civil_etl_v2_lawyer_id;

update administration_etl_v2 a ,casedate_error_uuid_old b set a.casedate = b.casedate where a.uuid = b.uuid;

