select * from judgment where uuid = "bf3262c4-cb39-4282-8455-a835012d9432"   句号以后被截断，及000切割问题
select * from judgment where uuid = "18983fe0-f5dd-4990-9aa9-a8b300d00360"   满月酒后面内容被截断！
select * from judgment where uuid = "af859d1c-42ad-4ff6-9bab-a81200a1724e"
select * from judgment where uuid = "4611bcbb-f5c2-4970-9ceb-a8a1009cda29"
party_info,trial_process,trial_request,trial_reply,court_find,court_idea,judge_result,doc_footer


select * from judgment_doc where doc_id = "4611bcbb-f5c2-4970-9ceb-a8a1009cda29"


GRANT ALL PRIVILEGES ON *.* TO 'wxy'@'%' IDENTIFIED BY '!@#$%qwert12345' WITH GRANT OPTION;
FLUSH PRIVILEGES;

SHOW GRANTS FOR "root"


select * from judgment where uuid = "bcbace13-7222-4e36-a297-a89d009cc6f6"


select * from judgment where uuid = "74e17a6b-344a-41f5-b7dd-a8cc0010dd09"

select count(*) from judgment where id <= 500000 and is_crawl = 1


无文本数据统计：
select count(*) from judgment where id < 1000000 and left(doc_content,5) != '$(fun' ;
625
select count(*) from judgment where id > 1000000 and id < 2000000 and  left(doc_content,5) != '$(fun' ;
476
select count(*) from judgment where id > 2000000 and id < 3000000 and  left(doc_content,5) != '$(fun' ;
177
select count(*) from judgment where id > 3000000 and id < 4000000 and  left(doc_content,5) != '$(fun' ;
1177
select count(*) from judgment where id > 4000000 and id < 5000000 and  left(doc_content,5) != '$(fun' ;
2961
select count(*) from judgment where id > 5000000 and id < 6000000 and  left(doc_content,5) != '$(fun' ;
2657
select count(*) from judgment where id > 6000000 and  left(doc_content,5) != '$(fun' ;
72

select id,doc_content,left(doc_content,5) from judgment where left(doc_content,5) != '$(fun' limit 100;

select id,doc_content from judgment where id in (8,16,22,27,34)


select id,doc_content from judgment where is_crawl = 2  limit 100;

select id,doc_content from judgment where is_format = 3 limit 100;
select id,doc_content from judgment where uuid = "afc34630-c38b-4f4d-849b-838d4cd2142f"


select * from judgment where uuid = "b90efbcb-7235-4452-a9ef-828b9a1cdc4e"

create table hbase_uuid_old01 like hbase_uuid_old02;
create table hbase_uuid_old02 like hbase_uuid_old01;
create table hbase_uuid_old03 like hbase_uuid_old01;
create table hbase_uuid_old04 like hbase_uuid_old01;

create table b like a;
insert ignore into a(uuid,uuid_old) select uuid,uuid_old from b;

hbase_uuid_old01:948400
hbase_uuid_old02:4766332
hbase_uuid_old03:5028782
hbase_uuid_old04:27876671


insert ignore into hbase_uuid_old04(uuid,uuid_old) select uuid,uuid_old from hbase_uuid_old01;
insert ignore into hbase_uuid_old03(uuid,uuid_old) select uuid,uuid_old from hbase_uuid_old02;

insert into hbase_uuid_old04(uuid,uuid_old) select uuid,uuid_old from hbase_uuid_old03;


insert into hbase_uuid_old04(uuid,uuid_old) select uuid,uuid_old from hbase_uuid_old_zhixing;


select count(*) from judgment_3_new where caseid = "" or caseid is null;
# 849727

select count(*) from judgment_3_new where left(doc_content,4) != "$(fu" 
# 0

GRANT ALL PRIVILEGES ON *.* TO 'weiwc'@'%' IDENTIFIED BY 'HHly2017.' WITH GRANT OPTION;
FLUSH PRIVILEGES;


select * from judgment_3_new where  CHAR_LENGTH(uuid) > 36
select * from judgment_3_new where  doc_content not like "%var jsonHtmlData = \"{%" limit 5;

create table invalid as 
select * from judgment_3_new a left join uuids b on a.uuid = b.uuid_old where b.uuid_old is null;

select * from all_uuid where uuid = "c50d5572-2845-46ea-aa33-a91500c25b18"
select * from judgment_2 where uuid = "c50d5572-2845-46ea-aa33-a91500c25b18"

create table record_1 as select * from judgment_2 where uuid = "c50d5572-2845-46ea-aa33-a91500c25b18";

select count(*) from judgment where is_format > 8;


alter table judgment_doc drop column case_content,
add column flag tinyint(1),
add index flag(flag);

EXPLAIN 
update judgment set is_format = 9 where id < 100000 and exists(select 1 from uuid_wenshu_gov where uuid = judgment.uuid)

create table judgment_filter as 
select uuid,doc_content from judgment where id >= 150000 and id < 1000000 
and exists(select 1 from uuid_wenshu_gov where uuid = judgment.uuid);

insert into judgment_filter(uuid,doc_content)  
select uuid,doc_content from judgment where id >= 1000000 
and exists(select 1 from uuid_wenshu_gov where uuid = judgment.uuid);
==========================
create table judgment_doc_filter as 
select * from judgment_doc where exists(select 1 from uuid_wenshu_gov where uuid = judgment_doc.uuid);
==============
flume测试： 
create table flume_wenshu as select * from judgment_3_new limit 10000;

