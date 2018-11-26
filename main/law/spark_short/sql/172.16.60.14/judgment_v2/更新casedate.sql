update adjudication_xingshi_etl_v2 a ,casedate_error_uuid_old_xingshi b set a.casedate = b.casedate where a.uuid = b.uuid;


update judgment_etl_v2 a ,casedate_error_uuid_old_judgment b set a.casedate = b.casedate where a.uuid = b.uuid;


create table casedate_error_uuid_old_union_2_tables like casedate_error_uuid_old_judgment;
insert into casedate_error_uuid_old_union_2_tables select * from casedate_error_uuid_old_xingshi;
insert into casedate_error_uuid_old_union_2_tables select * from casedate_error_uuid_old_judgment;


select id,doc_footer,judge_result,court_idea from casedate_error_uuid_old_union_2_tables   
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;


select id,doc_footer,judge_result,court_idea from casedate_error_uuid_old_union_2_tables   
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;

create table t1 as select * from casedate_error_uuid_old_union_2_tables a,


update casedate_error_uuid_old_union_2_tables a,adjudication_xingshi_etl_v2_court_cate_judge_footer b 
set a.doc_footer = b.doc_footer,
a.judge_result = b.judge_result,
a.court_idea = b.court_idea where a.uuid = b.uuid;

update casedate_error_uuid_old_union_2_tables a,adjudication_xingshi_uuid_law_id_v2 b 
set a.law_id = b.law_id  where a.uuid = b.uuid;

select a.law_id,b.law_id from casedate_error_uuid_old_union_2_tables a,adjudication_xingshi_uuid_law_id_v2 b
where a.uuid = b.uuid;

select * from casedate_error_uuid_old_union_2_tables a,adjudication_xingshi_etl_v2_court_cate_judge_footer b where a.uuid = b.uuid;

update casedate_error_uuid_old_union_2_tables a,judgment_etl_v2_court_cate_judge_footer b 
set a.doc_footer = b.doc_footer,
a.judge_result = b.judge_result,
a.court_idea = b.court_idea where a.uuid = b.uuid;

update casedate_error_uuid_old_union_2_tables a,judgment_uuid_law_id_v2 b 
set a.law_id = b.law_id  where a.uuid = b.uuid;



create table casedate_null_null_judgment as select id,uuid,casedate from casedate_error_uuid_old_union_2_tables where casedate = "";

create table casedate_error_uuid_2018_2_tables as select * from casedate_error_uuid_2018_judgment
insert into  casedate_error_uuid_2018_2_tables select * from casedate_error_uuid_xingshi_2018


create table uuids as select uuid from casedate_error_uuid_2018_judgment
insert into uuids select uuid from casedate_error_uuid_xingshi_2018

