SELECT count(*) from tmp_wxy 


SELECT count(*) from tmp_wxy where history_new != ''


history_new 字段补全处理流程：

按顺序处理如下：

1、筛选数据，过滤掉只包含一个uuid，且为36或24的：
create table uuid_history as 
SELECT uuid,history_new from tmp_wxy where history_new != '' and CHAR_LENGTH(history_new) != 36 and CHAR_LENGTH(history_new) != 24

2、程序处理：过滤掉包含多个uuid，且每个uuid都正确的。

3、剩下的程序需要处理的数据为：
	1.包含一个uuid，但uuid是错误的。
	2.包含多个uuid，至少有一个uuid是错误的。

4、执行uuid_history_is_format_8.py，更新uuid_history_result中，history_new2||分割后，长度与history_new||分割后不相等的数据，设置is_format_history_uuid为'8'，说明有没补全的uuid。

5、更新补全的数据：
UPDATE uuid_history_result a ,tmp_wxy b set b.history_new2 = a.uuid_history,b.is_format_history_uuid=a.is_format where a.uuid = b.uuid

6、自我更新包含一个uuid，且正确的history_new：
UPDATE tmp_wxy set history_new2 = history_new where history_new != '' and (CHAR_LENGTH(history_new) = 36 or CHAR_LENGTH(history_new) = 24)

7、更新包含多个uuid，且每个uuid都正确的，因为uuid_history_result结果里没有，需要自更新。
UPDATE tmp_wxy set history_new2 = history_new where history_new != '' and CHAR_LENGTH(history_new) > 36 and history_new2 is null

8、更新history_new中，进行uuid的join时一个也没有匹配补全，这样的在结果uuid_history_result中没有，需要手动更新。
UPDATE tmp_wxy set is_format_history_uuid = '8' where history_new != '' and history_new2 is null 


SELECT uuid,history_new,history_new2,is_format_history_uuid from tmp_wxy where history_new2 is null and history_new != ''
SELECT uuid,history_new,history_new2,is_format_history_uuid from tmp_wxy where history_new != '' and history_new2 is null and is_format_history_uuid = '8'


SELECT uuid,history_new from tmp_wxy where (history_new != '' and CHAR_LENGTH(history_new) = 36) or (history_new != '' and CHAR_LENGTH(history_new) = 24)
SELECT uuid,history_new from tmp_wxy where history_new != '' and (CHAR_LENGTH(history_new) = 36 or CHAR_LENGTH(history_new) = 24)


update uuid_history a ,judgment2 b set a.is_format = b.is_format where a.uuid = b.uuid


select concat(uuid,judge_chief_new,judge_member_new,foot) from test


select a.uuid,a.history_new,b.uuid_history from uuid_history a ,uuid_history_result b 
where a.uuid=b.uuid and split

SELECT * from uuid_history where uuid = '582b113354d07a0634c06232'
SELECT * from tmp_wxy where is_format_history_uuid = '8'



select id,uuid,title,is_format from judgment2 where title like '%一审%'

select uuid from judgment2 where title like '%一审%'

SELECT * from laws_doc.judgment_etl where uuid in (select uuid from judgment2 where title like '%一审%'
)

DELETE from judgment2 where title like '%一审%'


update judgment2 a,judgment2_etl b set b.new_reason = a.doc_reason where a.uuid = b.uuid
