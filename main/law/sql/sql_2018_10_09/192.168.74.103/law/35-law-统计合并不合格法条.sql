UPDATE law_rule_result2 SET lawlist_id = id 

SELECT id,art_num,art_num_new,lawlist_id from law_rule_result2 where art

-- 统计二审不合格的lawlist
create table lawlist_uuids_2shen_error as  SELECT title_short,art_num,uuids,uuids_len from lawlist_uuids_2shen_all where id not in (
SELECT a.id from lawlist_uuids_2shen_all a ,law_rule_result2 b where a.title_short = b.title_short and a.art_num = b.art_num ) 
order by uuids_len desc

-- 统计一审不合格的lawlist
create table lawlist_uuids_1shen_error as  SELECT title_short,art_num,uuids,uuids_len from lawlist_uuids_1shen_all where id not in (
SELECT a.id from lawlist_uuids_1shen_all a ,law_rule_result2 b where a.title_short = b.title_short and a.art_num = b.art_num ) 
order by uuids_len desc
7782
7775
110

-- 更新一审、二审的type值
UPDATE lawlist_uuids_1shen_error set type = 1
UPDATE lawlist_uuids_2shen_error set type = 2

-- 合并一审、二审的error表到一张export_error表：
create table export_error as (SELECT title_short,art_num,uuids_len,type,flag from lawlist_uuids_1shen_error) UNION 
(SELECT title_short,art_num,uuids_len,type,flag from lawlist_uuids_2shen_error) order by uuids_len desc


-- 统计export_error中title_short小于50个字符的数据：
create table export_error_lower50 as  SELECT * from export_error where CHAR_LENGTH(title_short) < 50 
order by uuids_len  desc

-- 统计export_error中title_short小于50个字符,且uuids_len大于等于10的数据：
create table export_error_lower50_great10 as  SELECT * from export_error where CHAR_LENGTH(title_short) < 50 and uuids_len >= 10 
order by uuids_len  desc


-- length:返回字符串所占的字节数，是计算字段的长度一个汉字是算三个字符,一个数字或字母算一个字符
-- char_length:返回字符串所占的字符数，不管汉字还是数字或者是字母都算是一个字符

SELECT casedate,court_new, LENGTH(casedate),CHAR_LENGTH(casedate),LENGTH(court_new),CHAR_LENGTH(court_new),
 (LENGTH(casedate)+LENGTH(court_new)) as sums  from judgment_etl where id < 100 order by (LENGTH(casedate)+LENGTH(court_new)) desc 

SELECT id,title_short,CHAR_LENGTH(title_short),uuids_len from export_error where CHAR_LENGTH(title_short) > 60 
order by CHAR_LENGTH(title_short) desc LIMIT 1500




SELECT id,title_short from export_error limit 100

select id,art_num,art_num_new from law_rule_result2 where id < 1246837 and art_num_new = '0' limit 10

select id,art_num,art_num_new from law_rule_result2 where id = 2880869  limit 10

select * from lawlist_uuids_1shen_all order by art_num desc


ALTER TABLE  law_rule_result2 ADD INDEX title_short(title_short), ADD INDEX art_num(art_num); 


SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;

SELECT * from lawlist_uuids_1shen_all where title_short ='最高人民法院关于适用财产刑若干问题的规定' and art_num='第二条'

select @@sql_mode;

=================================
SELECT COUNT(*) from laws

SELECT COUNT(*) from laws where type = '1' and id < 454 and title_right is not null

SELECT COUNT(*) from laws where type = '2' and id < 454 and title_right is not null



SELECT COUNT(*) from lawlist_uuids_2shen_error where CHAR_LENGTH(title_short) < 50 and uuids_len >= 10

SELECT COUNT(*) from export_error_lower50_great10

SELECT * from laws where count >= 10 and title_right is null order by count desc

UPDATE lawlist_uuids_1shen_all a ,laws b set a.title_short = b.title_right,a.art_num = b.num where a.title_short = b.title and b.type = '1'
UPDATE lawlist_uuids_2shen_all a ,laws b set a.title_short = b.title_right,a.art_num = b.num where a.title_short = b.title and b.type = '2'

CREATE table lawlist_uuids_2shen_all like lawlist_uuids_1shen_all;

SELECT COUNT(*) from lawlist_uuids_2shen_all  GROUP BY title_short,art_num HAVING(COUNT(*) >1)

-- 更新lawlist_uuids_1shen_all中的flag,lawlist_id
UPDATE lawlist_uuids_1shen_all a ,law_rule_result2 b set a.lawlist_id = b.lawlist_id , a.flag = '1'  where a.title_short = b.title_short and a.art_num = b.art_num 

UPDATE lawlist_uuids_2shen_all a ,law_rule_result2 b set a.lawlist_id = b.lawlist_id , a.flag = '1'  where a.title_short = b.title_short and a.art_num = b.art_num 

CREATE table uuids_lawlist_id_1shen as SELECT lawlist_id,uuids from lawlist_uuids_1shen_all where flag = '1' and lawlist_id is not null
CREATE table uuids_lawlist_id_2shen as SELECT lawlist_id,uuids from lawlist_uuids_2shen_all where flag = '1' and lawlist_id is not null


SELECT  * from uuids_lawlist_id_1shen where uuids is null or uuids = '' or lawlist_id is null or lawlist_id = ''


SELECT * from lawlist_uuids_1shen_all where uuids = 'd2229323-dba8-47a4-b864-dcda7e15a2b7'

SELECT * from law_rule_result2 where title_short = '最高人民法院关于刑事裁判涉财产部分执行的若干规定'


SELECT * from law_rule_result2 where  id > 2880860
