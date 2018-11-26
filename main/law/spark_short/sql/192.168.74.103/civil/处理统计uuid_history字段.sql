SELECT count(*) from tmp_wxy 


SELECT count(*) from tmp_wxy where history_new != ''

create table uuid_history as 
SELECT uuid,history_new from tmp_wxy where history_new != '' and CHAR_LENGTH(history_new) != 36 and CHAR_LENGTH(history_new) != 24


SELECT uuid,history_new from tmp_wxy where history_new != '' and (CHAR_LENGTH(history_new) = 36 or CHAR_LENGTH(history_new) = 24)

UPDATE tmp_wxy set history_new2 = history_new where history_new != '' and (CHAR_LENGTH(history_new) = 36 or CHAR_LENGTH(history_new) = 24)

UPDATE tmp_wxy set history_new2 = history_new where history_new != '' and CHAR_LENGTH(history_new) > 36 and history_new2 is null

UPDATE tmp_wxy set is_format_history_uuid = '8' where history_new != '' and history_new2 is null

SELECT uuid,history_new,history_new2,is_format_history_uuid from tmp_wxy where history_new != '' and history_new2 is null


SELECT uuid,history_new from tmp_wxy where (history_new != '' and CHAR_LENGTH(history_new) = 36) or (history_new != '' and CHAR_LENGTH(history_new) = 24)


update uuid_history a ,judgment2 b set a.is_format = b.is_format where a.uuid = b.uuid


select concat(uuid,judge_chief_new,judge_member_new,foot) from test

5854309554d07a13c01753f5

select a.uuid,a.history_new,b.uuid_history from uuid_history a ,uuid_history_result b 
where a.uuid=b.uuid and split

SELECT * from uuid_history where uuid = '582b113354d07a0634c06232'
SELECT * from tmp_wxy where is_format_history_uuid = '8'

UPDATE uuid_history_result a ,tmp_wxy b set b.history_new2 = a.uuid_history,b.is_format_history_uuid=a.is_format where a.uuid = b.uuid

select uuid from judgment where CHAR_LENGTH(uuid) = CHAR_LENGTH('59645f5f54c1721ae8f8e99f') order by uuid

SELECT SUBSTRING(uuid,1,2) u,count(uuid) from judgment_etl group by u order by u 
SELECT SUBSTRING(uuid,1,1) u,count(uuid) from judgment_etl group by u order by u 
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


SELECT * from judgment where uuid = 'c924e79d-786a-4b84-b376-fc1c88e3200a'

create table uuids as 
SELECT uuid from judgment_etl	where CHAR_LENGTH(uuid) > 24 and substring(uuid,1,1) in ('a','c','d','e','f')


