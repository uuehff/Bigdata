create table adjudication_civil_etl_v2_uuid as 
select uuid from adjudication_civil_etl_v2;

create table judgment_new_v2_uuid like 800w_01_uuid;

alter table judgment_new_v2_uuid 
add id int auto_increment primary key,
add field varchar(1) DEFAULT '',
add plaintiff_id varchar(1) DEFAULT '',
add defendant_id varchar(1) DEFAULT '',
add lawyer_id varchar(1) DEFAULT '',
add lawyer varchar(1) DEFAULT '',
add law_office varchar(1) DEFAULT '',
add plaintiff varchar(1) DEFAULT '',
add defendant varchar(1) DEFAULT '',
add org_plaintiff varchar(1) DEFAULT '',
add org_defendant varchar(1) DEFAULT '';
============
create table judgment_zhangye_civil_v2_result_uuid as 
select uuid from judgment_zhangye_civil_v2_result;


insert into judgment_new_v2_uuid(uuid) select uuid from judgment_new_v2;
insert into judgment_new_v2_uuid(uuid) select uuid from adjudication_civil_etl_v2;;
insert into judgment_new_v2_uuid(uuid) select uuid from judgment_zhangye_civil_v2_result;
insert into judgment_new_v2_uuid(uuid) select uuid from judgment_zhangye_civil_v3_result;
insert into judgment_new_v2_uuid(uuid) select uuid from judgment_zhangye_civil_v4_result;

行政：==================================
create table zz_xingzheng_online_uuid like civil_v2.800w_01_uuid;
insert into zz_xingzheng_online_uuid(uuid) select uuid from administration_v2.administration_etl_v2;
insert into zz_xingzheng_online_uuid(uuid) select uuid from administration_v2.judgment_zhangye_xingzheng_v2_result;
insert into zz_xingzheng_online_uuid(uuid) select uuid from administration_v2.judgment_zhangye_xingzheng_v3_result;
insert into zz_xingzheng_online_uuid(uuid) select uuid from administration_v2.judgment_zhangye_xingzheng_v4_result;
刑事：=============================
create table zz_xingshi_online_uuid like civil_v2.800w_01_uuid;
insert into zz_xingshi_online_uuid(uuid) select uuid from judgment_v2.adjudication_xingshi_etl_v2;
insert into zz_xingshi_online_uuid(uuid) select uuid from judgment_v2.judgment_etl_v2;
insert into zz_xingshi_online_uuid(uuid) select uuid from judgment_v2.judgment2_etl_v2;
insert into zz_xingshi_online_uuid(uuid) select uuid from judgment_v2.judgment_zhangye_xingshi_v2_result;
insert into zz_xingshi_online_uuid(uuid) select uuid from judgment_v2.judgment_zhangye_xingshi_v3_result;
insert into zz_xingshi_online_uuid(uuid) select uuid from judgment_v2.judgment_zhangye_xingshi_v4_result;

执行：=======================================
create table zz_zhixing_online_uuid like civil_v2.800w_01_uuid;
insert into zz_zhixing_online_uuid(uuid) select uuid from implement_v2.imp_other_etl_v2;
insert into zz_zhixing_online_uuid(uuid) select uuid from implement_v2.implement_civil_etl_v2;
insert into zz_zhixing_online_uuid(uuid) select uuid from implement_v2.judgment_zhangye_zhixing_v2_result;
insert into zz_zhixing_online_uuid(uuid) select uuid from implement_v2.judgment_zhangye_zhixing_v3_result;
insert into zz_zhixing_online_uuid(uuid) select uuid from implement_v2.judgment_zhangye_zhixing_v4_result;






