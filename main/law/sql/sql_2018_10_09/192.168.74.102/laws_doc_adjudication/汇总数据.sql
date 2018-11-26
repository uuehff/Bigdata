select min(id),max(id) from adjudication_xingshi_etl where id <= 1000000 and doc_from = "limai"

insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_02;
insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_03;
insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_04;
insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_wenshu;

insert into adjudication_civil_etl_01(id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer
) select * from adjudication_civil_etl_wenshu ;


alter table adjudication_civil_etl_01 
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

create table z2 select id from adjudication_civil_etl_wenshu

update adjudication_xingshi_etl a ,adjudication_xingshi_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

update adjudication_xingshi_etl_01 a ,adjudication_xingshi_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;


update adjudication_civil_etl a ,adjudication_civil_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

update adjudication_civil_etl_01 a ,adjudication_civil_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

select type,reason_type,judge_type,count(*) from adjudication_xingshi_etl group by type,reason_type,judge_type
	刑事	裁定	309492
	民事	裁定	309492


update judgment_new 
set type = 
case 
when type = "一审" then "1"
when type = "二审" then "2"
when type = "再审" then "3"
when type = "其他" then "4"
end

V2处理：===================

create table adjudication_civil_etl_v2 like laws_doc_administration.administration_etl_v2;

create table adjudication_civil_etl_v3 like laws_doc_administration.administration_etl_v2;
create table adjudication_xingshi_etl_v4 like laws_doc_administration.administration_etl_v2;


create table adjudication_civil_etl_wenshu_v2 like laws_doc_administration.administration_etl_v2;


 
create table adjudication_civil_other_fields_v2 like  laws_doc_imp_other.imp_other_other_fields_v2;
create table adjudication_xingshi_other_fields_v2 like  laws_doc_imp_other.imp_other_other_fields_v2;


create table adjudication_xingshi_uuid_law_id_v2 like  adjudication_civil_uuid_law_id_v2;




SELECT SUBSTRING(uuid,1,2) u,count(uuid) from adjudication_civil_uuid_law_id_v2 group by u order by u


alter table adjudication_civil_etl_v2 
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext;


update adjudication_civil_etl_v2 a ,adjudication_civil_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update adjudication_civil_etl_v2 a ,adjudication_civil_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;


================================================
alter table adjudication_xingshi_etl_v2 
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext;


update adjudication_xingshi_etl_v2 a ,adjudication_xingshi_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update adjudication_xingshi_etl_v2 a ,adjudication_xingshi_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;















