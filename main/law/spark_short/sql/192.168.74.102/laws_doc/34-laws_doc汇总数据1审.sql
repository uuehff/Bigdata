-- 创建宽表

CREATE table judgment_etl SELECT a.*,
court_new,doc_oriligigation_new,record_time_new,casedate_new,duration,defendant_new,plaintiff_new,
judge_chief_new,judge_member_new,if_adult,if_surrender,if_nosuccess,if_accumulate,
crime_reason,fact_finder_new,punish_cate,punish_date,delay_date,punish_money,
law_office,d.province,city,district,court_cate,court,
gender,nation,edu,suspect_num,birth_day,native_place,age_year,reason,crml_team,
j_adult,prvs from tmp_weiwenchao a,tmp_wxy b,tmp_liufang c,tmp_raolu d,tmp_hzj e where 1=2

INSERT into judgment_etl(id,uuid,type,casedate,lawlist,lawlist_1r) SELECT id,uuid,type,casedate,lawlist,lawlist_1r from tmp_weiwenchao where id >  1800000

-- 受影响的行: 1751464
-- 时间: 883.832s

select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_weiwenchao' and table_schema='laws_doc'
id,uuid,type,casedate,lawlist,lawlist_1r,
update judgment_etl j, tmp_weiwenchao t set 
j.lawlist = t.lawlist,
j.lawlist_1r = t.lawlist_1r where t.uuid = j.uuid and t.id <= 1800000;

-- tmp_weiwenchao2为标注结果
select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_weiwenchao2' and table_schema='laws_doc'
id,uuid,type,casedate,doc_content,per,loc,org,time,role,crime

update judgment_etl j, tmp_weiwenchao2 t set 
j.per = t.per,
j.loc = t.loc,
j.org = t.org,
j.time = t.time,
j.role = t.role,
j.crime = t.crime where t.uuid = j.uuid and t.id > 1800000;

select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_wxy' and table_schema='laws_doc'
id,uuid,type,casedate,court_new,doc_oriligigation_new,record_time_new,casedate_new,duration,defendant_new,plaintiff_new,
judge_chief_new,judge_member_new,if_adult,if_surrender,if_nosuccess,if_accumulate

id
uuid
type
casedate
court_new
doc_oriligigation_new
record_time_new
casedate_new
duration
defendant_new
judge_chief_new
judge_member_new
fact_finder_new
if_adult
if_surrender
if_nosuccess
if_accumulate

全字段更新：

注意：j.plaintiff_new = t.plaintiff_new,字段不用！

update judgment_etl j, tmp_wxy t set 
j.court_new = t.court_new,
j.doc_oriligigation_new = t.doc_oriligigation_new,
j.record_time_new = t.record_time_new,
j.casedate_new = t.casedate_new,
j.duration = t.duration,
j.defendant_new = t.defendant_new,
j.judge_chief_new = t.judge_chief_new,
j.judge_member_new = t.judge_member_new,
j.fact_finder_new = t.fact_finder_new,
j.if_adult = t.if_adult,
j.if_surrender = t.if_surrender,
j.if_nosuccess = t.if_nosuccess,
j.if_accumulate = t.if_accumulate where j.uuid = t.uuid ; 

部分字段更新：
update judgment_etl j, tmp_wxy t set 
j.age_min = t.age_min,
j.age_max = t.age_max where j.uuid = t.uuid ;

二次更新部分字段：
update judgment_etl j, tmp_wxy t set 
j.judge_member_new = t.judge_member_new,
j.judge_chief_new = t.judge_chief_new,
j.defendant_new = t.defendant_new,
j.fact_finder_new = t.fact_finder_new,
j.court_new = t.court_new where j.uuid = t.uuid and t.id <= 1800000;

=============
更新judgment_etl中的court_idea,judge_result字段：

update judgment_etl j, tmp_wxy t set 
j.court_idea = t.court_idea_new,
j.judge_result = t.judge_result_new where j.uuid = t.uuid ;

======================================
更新judgment_etl中的court_new字段：

update judgment_etl j, tmp_wxy t set 
j.court_new = t.court_new where j.uuid = t.uuid ;
======================================
更新judgment_etl中的court_new字段：

update judgment_etl j, tmp_wxy t set 
j.if_guity = t.if_guity,
j.org_plaintiff = t.org_plaintiff,
j.org_defendant = t.org_defendant,
j.dispute = t.dispute where j.uuid = t.uuid ;

==================================
select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_liufang' and table_schema='laws_doc'
id,uuid,casedate,type,province,doc_oriligigation,crime_reason,fact_finder_new,punish_cate,punish_date,delay_date,if_delay,control_date
lock_date,punish_money,if_right,right_date,reason

注意：j.fact_finder_new = t.fact_finder_new,用tmp_wxy的！

update judgment_etl j, tmp_liufang t set 
j.crime_reason = t.crime_reason,
j.punish_cate = t.punish_cate,
j.punish_date = t.punish_date,
j.delay_date = t.delay_date,
j.if_delay = t.if_delay,
j.control_date = t.control_date,
j.lock_date = t.lock_date,
j.punish_money = t.punish_money,
j.if_right = t.if_right,
j.right_date = t.right_date,
j.reason = t.reason where t.uuid = j.uuid;


update judgment_etl j, tmp_liufang t set 
j.degree = t.degree where t.uuid = j.uuid ;

==================
select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_raolu' and table_schema='laws_doc'
id,uuid,type,casedate,law_office,province,city,district,court_cate,court,new_office,new_lawyer

更新全部字段：
update judgment_etl j, tmp_raolu t set 
j.law_office = t.law_office,
j.province = t.province,
j.city = t.city,
j.district = t.district,
j.court_cate = t.court_cate,
j.court = t.court,
j.new_office = t.new_office,
j.new_lawyer = t.new_lawyer where t.uuid = j.uuid ;

更新：
update judgment_etl j, tmp_raolu t set 
j.new_office = t.new_office,
j.new_lawyer = t.new_lawyer where t.uuid = j.uuid;

更新province：
update judgment_etl j, tmp_raolu t set 
j.province = t.province where t.uuid = j.uuid;

===========================
select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_hzj' and table_schema='laws_doc'
province,gender,nation,edu,edu_new,suspect_num,birth_day,native_place,age_year,reason,crml_team,j_adult,prvs,new_reason

update judgment_etl j, tmp_hzj t set 
j.gender = t.gender,
j.nation = t.nation,
j.edu = t.edu,
j.edu_new = t.edu_new,
j.suspect_num = t.suspect_num,
j.birth_day = t.birth_day,
j.native_place = t.native_place,
j.age_year = t.age_year,
j.crml_team = t.crml_team,
j.j_adult = t.j_adult,
j.prvs = t.prvs,
j.new_reason = t.new_reason where j.uuid = t.uuid ; 

============
update judgment_etl j, tmp_hzj t set 
j.age_year = t.age_year,
j.edu_new = t.edu_new where j.uuid = t.uuid ; 

=======================
更新tmp_footer表的doc_footer字段：

update judgment_etl j, tmp_footer t set 
j.doc_footer = t.doc_footer where j.uuid = t.uuid ; 


SELECT * from tmp_weiwenchao2 where id >= 1179000 and id <= 1200001
SELECT * from tmp_weiwenchao2 where id > 955000 and id < 958000   219

SELECT * from tmp_weiwenchao2 where id > 1495000 and id < 1495000  24
SELECT * from tmp_weiwenchao2 where id > 1340000 and id <= 1350000  24

SELECT * from tmp_weiwenchao2 where id >= 1000000 and id <= 1500000 and loc is null and per is null
SELECT COUNT(*) from judgment where id <= 100000 

SELECT * from tmp_weiwenchao2 where id >= 500000 and id <= 1000000 and loc is null and per is null   10242
SELECT * from tmp_weiwenchao2 where id >= 0 and id <= 1800000 and loc is null and per is null   5513
-- 7025条
-- 17532,前10万都OK了
==============================================================
更新一审lawlist_ids字段：

update judgment_etl j, uuid_and_lawlist_ids_1shen_result t set 
j.lawlist_ids = t.lawlist_ids where j.uuid = t.uuid;

-- update judgment_etl j 
-- INNER JOIN uuid_and_lawlist_ids_1shen_result t 
-- on j.uuid = t.uuid
-- set j.lawlist_ids = t.lawlist_ids;

更新二审lawlist_ids字段：
update laws_doc2.judgment2 j, laws_doc2.uuid_and_lawlist_ids_2shen_result t set 
j.lawlist_ids = t.lawlist_ids where j.uuid = t.uuid ;

SELECT id,uuid,doc_content from judgment where id = 268656
268656	645198ad-9b60-46dd-90c2-6d177dcd25d5	0	2016-10-27							
268657	469b5956-7116-4815-9b6a-1ef972117e16	0	2016-12-14							
268658	b887cf29-3145-44e6-8ef6-a723012851bd	0	2016-12-22							
268659	a08efaae-7e31-4930-bc80-f6935c15f078	0	2016-01-20							



select a.id,a.uuid,a.doc_content from judgment a,tmp_weiwenchao2 b where a.uuid = b.uuid and b.id <= 30000 and  b.loc is null
update tmp_weiwenchao2 set LOC ='江苏省句容市,江苏省宜兴市金三角小商品市场,江苏省句容市,安徽省黄山市黄山区仙源镇水东村红庙组的山林里（北纬30°18\',江苏省宜兴市,安徽省黄山市黄山区仙源镇水东村红庙组的山林里（北纬30°18\',江苏省宜兴市,安徽省黄山市黄山区仙源镇水东村红庙组的山林里（北纬30°18\',安徽省黄山市黄山区仙源镇水东村红庙组的山林里,黄山市黄山区仙源镇水东村红庙组古墓葬年' where uuid= '5c635db9-9aa0-492a-a807-fe0e0e91be3d'

9013
10920
23709
23710
24664


SELECT * from tmp_weiwenchao2 where id >= 1193816  and id <= 1194999

SELECT id,doc_content from judgment where id = 899000

-- 2127296
-- """"["《中华人民共和国刑法》第五十三条", "《中华人民共和国刑法》第五十六条第一款", "《中华人民共和国刑法》第六十四条", "《中华人民共和国刑法》第二百六十三条第（四）项", "《中华人民共和国刑法》第三十六条第一款", "《中华人民共和国刑法》第五十二条", "《中华人民共和国刑法》第二百六十三条第（五）项", "《中华人民共和国刑法》第五十五条第一款", "《中华人民共和国民法通则》第一百一十九条"]""""

-- "["《中华人民共和国刑法》第三百零三条第二款", "《中华人民共和国刑法》第六十四条", "《中华人民共和国刑法》第六十七条第三款"]"
SELECT id,uuid,lawlist from tmp_weiwenchao where id >= 1876056 and id <= 2127296 and lawlist = '"["《中华人民共和国刑法》第三百零三条第二款", "《中华人民共和国刑法》第六十四条", "《中华人民共和国刑法》第六十七条第三款"]"'
SELECT id,uuid,lawlist from judgment where id >= 1962689 and id <= 1983521

-- 685635 到 686000
-- 696297到 700000
SELECT * from tmp_weiwenchao2 where id >= 685635 and id <= 686001

SELECT * from tmp_weiwenchao2 where id >= 696297 and id <= 700000

-- 2127296,2824916

-- [2127296,2824916]

SELECT id , uuid , casedate, lawlist from judgment where id >= 2824900 and id <= 2824916

2824900	98c90f82-e91c-4a8e-97e0-1b17bf85f812	2015-02-09	["《中华人民共和国刑法》第一百三十三条之一", "《最高人民法院关于处理自首和立功具体应用法律若干问题的解释》第一条"]
2824901	8c4b0408-43c7-4d91-9ebc-6fbf66b64f76	2015-08-03	["《中华人民共和国刑法》第二百二十四条第二项", "《中华人民共和国刑法》第六十四条", "《中华人民共和国刑法》第六十七条第三款"]
2824902	523a5108-6af1-4b5a-8e28-bf448c93b444	2015-01-12	["《中华人民共和国刑法》第二百六十四条", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第一条第一款", "《中华人民共和国刑法》第七十三条第二款", "《中华人民共和国刑法》第二百六十四条第三款", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第十四条", "《中华人民共和国刑法》第七十二条第一款", "《中华人民共和国刑法》第六十七条第三款"]
2824903	50942f47-5377-415e-bf67-08b75845a3af	2015-11-09	["《中华人民共和国刑法》第一百六十二条之一"]
2824904	81945197-fa98-488d-bf93-bea75430365d	2015-09-19	["《中华人民共和国刑法》第一百三十三条之一", "《最高人民法院关于处理自首和立功具体应用法律若干问题的解释》第一条"]
2824905	6de5c6d8-7167-49ae-8d4e-a72b008a37c0	2017-01-26	["《中华人民共和国刑法》第二百六十四条", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第十四条", "《中华人民共和国刑法》第六十七条第三款", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第一条", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第三条第二款"]
2824906	b32cf060-5bf0-4110-8873-a72b008a37f3	2017-01-23	["《中华人民共和国刑法》第二百六十四条", "《中华人民共和国刑法》第七十七条第一款", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第十四条", "《中华人民共和国刑法》第六十九条", "《中华人民共和国刑法》第六十七条第三款", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第一条"]
2824907	4c3631ef-0adc-43bf-9a1f-a72b008a44c4	2017-01-18	["《中华人民共和国刑法》第一百三十三条之一"]
2824908	9fb04cd7-6054-4c56-a12b-48e8196d12f3	2016-04-11	["《中华人民共和国刑法》第二十五条第一款", "《中华人民共和国刑法》第三百零三条第三款", "《最高人民法院、最高人民检察院关于办理赌博刑事案件具体应用法律若干问题的解释》第一条第二项", "《中华人民共和国刑法》第六十九条第一款", "《中华人民共和国刑法》第七十三条第二款", "《最高人民法院、最高人民检察院关于办理赌博刑事案件具体应用法律若干问题的解释》第一条第三项", "《中华人民共和国刑法》第七十二条第一款", "《中华人民共和国刑法》第二十七条", "《中华人民共和国刑法》第三百零三条第四款", "《中华人民共和国刑法》第六十四条", "《中华人民共和国刑法》第七十七条第一款", "《中华人民共和国刑法》第三百零三条第一款", "《中华人民共和国刑法》第六十七条第三款", "《中华人民共和国刑法》第二十六条第一款", "《最高人民法院、最高人民检察院关于办理赌博刑事案件具体应用法律若干问题的解释》第一条第一项"]
2824909	cb3d61db-5de1-4111-9778-051a9a8e7130	2015-01-12	["《中华人民共和国刑法》第二百六十四条", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第一条第一款", "《中华人民共和国刑法》第六十五条第一款", "《中华人民共和国刑法》第六十四条", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第十四条", "《最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释》第三条第一款", "《中华人民共和国刑法》第六十七条第三款"]


SELECT id , uuid , type,casedate,lawlist from tmp_weiwenchao where id >= 2824900 and id <= 2824916
SELECT id , uuid , type,casedate,lawlist from tmp_weiwenchao where id >= 2127934 and id <= 2127946

SELECT casedate_new, court_cate, court_new, crime_reason, duration,fact_finder_new from judgment_etl  LIMIT 10

SELECT reason from judgment limit 5
