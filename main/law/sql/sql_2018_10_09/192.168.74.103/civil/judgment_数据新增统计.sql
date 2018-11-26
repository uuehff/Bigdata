数据说明：11295127之前（包括id=11295127）的是第一批数据，其中只处理了"判决书"。

处理1结果:judgment_add560wan_etl：df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.12.35:3306/civil', 
table='(select id,uuid,doc_content from judgment where id > 11295127 and id < 12307681 ) tmp',
column='id',lowerBound=11295127,upperBound=12307681,numPartitions=24,
properties={"user": "root", "password": "HHly2017."})

处理2结果：judgment_add560wan_etl01：table=(select id,uuid,doc_content,judge_type from judgment where id > 0 and id <= 1500000 ,这里的条件judge_type != "判决"无效，因此需要全部读进去，再过滤。

处理3结果：judgment_add560wan_etl02：select id,uuid,doc_content from judgment where id > 1500000 and id <= 3000000 这里的条件judge_type != "判决"无效，因此需要全部读进去，再过滤。

select count(*) from judgment 16437623  
select * from judgment where is_crawl = "0" limit 10
8218084
12307681
12307709
12307825
12307971
12308002
12308006
12308064
12308146
12308159

select min(id) from judgment where id <= 1000000 and judge_type != "判决";


select count(*) from judgment where is_format = "1"; 12309680
select * from judgment where id = 12309000

select * from judgment where id <= 11295127 and doc_from != "limai" and doc_from != "legalminer_com" limit 10;
select count(*) from judgment where id <= 11295127 and is_format = "1";  11020000
select min(id),max(id),count(*) from judgment where id <= 11295127 and judge_type != "判决";


select id,uuid,doc_content,judge_type from judgment where id > 0 and id <= 150 and judge_type != "判决"

非判决书有550万
insert into implement_civil_etl select * from implement_civil_etl2;

create table judgment_add560wan_part_etl01 as select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where 1=2;
create table judgment_add560wan_part_etl02 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl03 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl04 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl05 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl06 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl07 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl08 like judgment_add560wan_part_etl01;
create table judgment_add560wan_part_etl like judgment_add560wan_part_etl01;


INSERT into judgment_add560wan_part_etl01(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id <= 1500000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl02(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 1500000 and id <= 3000000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl03(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 3000000 and id <= 4500000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl04(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 4500000 and id <= 6000000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl05(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 6000000 and id <= 7500000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl06(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 7500000 and id <= 9000000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl07(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 9000000 and id <= 10500000 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl08(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 10500000 and id <= 11295127 and judge_type != "判决";
INSERT into judgment_add560wan_part_etl(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 11295127 and id < 12307681 ;

 
alter table judgment_add560wan_etl08
add caseid varchar(80),
add title varchar(220),
add court varchar(255),
add court_uid varchar(255),
add lawlist text,
add law_id text,
add casedate varchar(255),
add reason_type varchar(255),
add type varchar(255),
add judge_type varchar(255),
add reason varchar(255),
add reason_uid varchar(255),
add province varchar(250),
add plt_claim mediumtext,
add dft_rep mediumtext,
add crs_exm mediumtext;

update judgment_add560wan_part_etl08
set type =
case
when type = "0" then "1"
when type = "1" then "2"
when type = "2" then "3"
when type = "3" then "4"
when type = "4" then "5"
end;

update judgment_add560wan_etl08 a ,judgment_add560wan_part_etl08 b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;


create table judgment_add560wan_all like judgment_add560wan_etl;
insert into judgment_add560wan_all select * from judgment_add560wan_etl;
insert into judgment_add560wan_all select * from judgment_add560wan_etl01;
insert into judgment_add560wan_all select * from judgment_add560wan_etl02;
insert into judgment_add560wan_all select * from judgment_add560wan_etl03;
insert into judgment_add560wan_all select * from judgment_add560wan_etl04;
insert into judgment_add560wan_all select * from judgment_add560wan_etl05;
insert into judgment_add560wan_all select * from judgment_add560wan_etl06;
insert into judgment_add560wan_all select * from judgment_add560wan_etl07;
insert into judgment_add560wan_all select * from judgment_add560wan_etl08;

二次新增数据统计：
==================
select * from judgment where is_crawl = "0" limit 10

13516113 - 12307681 = 1208432
=====================
13516113
13519877
13520020
13520076
13520536
13520622
===============================================================
第三次新增数据统计：起始点12307680

spark分批处理：
1： id > 12307680 and id <= 13300000
2：id > 13300000 and id <= 14300000
3：id > 14300000 and id <= 15300000
4：id > 15300000 and id <= 16437624
共有id：16437624


新增300万处理：实际新增大约：3307627
create table judgment_add300wan_part_etl01 like judgment_add560wan_part_etl01;
create table judgment_add300wan_part_etl02 like judgment_add560wan_part_etl01;
create table judgment_add300wan_part_etl03 like judgment_add560wan_part_etl01;
create table judgment_add300wan_part_etl04 like judgment_add560wan_part_etl01;


INSERT into judgment_add300wan_part_etl01(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 12307680 and id <= 13300000 and is_crawl = "1" ;
INSERT into judgment_add300wan_part_etl02(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 13300000 and id <= 14300000 and is_crawl = "1" ;
INSERT into judgment_add300wan_part_etl03(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 14300000 and id <= 15300000 and is_crawl = "1" ;
INSERT into judgment_add300wan_part_etl04(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 15300000 and id <= 16437624 and is_crawl = "1" ;


create table judgment_add300wan_all like judgment_add300wan_etl01;
insert into judgment_add300wan_all select * from judgment_add300wan_etl01;
insert into judgment_add300wan_all select * from judgment_add300wan_etl02;
insert into judgment_add300wan_all select * from judgment_add300wan_etl03;
insert into judgment_add300wan_all select * from judgment_add300wan_etl04;


create table judgment_add300wan_part_all like judgment_add300wan_part_etl01;
insert into judgment_add300wan_part_all select * from judgment_add300wan_part_etl01;
insert into judgment_add300wan_part_all select * from judgment_add300wan_part_etl02;
insert into judgment_add300wan_part_all select * from judgment_add300wan_part_etl03;
insert into judgment_add300wan_part_all select * from judgment_add300wan_part_etl04;


alter table judgment_add300wan_all
add caseid varchar(80),
add title varchar(220),
add court varchar(255),
add court_uid varchar(255),
add lawlist text,
add law_id text,
add casedate varchar(255),
add reason_type varchar(255),
add type varchar(255),
add judge_type varchar(255),
add reason varchar(255),
add reason_uid varchar(255),
add province varchar(250),
add plt_claim mediumtext,
add dft_rep mediumtext,
add crs_exm mediumtext;

update judgment_add300wan_part_all
set type =
case
when type = "0" then "1"
when type = "1" then "2"
when type = "2" then "3"
when type = "3" then "4"
when type = "4" then "5"
end;

mysql> select reason_type,judge_type,type,count(*) from judgment_add300wan_part_all group by reason_type,judge_type,type;
+-------------+------------+------+----------+
| reason_type | judge_type | type | count(*) |
+-------------+------------+------+----------+
| 民事        | 判决       | 0    |  3307629 |
+-------------+------------+------+----------+
update judgment_add300wan_part_all set type = "1";


update judgment_add300wan_all a ,judgment_add300wan_part_all b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;


select count(*) from judgment where id > 12307680 and  is_crawl = "1"  #3307627

14089359 - 12307680= 1781679
select *  from judgment where id > 12307680 and  is_crawl = "0"  limit 50

select *  from judgment where id > 14089359 and  is_crawl = "1"  limit 50
14089359
14089362
14089364
14089365
14089368
14089372
14089377
14089378


==================================================================
==================================================================
第四次新增数据统计：起始点12307680,新增大约80万

spark分批处理：
1： id > 12307680 and id <= 16437624 and is_crawl = "21" 


judgment表共有id：16437624


select * from judgment where id > 12307680 and is_crawl = "21"  limit 100


新增80万处理：实际新增大约：
create table judgment_add80wan_part_etl01 like judgment_add560wan_part_etl01;
INSERT into judgment_add80wan_part_etl01(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 12307680 and is_crawl = "21" ;


CREATE table judgment_add80wan_etl01 like laws_doc_judgment_add300wan.judgment_add300wan_etl01;


alter table judgment_add80wan_etl01
add caseid varchar(80),
add title varchar(220),
add court varchar(255),
add court_uid varchar(255),
add lawlist text,
add law_id text,
add casedate varchar(255),
add reason_type varchar(255),
add type varchar(255),
add judge_type varchar(255),
add reason varchar(255),
add reason_uid varchar(255),
add province varchar(250),
add plt_claim mediumtext,
add dft_rep mediumtext,
add crs_exm mediumtext,
add PRIMARY key(id);

update judgment_add80wan_part_etl01
set type =
case
when type = "0" then "1"
when type = "1" then "2"
when type = "2" then "3"
when type = "3" then "4"
when type = "4" then "5"
end;

mysql> select reason_type,judge_type,type,count(*) from judgment_add80wan_part_etl01 group by reason_type,judge_type,type;
+-------------+------------+------+----------+
| reason_type | judge_type | type | count(*) |
+-------------+------------+------+----------+
| 民事        | 判决       | 1    |  821356   
+-------------+------------+------+----------+


update judgment_add80wan_etl01 a ,judgment_add80wan_part_etl01 b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;


select count(*) from judgment where id > 12307680 and  is_crawl = "1"  #3307627

select *  from judgment where id > 12307680 and  is_crawl = "21"  limit 50




