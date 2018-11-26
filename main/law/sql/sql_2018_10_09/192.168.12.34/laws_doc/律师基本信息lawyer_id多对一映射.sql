create table lawyers_uuid_plain_defen_law_id as select uuid,plaintiff_id,defendant_id,lawyer_id from judgment_main_etl 

select * from lawyers_new where id = 392364
395167||85509
84724||392364


一审更新原告、被告id.
1、spark代码lawyers_plaintiff_defendant_id_update_judgment.py处理输出plain_defen_id2表。
update judgment_main_etl a set a.plaintiff_id = NULL,
a.defendant_id = NULL,
a.lawyer_id = NULL

2、
update judgment_main_etl as a, plain_defen_id2 as b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.denfendant_id,
a.lawyer_id = CONCAT_WS("||",b.plaintiff_id,b.denfendant_id) where a.id = b.id   #CONCAT_WS忽略连接中的NULL值。 where a.id = b.id

update judgment_main_etl set lawyer_id = CONCAT_WS("||",plaintiff_id,defendant_id)

3、删除judgment_visualization_v2中的原告、被告id。


二审更新原告、被告id.
1、spark代码lawyers_plaintiff_defendant_id_update_judgment2.py处理输出plain_defen_id2表。

2、update laws_doc2.judgment2_main_etl as a, laws_doc2.plain_defen_id2 as b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.denfendant_id,
a.lawyer_id = CONCAT_WS("||",b.plaintiff_id,b.denfendant_id)  where a.id = b.id 

3、删除judgment2_visualization_v2中的原告、被告id。

ALTER TABLE plain_defen_id_judgment2 add unique index id(id);
ALTER TABLE judgment2_main_etl add unique index id(id);

线上：
update judgment_main_etl as a, plain_defen_id_judgment as b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.denfendant_id,
a.lawyer_id = CONCAT_WS("||",b.plaintiff_id,b.denfendant_id) where a.id = b.id;

update judgment2_main_etl as a, plain_defen_id_judgment2 as b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.denfendant_id,
a.lawyer_id = CONCAT_WS("||",b.plaintiff_id,b.denfendant_id) where a.id = b.id;



律师职业编号解释：
第一位为执业证书文本种类代码。代表执业律师执业证文本，全国统一为1；
第二、三位为持证人执业机构所在省、直辖市、自治区代码。
第四、五位为执业机构所在地市区（县）代码。
第六至九位为首次批准律师执业的年度代码。由此可以判断律师执业起始年限。
第十位为执业证类别代码。专职律师为1，兼职律师为2，香港居民律师为3，澳门居民律师为4，台湾居民律师为5，公职律师为6，
公司律师为7，法律援助律师为8，军队律师为9。

第十一位为性别代码，男为0，女为1。本人男性为0。
第十二位至十七位为执业证序列号代码。


select id,char_no,gender,pra_type,first_pra_time from lawyers_new where char_no is not null and char_no != "" and CHAR_LENGTH(char_no) = 17  #332224

update lawyers_new set char_no = null where CHAR_LENGTH(char_no) !=17

select CHAR_LENGTH(char_no),count(*) from lawyers_new where char_no is not null and char_no != "" group by CHAR_LENGTH(char_no)

select id,char_no,gender,pra_type,first_pra_time from lawyers_new where char_no is not null and char_no != ""

select pra_type,count(*) from lawyers_new where char_no is not null and char_no != "" group by pra_type

select char_no,pra_type from lawyers_new where char_no is not null and char_no != "" and pra_type = "社会律师"


线上删除judgment_visualization_v2、judgment2_visualization_v2中的plaintiff_id,denfendant_id字段。

alter table judgment_visualization_v2
drop plaintiff_id,
drop defendant_id;

alter table judgment2_visualization_v2
drop plaintiff_id,
drop defendant_id;

alter table lawyers
drop lawyer_key,
drop old_id;






