
create table imp_other_etl4 like imp_other_etl1;

insert into imp_other_etl1 select * from imp_other_etl3;

alter table imp_other_etl1 rename imp_other_etl;

alter table imp_other_etl
add caseid varchar(80),
add title varchar(220),
add court varchar(255),
add court_uid varchar(255),
add lawlist text,
add law_id text,
add casedate varchar(255),
add reason_type varchar(255),
add type varchar(255),
add judge_type varchar(255),
add reason varchar(255),
add reason_uid varchar(255),
add province varchar(250),
add plt_claim mediumtext,
add dft_rep mediumtext,
add crs_exm mediumtext;

update imp_other_etl a ,imp_other_part b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.type = b.type,
 a.judge_type = b.judge_type,
 a.reason_type = "执行",
 a.reason = "其他执行"  
 where a.id = b.id;

V2处理======================================

create table imp_other_etl_v2 like laws_doc_implement.implement_civil_etl_v2;
create table imp_other_etl_v3 like laws_doc_implement.implement_civil_etl_v2;

select * from imp_other_etl_v3 where id in (1578429,1578430) #执行员

select * from imp_other_etl_v2 where 
party_info = "" and 
trial_process = "" and 
trial_request = "" and 
court_find = "" and 
-- court_idea = "" and 
judge_result = "" and 
doc_footer = "" ;


select count(*) from imp_other_etl_v2 where court_idea = ""


create table aa like laws_doc_implement.implement_other_fields_v2

SELECT SUBSTRING(uuid,1,2) u,count(uuid) from imp_other_uuid_law_id_v2 group by u order by u



update imp_other_etl_v2 a ,imp_other_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update imp_other_etl_v2 a ,imp_other_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;


