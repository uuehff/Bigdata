create table adju_uuid as select uuid,uuid_old from adjudication_civil_etl_v2; #加uuid索引
create table 800w_01_uuid as select uuid from civil_etl_v2_800w_01; 
create table 800w_02_uuid as select uuid from civil_etl_v2_800w_02;
create table judgment_new_uuid as select uuid,uuid_old from judgment_new_v2; #加uuid索引


create table judgment_zhangye_uuid as select uuid from judgment_zhangye_civil_v2_result;

select a.uuid,b.uuid from adju_uuid a,judgment_new_uuid b where a.uuid = b.uuid limit 100;
select a.uuid,b.uuid from adju_uuid a,judgment_new_uuid b where a.uuid = b.uuid limit 100;

select count(*) from adju_uuid a,judgment_new_uuid b where a.uuid = b.uuid;
select * from adjudication_civil_etl_v2 a,judgment_new_v2 b where a.uuid = b.uuid limit 100;
3571,经查看，需删除adjudication_civil_etl_v2表数据。
create table adju_uuid_del01 as select a.uuid,a.uuid_old from adju_uuid a,judgment_new_uuid b where a.uuid = b.uuid;


select count(*) from adju_uuid a,judgment_zhangye_uuid b where a.uuid = b.uuid;
0
select count(*) from judgment_new_uuid a,judgment_zhangye_uuid b where a.uuid = b.uuid;
0
select count(*) from adju_uuid a,800w_01_uuid b where a.uuid = b.uuid ;
select a.uuid,b.uuid from adju_uuid a,800w_01_uuid b where a.uuid = b.uuid limit 100;
select * from adjudication_civil_etl_v2 a,civil_etl_v2_800w_01 b where a.uuid = b.uuid limit 10;
83325,经查看，需删除adjudication_civil_etl_v2表重复数据。
create table adju_uuid_del02 as select a.uuid,a.uuid_old from adju_uuid a,800w_01_uuid b where a.uuid = b.uuid;

select count(*) from adju_uuid a,800w_02_uuid b where a.uuid = b.uuid ;
select a.uuid,b.uuid from adju_uuid a,800w_02_uuid b where a.uuid = b.uuid limit 100;
select * from adjudication_civil_etl_v2 a,civil_etl_v2_800w_02 b where a.uuid = b.uuid limit 10;
114266,经查看，需删除adjudication_civil_etl_v2表重复数据。
create table adju_uuid_del03 as select a.uuid,a.uuid_old from adju_uuid a,800w_02_uuid b where a.uuid = b.uuid;

合并要删除的数据：
INSERT into adju_uuid_del03(uuid,uuid_old) select uuid,uuid_old from adju_uuid_del02;
INSERT into adju_uuid_del03(uuid,uuid_old) select uuid,uuid_old from adju_uuid_del01;
select count(*) from adju_uuid_del03;201162
select uuid,uuid_old,count(*) from adju_uuid_del03 group by uuid,uuid_old;#200934
create table adju_uuid_del03_distinct as  select uuid,uuid_old from adju_uuid_del03 group by uuid,uuid_old;

删除adjudication_civil_etl_v2表重复数据：

DELETE a from adjudication_civil_etl_v2 a,adju_uuid_del03_distinct b where a.uuid = b.uuid;
DELETE a from adjudication_civil_uuid_law_id_v2 a,adju_uuid_del03_distinct b where a.uuid = b.uuid;



select count(*) from judgment_new_uuid a,800w_01_uuid b where a.uuid = b.uuid ;
select a.uuid,b.uuid from judgment_new_uuid a,800w_01_uuid b where a.uuid = b.uuid limit 100;
select * from judgment_new_v2 a,civil_etl_v2_800w_01 b where a.uuid = b.uuid limit 10;
145217,经查看，需删除judgment_new_v2表重复数据。
create table judgment_new_uuid_del_01 as select a.uuid,a.uuid_old from judgment_new_uuid a,800w_01_uuid b where a.uuid = b.uuid;



select count(*) from judgment_new_uuid a,800w_02_uuid b where a.uuid = b.uuid ;
select a.uuid,b.uuid from judgment_new_uuid a,800w_02_uuid b where a.uuid = b.uuid limit 100;
select * from judgment_new_v2 a,civil_etl_v2_800w_02 b where a.uuid = b.uuid limit 10;
select * from judgment_new_v2 a,civil_etl_v2_800w_02 b where a.uuid = b.uuid limit 10;
324381,经查看，需删除judgment_new_v2表重复数据。
create table judgment_new_uuid_del_02 as select a.uuid,a.uuid_old from judgment_new_uuid a,800w_02_uuid b where a.uuid = b.uuid;

INSERT into judgment_new_uuid_del_02(uuid,uuid_old) select uuid,uuid_old from judgment_new_uuid_del_01;

删除judgment_new_v2表重复数据：

DELETE a from judgment_new_v2 a,judgment_new_uuid_del_02 b where a.uuid = b.uuid;
DELETE a from judgment_new_uuid_law_id_v2 a,judgment_new_uuid_del_02 b where a.uuid = b.uuid;
受影响的行: 404210


==========================================================================


==========================================
select * from adjudication_civil_etl_v2 where uuid = "0017a508a7fa355ba3d5983ea90dd541"
uuid_old = dfb93648-73b4-4e14-b39d-a7a20111f939

select * from judgment_new_v2 where uuid = "00004bfedd183170aa28b13cf9f0dd91"
uuid_old = 08e5ed58-7b80-4db5-889b-8aa9e3ba11e9
select * from civil_etl_v2_800w_02 where uuid = "00004bfedd183170aa28b13cf9f0dd91"


select * from judgment_new_v2 a,adjudication_civil_etl_v2 b where a.uuid = "0017a508a7fa355ba3d5983ea90dd541" limit 1
