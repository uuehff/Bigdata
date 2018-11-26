update administration_etl_v2 a ,casedate_error_uuid_old b set a.casedate = b.casedate where a.uuid = b.uuid;

create table uuids as select uuid from casedate_error_uuid_old
insert into  uuids select uuid from casedate_error_uuid_2018_administration
