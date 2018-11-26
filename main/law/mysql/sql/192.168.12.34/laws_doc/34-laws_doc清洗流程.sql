select doc_from,is_crawl,is_format from tb_doc

show index from tmp_weiwenchao2
alter table judgment add index is_crawl(is_crawl);
alter table judgment add index is_format(is_format);
alter table judgment add index doc_from(doc_from);


EXPLAIN select uuid from tb_doc where uuid > 1 and is_crawl=0

方法一：
1.CREATE TABLE laws_doc.tmp_weiwenchao2 SELECT id,uuid,type,casedate,doc_content from laws_doc.judgment where 1 = 2 
2.-- 接着添加主键，修改引擎
3.alter table laws_doc.tmp_weiwenchao2 add unique index uuid(uuid);
alter table laws_doc.tmp_weiwenchao2 add unique index uuid(uuid);

4.每次读取原始字段id,uuid,type,casedate 10万行，处理后插入lawlist字段。
INSERT  into tmp_weiwenchao(id,uuid,type,casedate) SELECT id,uuid,type,casedate from tb_doc where id < 100000

方法二：

1.一次将原表中的id,uuid,type,casedate值插入过来，

CREATE table tmp_weiwenchao2 as SELECT id,uuid,type,casedate from tb_doc where id < 100
2.-- 接着添加主键，修改引擎
3. alter table tmp_weiwenchao2 add unique index uuid(uuid);
4.添加新的字段
5.每次读取原始字段id,uuid,type,casedate 10万行，处理后插入lawlist字段。
INSERT  into tmp_weiwenchao2(id,uuid,type,casedate) SELECT id,uuid,type,casedate from tb_doc where id < 100000
=========================================
select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name='tmp_raolu' and table_schema='laws_doc'


CREATE table judgment_part as select id,title,doc_reason,doc_oriligigation,fact_finder,record_time,timeline,party_info,defendant,plaintiff,third,trial_process,trial_request,trial_reply,court_find,court_idea,judge_result,judge_chief,judge_member,history,reason_type,judge_type,result_type,update_time,doc_from from judgment;

2016-03-08
SELECT id,record_time_new from judgment_etl where id >= 2000000 and id <= 2100000 and record_time_new is not null and record_time_new not like '____-__-__'
SELECT id,record_time_new from judgment_etl where id >= 2000000 and id <= 2100000 and record_time_new is not null and record_time_new like '____-__-__' limit 10

SELECT record_time_new from judgment_etl  limit 10
