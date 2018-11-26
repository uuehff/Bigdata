--  DELETE from tb_doc where id in (
--  select tt3.idd from 
--   (select tt.id as idd from (select id as id from tb_doc as t,
--  	(SELECT CONCAT(caseid,title,casedate) as c from tb_doc as a GROUP BY CONCAT(caseid,title,casedate) HAVING(COUNT(*)>1)) as tmp 
--  	where CONCAT(t.caseid,t.title,t.casedate) = tmp.c ) as tt WHERE tt.id not in 
--  (SELECT min(id) as id2 from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1)) as tt3
--  )
-- 725,588s

-- select CONCAT(caseid,title,casedate),COUNT(*) from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1  60314
-- DELETE from tb_doc where id in (select t.tid from (SELECT max(id) as tid from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1) as t ) 60314,4min
-- 第二次：
-- select CONCAT(caseid,title,casedate),COUNT(*) from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1  4864，这是至少有三条重复记录的
-- DELETE from tb_doc where id in (select t.tid from (SELECT max(id) as tid from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1) as t )

select CONCAT(caseid,title,casedate),COUNT(1) from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1  1583,9min
-- DELETE from tb_doc where id in (select t.tid from (SELECT max(id) as tid from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1) as t ) 1583

-- DELETE from tb_doc where id in (select t.tid from (SELECT max(id) as tid from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1) as t ) 652,198s
-- DELETE from tb_doc where id in (select t.tid from (SELECT max(id) as tid from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1) as t ) 478
-- DELETE from tb_doc where id in (select t.tid from (SELECT max(id) as tid from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1) as t ) 376,162s
Show index from tb_doc;
-- alter table tb_doc add unique index union_index(casedate,title,caseid);
-- ALTER TABLE tb_doc ENGINE=InnoDB;
-- SELECT id,caseid,title,casedate,LENGTH(caseid) t,LENGTH(title) t2,LENGTH(casedate) t3 from tb_doc order by t3 desc limit 50;
-- DELETE from tb_doc where id = 1981032

-- select id,CONCAT(caseid,title,casedate) from tb_doc where CONCAT(caseid,title,casedate) = '（2015）章刑初字第68号-陈某某故意伤害案一审刑' null
-- select id,CONCAT(caseid,title,casedate) from tb_doc where CONCAT(caseid,title,casedate) like  '（2015）章刑初字第68号-陈某某故意伤害案一审刑%'
select id,caseid,title,casedate from tb_doc where title = '陈某某故意伤害案一审刑'
select COUNT(*) from tb_doc where id <= 1000000
SELECT * FROM tb_doc WHERE id = 2592142
select CONCAT(round(sum(DATA_LENGTH/1024/1024), 2),'MB') AS data FROM `TABLES` WHERE TABLE_NAME='tb_doc';

update tb_doc set type='0' where type='一审';

SELECT type from judgment WHERE id > 2500000 limit 20

SELECT SUBSTRING(casedate,1,7),COUNT(1) from judgment where id <= 1000000 group by  SUBSTRING(casedate,1,7)

SELECT uuid from judgment where is_format = 0 LIMIT 100

show index from tem_hzj
alter table judgment add index is_crawl(is_crawl);
alter table judgment add index is_format(is_format),add index doc_from(doc_from);


CREATE TABLE tmp_weiwenchao3 SELECT id,uuid,type,casedate,lawlist from judgment where id <= 10
alter table tem_hzj add unique index uuid(uuid);

SELECT id,uuid,type,casedate from tb_doc where id
select count(*) from judgment where id <= 500000;
select count(*) from tmp_weiwenchao where id > 500000 and id <= 2000000;
select id,uuid,lawlist from judgment where id > 500000 and id <= 2000000 and lawlist is null;
select id,uuid,lawlist from tmp_weiwenchao where id > 2120000 and id <= 2130000 and lawlist is not null;
select id,uuid,lawlist from tmp_weiwenchao where id > 1876050 and id <= 1876060 ;

alter table judgment_etl add unique index uuid(uuid);

select COLUMN_NAME from information_schema.COLUMNS where table_name = 'judgment' and table_schema = 'laws_doc';

INSERT  into tmp_weiwenchao(id,uuid,type,casedate) SELECT id,uuid,type,casedate from judgment where id > 2000000
DELETE from tmp_weiwenchao where 1 =1 
id,uuid,lawlist
SELECT COUNT(*) from civil.tb_doc ;

select uuid, casedate, type, reason, fact_finder, judge_member, judge_result, is_format, id from judgment where is_format=1 and id>=1 and id<=10
CREATE TABLE tmp_test SELECT * from tmp_liufang where 1 = 2 

alter table judgment modify column defendant text(0);
alter table adjudication modify column history text(0);
alter table decision modify column history text(0);
alter table inform modify column history text(0);
alter table mediate modify column history text(0);
alter table other modify column history text(0);

Waiting for table metadata lock

Waiting for table metadata lock

ALTER TABLE `judgment`
MODIFY COLUMN `defendant`  text CHARACTER SET utf8 COLLATE utf8_general_ci NULL AFTER `party_info`

select COUNT(*) from judgment where id > 0 and id < 1876058 and lawlist is null

UPDATE `civil`.`tb_doc` SET `id`='1', `doc_id`='5c59fcac-2bc6-42ca-bd3e-a761000dde9b', `doc_title`='北京博宇嘉物业管理有限公司与赵福志物业服务合同纠纷一审民事判决书', `doc_date`='2017-04-17', `doc_time`='2017-04-27 20:51:43', `doc_court`='北京市门头沟区人民法院', `doc_num`='（2017）京0109民初2129号', `is_crawled`='1', `is_format`='0' WHERE (`id`='1');

CREATE table civil.content_test as select * from civil.tb_content where 1 =3
uuid,lawlist
select  from judgment where id >= 1876058 and id <= 2100000























