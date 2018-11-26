insert into implement_civil_etl select * from implement_civil_etl2;

alter table implement_civil_etl 
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

update implement_civil_etl a ,implement_part b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;


update implement_civil_etl 
set reason = reason_type;

update implement_civil_etl 
set reason_type = "执行";

V2版本处理====================
create table implement_civil_etl_v2 like laws_doc_administration.administration_etl_v2;
create table implement_civil_etl_v3 like laws_doc_administration.administration_etl_v2;
create table implement_civil_etl_v4 like laws_doc_administration.administration_etl_v2;

select * from implement_civil_etl_v3 where 
party_info = "" and 
trial_process = "" and 
trial_request = "" and 
court_find = "" and 
-- court_idea = "" and 
judge_result = "" and 
doc_footer = "" ;

select * from implement_civil_etl_v3 where id in (376348,376399,376401,376486,376487,376489)
select * from implement_civil_etl_v4 where id in (376348,376399,376401,376486,376487,376489)

select * from implement_civil_etl_v2 where id in (364966,364967)  #执行员
select * from implement_civil_etl_v3 where id in (364966,364967)  #执行员

create table implement_other_fields_v2 like laws_doc_administration.administration_other_fields_v2;
alter table implement_civil_etl_v2 
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext;

update implement_civil_etl_v2 a ,implement_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update implement_civil_etl_v2 a ,implement_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;



