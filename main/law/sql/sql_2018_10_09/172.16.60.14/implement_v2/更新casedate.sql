update imp_other_etl_v2 a ,casedate_error_uuid_old b set a.casedate = b.casedate where a.uuid = b.uuid;

select * from judgment_zhangye_zhixing_v2_v3_result_lawyer_id where uuid = "09c4140c39163b90bb02f8a36fd46bb2";
select * from judgment_zhangye_zhixing_v2_v3_result_lawyer_id where law_office like "%内蒙古庆胜律师事务所%";

create table uuids as select uuid from casedate_error_uuid_old
insert into uuids select uuid from casedate_error_uuid_2018_imp_other

select * from imp_other_etl_v2 where uuid_old = "" or uuid is null limit 100;
select * from implement_civil_etl_v2 where uuid_old = "" or uuid is null limit 100;