select id,uuid_,uuid,lawlist,law_id from administration_etl_v2 where uuid_ = "d46ab396140e3e30a896b8b1e6dfb37a"
182193	d46ab396140e3e30a896b8b1e6dfb37a	55a807ab-d699-48cb-910a-a8480173a4bf	["《中华人民共和国行政诉讼法》第六十二条"]	

线下v2: d46ab396140e3e30a896b8b1e6dfb37a  4775850062



select id,caseid,party_info from administration_etl where CHAR_LENGTH(caseid) > 225; #caseid包含当事人信息
DELETE from administration_etl where CHAR_LENGTH(caseid) > 225;

alter table administration_etl
add title varchar(220),
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

update administration_etl a ,administration_part b set 
 a.title = b.title,
 a.lawlist = b.lawlist,
 a.type = b.type,
 a.judge_type = b.judge_type,
 a.reason_type = b.reason_type 
 where a.id = b.id;

V2处理：==================================================================
create table administration_etl_v4 like administration_etl_v2;
create table administration_etl_v3 like administration_etl_v2;


GRANT ALL PRIVILEGES ON *.* TO 'weiwc'@'%' IDENTIFIED BY 'HHly2017.' WITH GRANT OPTION;
-- REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'liuf';
FLUSH PRIVILEGES;


-- create table administration_pri_reason_id as 
select * from administration_etl_v2 where 
party_info = "" and 
trial_process = "" and 
trial_request = "" and 
court_find = "" and 
-- court_idea = "" and 
judge_result = "" and 
doc_footer = "" ;

select * from administration_etl_v2 where id = 284752 or id = 429564
select * from administration_etl_v4 where id = 284752 or id = 429564
select * from administration_etl_v3 where id = 284752 or id = 429564



update administration_etl_v2 a ,administration_other_fields_v2_old b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update administration_etl_v2 a ,administration_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;


alter table administration_etl_v2 
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext;

alter table administration_etl_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);

======================================
alter table imp_other_etl_v2  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update imp_other_etl_v2 a ,imp_other_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update imp_other_etl_v2 a ,imp_other_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table imp_other_etl_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);
========================================================
implement_civil_etl_v2    |
| implement_other_fields_v2 |
| implement_uuid_law_id_v2

alter table implement_civil_etl_v2  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update implement_civil_etl_v2 a ,implement_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update implement_civil_etl_v2 a ,implement_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table implement_civil_etl_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);

==============================================

========================================================
| adjudication_xingshi_etl_v2          |
| adjudication_xingshi_other_fields_v2 |
| adjudication_xingshi_uuid_law_id_v2  |
| judgment_etl_v2                      |
| judgment_other_fields_v2             |
| judgment_uuid_law_id_v2


alter table adjudication_xingshi_etl_v2  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update adjudication_xingshi_etl_v2 a ,adjudication_xingshi_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update adjudication_xingshi_etl_v2 a ,adjudication_xingshi_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table adjudication_xingshi_etl_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);
================================

| judgment_etl_v2                      |
| judgment_other_fields_v2             |
| judgment_uuid_law_id_v2


alter table judgment_etl_v2  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update judgment_etl_v2 a ,judgment_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update judgment_etl_v2 a ,judgment_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table judgment_etl_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);
===============================================
adjudication_civil_etl_v2          |
| adjudication_civil_other_fields_v2 |
| adjudication_civil_uuid_law_id_v2  |

==============================================================
==============================================================
==============================================================
alter table adjudication_civil_etl_v2  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update adjudication_civil_etl_v2 a ,adjudication_civil_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update adjudication_civil_etl_v2 a ,adjudication_civil_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table adjudication_civil_etl_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);

alter table civil_etl_v2_800w_01  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update civil_etl_v2_800w_01 a ,civil_other_fields_v2_800w_01 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update civil_etl_v2_800w_01 a ,uuid_law_id_civil_etl_v2_800w_01 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table civil_etl_v2_800w_01 
change column uuid uuid_old varchar(40),
change column uuid_ uuid varchar(255);

alter table civil_etl_v2_800w_02  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update civil_etl_v2_800w_02 a ,civil_other_fields_v2_800w_02 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update civil_etl_v2_800w_02 a ,uuid_law_id_civil_etl_v2_800w_02 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table civil_etl_v2_800w_02 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);

alter table judgment_new_v2  
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext,
modify court longtext;

update judgment_new_v2 a ,judgment_new_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid = b.uuid;

update judgment_new_v2 a ,judgment_new_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;

alter table judgment_new_v2 
change column uuid uuid_old varchar(36),
change column uuid_ uuid varchar(32);


SELECT SUBSTRING(uuid,1,2) u,count(uuid) from administration_etl_v2 group by u order by u
SELECT uuid,SUBSTRING(uuid,1,2) u from administration_etl_v2 limit 3;
