update adjudication_civil_etl_v2 a ,casedate_error_uuid_old_civil b set a.casedate = b.casedate where a.uuid = b.uuid;

update judgment_new_v2 a ,casedate_error_uuid_old b set a.casedate = b.casedate where a.uuid = b.uuid;


update civil_etl_v2_800w_01 a ,casedate_error_uuid_old_01 b set a.casedate = b.casedate where a.uuid = b.uuid;
update civil_etl_v2_800w_02 a ,casedate_error_uuid_old_02 b set a.casedate = b.casedate where a.uuid = b.uuid;


create table casedate_error_uuid_old_union_4_tables like casedate_error_uuid_old_02

insert into casedate_error_uuid_old_union_4_tables select * from casedate_error_uuid_old_civil;
insert into casedate_error_uuid_old_union_4_tables select * from casedate_error_uuid_old;
insert into casedate_error_uuid_old_union_4_tables select * from casedate_error_uuid_old_01;
insert into casedate_error_uuid_old_union_4_tables select * from casedate_error_uuid_old_02;



select * from civil_other_fields_v2_800w_01 where uuid =  "6c1d8148e4293257b578681856e61ec1"


create table casedate_null_null as select id,uuid,casedate from casedate_error_uuid_old_union_4_tables where casedate = "";

create table casedate_error_uuid_2018_3_tables as select * from casedate_error_uuid_2018;
insert into  casedate_error_uuid_2018_3_tables select * from casedate_error_uuid_2018_new;
insert into  casedate_error_uuid_2018_3_tables select * from casedate_error_uuid_civil_2018;

create table uuids as select uuid from casedate_error_uuid_2018_3_tables;
insert into  uuids select uuid from casedate_error_uuid_old_union_4_tables;
create table uuids2 as select uuid from uuids group by uuid 

