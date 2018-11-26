alter table judgment_etl_v2 
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext;

update judgment_etl_v2 a ,judgment_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update judgment_etl_v2 a ,judgment_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;
================================================
alter table judgment2_etl_v2 
modify reason_type longtext,
modify type longtext,
modify judge_type longtext,
modify law_id longtext,
modify reason longtext,
modify reason_uid longtext,
modify casedate longtext,
modify province longtext,
modify court_uid longtext;


update judgment2_etl_v2 a ,judgment2_other_fields_v2 b set 
 a.reason = b.reason,
 a.reason_uid = b.reason_uid,
 a.casedate = b.casedate,
 a.province = b.province,
 a.court_uid = b.court_uid 
 where a.uuid_old = b.uuid;

update judgment2_etl_v2 a ,judgment2_uuid_law_id_v2 b set 
 a.law_id = b.law_id 
 where a.uuid = b.uuid;
===================================================

