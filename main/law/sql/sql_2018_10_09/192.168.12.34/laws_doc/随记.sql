select * from court where name like '%高级%' and court_cate != '高级' 

select * from court where  province = '湖北省'  order by uid

select * from court where name not like '%高级%' and court_cate = '高级'
update judgment_etl set court_uid = '21000' where court_uid = '21008019'

select court from laws_doc2.judgment2_etl where court_uid = '21000'

create table court_orderBy_uid as select id,name,province,city,pid,uid from court order by uid

update court_orderBy_uid set name = city where name is null and city is not null

create table reason_orderBy_uid as select id,name,full_name,pid,uid from reason order by uid


select pid,uid,CONCAT(pid,"||",uid) from court where name is not null and CHAR_LENGTH(uid) = 5

update court a, laws_doc2.judgment2_etl b set b.court_uid = a.full_uid where a.name is not null and a.uid = b.court_uid 
update court a, judgment_etl b set b.court_uid = a.full_uid where a.name is not null and a.uid = b.court_uid 

select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'judgment_etl' and table_schema='laws_doc' order by COLUMN_NAME

SELECT * from laws_doc2.judgment2_etl where history is not null and CHAR_LENGTH(history) > 36

SELECT *  from laws_doc2.judgment2 where uuid = '58680e08-f05d-418f-90ad-8ea9e26bc88e'

SELECT id,uuid,province,age_year,if_surrender,if_nosuccess,if_accumulate  from judgment_etl where uuid in ('0b193b86-2d83-40e9-b523-3bf7b705aa95','6f1a8700-923d-4959-9226-e608e21a7645')
SELECT *  from judgment where uuid in ('989fb5bb-f533-42b0-b485-86ebe98ed5b5','6f1a8700-923d-4959-9226-e608e21a7645')

SELECT uuid, province,age_year,if_surrender,if_nosuccess,if_accumulate  from laws_doc2.judgment2_etl where uuid = 'ed96cf8d-03e3-424f-bfdc-b6f86f087818'

d707c177-1921-4e79-aaf6-4479cfaf1493

update laws_doc2.judgment2_etl set history_2_fill = '37' where CHAR_LENGTH(history) > 36

SELECT history from laws_doc2.judgment2_etl where history = ''

update laws_doc2.judgment2_etl a, laws_doc2.eye_scan_uuid_history b 
set a.history = b.history where CHAR_LENGTH(a.history) > 36 and a.uuid = b.uuid 

select count(*) from judgment where is_format = 1
select uuid from judgment_main_etl where CHAR_LENGTH(uuid) <36 and uuid not in (SELECT uuid from judgment_etl where CHAR_LENGTH(uuid) < 36)

select * from judgment_main_etl where uuid = '581e8e1454d07a046868bfe6'

CREATE table hbase_authorized_keys as select uuid from judgment_etl where id < 50



