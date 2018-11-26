create table sub_uuids_b647 as SELECT uuid from judgment where substring_index(uuid, '-', -4) = 'b647-11e3-84e9-5cf3fc0c2c18'

SELECT substring_index(uuid, '-', -4) uu from judgment where substring(uuid,9,1) = '-' group by uu HAVING(count(uu)>1)		时间: 227.761s

efea1d6c-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efeaaeee-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efec0c87-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efeccf66-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efecd28c-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efecdc37-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efece93f-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
efed01a5-b647-11e3-84e9-5cf3fc0c2c18	b647-11e3-84e9-5cf3fc0c2c18
SELECT id,uuid,title from judgment where uuid = 'efece93f-b647-11e3-84e9-5cf3fc0c2c18'

CREATE table uuid_28 as 
SELECT uuid,substring_index(uuid, '-', -4) uu from judgment where substring_index(uuid, '-', -4) = 'b647-11e3-84e9-5cf3fc0c2c18'



select uuid from judgment_etl where CHAR_LENGTH(uuid) = CHAR_LENGTH('59645f5f54c1721ae8f8e99f') order by uuid

SELECT SUBSTRING(uuid,1,2) u,count(uuid) from tmp_wxy group by u order by u 

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


create table uuids as 
SELECT uuid from tmp_wxy	where CHAR_LENGTH(uuid) > 24 and substring(uuid,1,1) in ('a','c','d','e','f')

create table uuid_history as 
SELECT uuid,history_new from tmp_wxy where history_new != '' and CHAR_LENGTH(history_new) != 36 and CHAR_LENGTH(history_new) != 24

tmp_wxy 与 judgment表，id一致：
SELECT MAX(id) from judgment 11295127
SELECT MAX(id) from tmp_wxy 11295127



