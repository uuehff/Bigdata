CREATE table judgment_etl_reason_is_null as SELECT uuid,new_reason from judgment_etl 
where new_reason is not null and reason_uid is null

SELECT * from reason where new_name is null or new_name = ''

SELECT uuid,new_reason  from judgment_etl where uuid = '3fd4d775-bd03-4954-b229-d0d47a7a468b'
盗窃罪||开设赌场罪||故意伤害罪

非法持有、私藏枪支、弹药罪||非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪
1002036||1002031

1004003||1005002||1006001049
select * from reason where uid = '1004003' or uid = '1005002' or uid = '1006001049'

UPDATE judgment_etl a,reason_uid_null b set a.reason_uid = b.reason_uids where a.uuid = b.uuid

select uuid from judgment_etl where CHAR_LENGTH(uuid) = CHAR_LENGTH('59645f5f54c1721ae8f8e99f') order by uuid

UPDATE judgment_etl set type = '0' where type != '0'


SELECT uuid, substring_index(uuid, '-', -4) uu from judgment_etl where substring_index(uuid, '-', -4) = 'c46c-41fe-a8c8-3c96e2fe19d2'

6c9ee6a6-fc96-40fa-a243-035f7731d6d5	2ebda3d-8d3b-42c3-a0cf-3655edd97462		
d365d37a-d52b-4828-9d26-63d8376064f2	14400a3-ac3f-45d3-b46c-c070b1b389e3		
2de151d4-5873-43fa-b5a2-b1916936a5ed	fd898e1-c46c-41fe-a8c8-3c96e2fe19d2		
e57217f2-454f-4227-a72b-610759585e1f	2dcf232-8e1c-4007-91c5-dd6006c8e5af		
79dce4fb-3a14-4239-9336-9fe34e3da8c6	062eb49-5453-47dd-8f1a-32fd6bff2dc5		
fb22900f-93de-4ed5-aa3f-fa194e1f51cb	7bf378-7a20-4627-96f2-1a04c4e04d29		
a86ef5bb-07c8-4001-83ee-a80700a31a93	8cd4af3-fe15-444b-b83c-a7e400a34d00		




