create table tmp_weiwc_court_new as SELECT court_new from judgment_etl GROUP BY court_new

SELECT * FROM judgment_etl WHERE uuid = '00003fb2-1b77-4537-888b-b42b3daaa627'

create table uuids as 
SELECT uuid from judgment_etl	where CHAR_LENGTH(uuid) > 24 and substring(uuid,1,1) in ('a','c','d','e','f')

6308266-31ce-45bf-bbae-9c1d284be218

SELECT uuid, substring_index(uuid, '-', -4) uu from judgment_etl where substring_index(uuid, '-', -4) = '91bb1-0f7e-4eba-a675-a7f20121c533'

SELECT COUNT(*) from uuids GROUP BY subs
SELECT uuid,substring_index(uuid, '-', 1),substring_index(uuid, '-', -4) from uuids limit 10
SELECT CHAR_LENGTH(uuid) from uuids where substring(uuid,9,1) != '-' limit 10
SELECT CHAR_LENGTH(uuid) from uuids where substring(uuid,9,1) = '-' limit 10

判断能否使用第一个-后面的字符进行补全uuid:
统计第一个-后面的字符串是否唯一：
SELECT uu from (
SELECT substring_index(uuid, '-', -4) uu from uuids
union all 
SELECT substring_index(uuid, '-', -4) from laws_doc2.uuid_history where substring(uuid,9,1) = '-'
) a group by uu HAVING(count(uu)>1)

SELECT uu from (
SELECT SUBSTRING(uuid,1) uu from uuids
union all 
SELECT SUBSTRING(uuid,1) from laws_doc2.uuid_history where substring(uuid,9,1) = '-'
) a group by uu HAVING(count(uu)>1)


SELECT id,uuid,title from judgment where uuid in (
SELECT uu from (
SELECT uuid uu from uuids
union all 
SELECT uuid from laws_doc2.uuid_history where substring(uuid,9,1) = '-'
) a group by uu HAVING(count(uu)>1)
)


create table uuid_1_2 as SELECT * from (
SELECT uu from (
SELECT uuid uu from uuids
union all 
SELECT uuid from laws_doc2.uuid_history where substring(uuid,9,1) = '-'
) a group by uu HAVING(count(uu)>1)
) b

create table z_uuid as ( 
SELECT b.uuid ,b.title, b.court from uuid_1_2 a ,laws_doc2.judgment2 b where a.uu = b.uuid and b.title not LIKE '%二审%' 
and b.court not like '%中级%' and b.court not like '%高级%' )


create table z_uuid_ as SELECT uu uuid from uuid_1_2 where uu not in (SELECT uuid from z_uuid)
DELETE from laws_doc2.judgment2 where uuid not in (SELECT uuid from z_uuid)

DELETE from laws_doc2.tmp_wxy where uuid not in (SELECT uuid from z_uuid)

DELETE from judgment_etl where uuid in (SELECT uuid from z_uuid_)

DELETE from judgment where uuid in (SELECT uuid from z_uuid_)



SELECT b.uuid ,b.title, b.court from uuid_1_2 a ,laws_doc2.judgment2 b where a.uu = b.uuid and b.title LIKE '%二审%' 
and (  b.court like '%中级%' or b.court like '%高级%' )

SELECT b.uuid ,b.title, b.court from uuid_1_2 a ,laws_doc2.judgment2 b where a.uu = b.uuid and (b.title LIKE '%一审%' or b.court not like '%中级%' or b.court not like '%高级%')

CREATE table uuids as SELECT uuid from  judgment_etl

SELECT * from laws_doc2.judgment2 where uuid ='00ea6063-ae91-4d6f-b908-a74800946037'
SELECT * from judgment where uuid ='006b2281-d3bf-48b2-9f82-a77401291025'

0056eb25-7484-49c1-89c0-a7440112006b	黄海峰犯诈骗罪二审刑事判决书
006b2281-d3bf-48b2-9f82-a77401291025	张某某故意伤害一审刑事判决书
006c35a5-6fca-4dc5-bebf-a72801212da8	索某某故意伤害案二审刑事附带民事判决书
00d38376-eaa2-4a3c-8f4b-a73e0170fc85	邱芳林诈骗二审刑事判决书
00de27f7-d020-435e-8fc3-b0695d5b9c54	蒲某与唐某甲寻衅滋事一审刑事附带民事判决书
00def13b-838c-41cb-8f48-a747017ad868	周宇杰受贿二审刑事判决书
00ea6063-ae91-4d6f-b908-a74800946037	唐云强、缪锦林职务侵占罪二审刑事判决书
00ece8c3-8e2f-4bf8-bfa3-5c5bb5a415c0	王某甲、田某某招摇撞骗罪一审刑事判决书
0116cc6e-3ce5-4558-b5f7-411d2e0425b3	韦汝成挪用资金、诈骗一审刑事判决书
02085f73-e8a3-4fcf-a5af-53f148110880	马某某玩忽职守一审刑事判决书
0220e558-2687-4932-99ba-bd364a8b1b74	贡曲土多盗窃罪二审刑事判决书
022de56c-ea6b-4f60-bac4-78adb917dd47	余某甲挪用公款罪一审刑事判决书
027dce16-86e4-4a76-93be-0c27322ef36f	徐涛故意伤害一审刑事判决书


SELECT uuid ,title from (
SELECT uuid ,title from judgment e where substring(uuid,9,1) = '-'
union all 
SELECT uuid ,title from laws_doc2.judgment2 f where substring(uuid,9,1) = '-'
) a group by uuid HAVING(count(uuid)>1)


SELECT SUBSTRING(uuid,5) from uuids limit 10

SELECT * from judgment where uuid = '006c35a5-6fca-4dc5-bebf-a72801212da8'

SELECT * from laws_doc2.judgment2 where uuid = '0471bb58-a26f-44e5-a77a-78a292fb186b'

update uuid_history a ,judgment2 b set a.is_format = b.is_format where a.uuid = b.uuid

select uuid,title from judgment where title like '%二审%'



