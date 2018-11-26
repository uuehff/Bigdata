SELECT * from reason_bashou where n = '网络侵权责任纠纷' or p = '002009'
SELECT * from reason where new_name = '破坏社会主义市场经济秩序罪'
SELECT * from reason where new_name = '侵犯公民人身权利、民主权利罪'
SELECT * from reason where new_name like '%非法生产、销售专用间谍器材、窃听、窃照专用器材罪%'
SELECT * from reason where new_name =  '非法获取公民个人信息罪'

SELECT * from reason where new_name in ('非法获取公民个人信息罪','出售、非法提供公民个人信息罪','侵犯公民个人信息罪')
二审：
------以下是多了（已删除罪名），且新名称在reason中也有的。

伪造、变造居民身份证罪（已删除罪名）  伪造、变造、买卖身份证件罪
走私制毒物品罪（已删除罪名）    非法生产、买卖、运输制毒物品、走私制毒物品罪
非法买卖制毒物品罪（已删除罪名）   非法生产、买卖、运输制毒物品、走私制毒物品罪
非法生产、销售间谍专用器材罪（已删除罪名）  非法生产、销售专用间谍器材、窃听、窃照专用器材罪
盗窃、侮辱尸体罪（已删除罪名）     盗窃、侮辱、故意毁坏尸体、尸骨、骨灰罪
强制猥亵、侮辱妇女罪(已删除罪名)    强制猥亵、侮辱罪
出售、非法提供公民个人信息罪（已删除罪名） 侵犯公民个人信息罪
非法获取公民个人信息罪（已删除罪名）  侵犯公民个人信息罪
-----------
以下是名字错的：

破坏市场经济秩序罪	5105	破坏社会主义市场经济秩序罪
侵犯人身权利、民主权利罪	8138	侵犯公民人身权利、民主权利罪
制造、贩卖、传播淫秽物品罪	6	制作、贩卖、传播淫秽物品罪

SELECT uuid,new_reason from reason_add where new_reason like '%破坏市场经济秩序罪%'

update reason_add set 
new_reason = REPLACE(new_reason,'制造、贩卖、传播淫秽物品罪','制作、贩卖、传播淫秽物品罪') 
where new_reason like '%制造、贩卖、传播淫秽物品罪%'

SELECT uuid,new_reason from reason_add where uuid = '569884c9-6118-46d0-b0ef-073bb83e3c8f'


update reason_add a,judgment2_etl b set b.new_reason = a.new_reason where a.uuid = b.uuid

update reason_add a,judgment2 b set b.doc_reason = a.new_reason where a.uuid = b.uuid


create table judgment2_etl_uuid_new_reason as 
select uuid,new_reason from judgment2_etl
 
update judgment2_etl_uuid_new_reason_result a ,judgment2_etl b set b.reason_uid = a.reason_uids where a.uuid = b.uuid

