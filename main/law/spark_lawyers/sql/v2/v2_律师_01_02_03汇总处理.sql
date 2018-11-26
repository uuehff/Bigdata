-- 查询表的名称或字段：
-- select *
-- from information_schema.tables 
-- where table_schema in 
-- (select schema_name from information_schema.SCHEMATA  
-- where schema_name like "laws_doc_%" and schema_name != "laws_doc2" 
-- and schema_name not like "laws_doc_lawyers%" and schema_name != "laws_doc_mediate"
-- )
-- and (table_name like "%_field" or table_name like "%_lawyer" or table_name like "%_organization" ) 
-- order by right(table_name,1)

-- select table_schema,table_name 
-- from information_schema.tables 
-- where table_schema = "laws_doc_lawyers_new" and table_name like "%match"
-- in 
-- (select schema_name from information_schema.SCHEMATA  
-- where schema_name like "laws_doc_%" and schema_name != "laws_doc2" 
-- and schema_name not like "laws_doc_lawyers%" and schema_name != "laws_doc_mediate"
-- )
-- and (table_name like "%_field" or table_name like "%_lawyer" or table_name like "%_organization" ) 
-- order by right(table_name,1)


-- select DISTINCT COLUMN_NAME from INFORMATION_SCHEMA.Columns 
-- where table_schema='laws_doc_lawyers_new' 
-- and table_name like "hht_lawyer_%" 
-- and table_name not like "hht_lawyer_12348%" 
-- and table_name not like "hht_lawyer_v2" 
-- and table_name not like "%_add" 
-- and table_name not like "%_match" 
-- order by column_name;

创建法网与律协三字段匹配的表结构：
create table hht_lawyer_all_collect_match( 
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
name varchar(255) default '',
pra_number varchar(255) default '',
org_name varchar(255) default '',
age varchar(255) default '',
area varchar(255) default '',
birth_date varchar(255) default '',
biyexueyuan varchar(255) default '',
city varchar(255) default '',
edu_origin varchar(255) default '',
first_pra_time varchar(255) default '',
gender varchar(255) default '',
id_num varchar(255) default '',
mail varchar(255) default '',
nation varchar(255) default '',
org_identity varchar(255) default '',
phone varchar(255) default '',
politics varchar(255) default '',
practicestatus varchar(255) default '',
pra_course varchar(255) default '',
pra_type varchar(255) default '',
province varchar(255) default '',
qua_number varchar(255) default '',
qua_time varchar(255) default '',
xuewei varchar(255) default '',
zhuanye varchar(255) default '');

create table hht_lawyer_all_collect_add like hht_lawyer_all_collect_match;

-- 去重字段名：
-- select DISTINCT COLUMN_NAME from INFORMATION_SCHEMA.Columns 
-- where table_schema='laws_doc_lawyers_new' 
-- and table_name = "hht_lawyer_12348gov_v3"
-- order by column_name;

-- 查询字段名：
-- select * from INFORMATION_SCHEMA.Columns 
-- where table_schema='laws_doc_lawyers_new' 
-- and table_name like "hht_lawyer_%" 
-- and table_name not like "hht_lawyer_12348%" 
-- and table_name not like "hht_lawyer_v2" 
-- and table_name not like "%_add" 
-- and table_name not like "%_match" 
-- and (
-- column_name = "user_link" 
-- or column_name = "xuewei" 
-- or column_name = "zhuanye" 
-- or column_name = "biyexueyuan" 
-- or column_name = "edu_origin" 
-- or column_name = "area_code" 
-- or column_name = "qua_type" 
-- ) order by column_name;

-- select * from INFORMATION_SCHEMA.Columns 
-- where table_schema='laws_doc_lawyers_new' 
-- and table_name like "hht_lawyer_%" 
-- and table_name not like "hht_lawyer_12348%" 
-- and table_name not like "hht_lawyer_v2" 
-- and table_name not like "%_add" 
-- and table_name not like "%_match" 
-- and (column_name = "user_link" 
-- or column_name = "org_full" 
-- or column_name = "qualifytime" 
-- or column_name = "qua_time" 
-- or column_name = "qua_type" 
-- or column_name = "xuewei" 
-- or column_name = "zhuanye" 
-- or column_name = "biyexueyuan" 
-- or column_name = "edutime" 
-- or column_name = "edu_origin" 
-- or column_name = "email" 
-- or column_name = "firstpracticetime" 
-- or column_name = "first_pra_time" 
-- or column_name = "mail"
-- ) order by column_name;


-- select * from hht_lawyer_bsgs where qualifytime is not null and qualifytime != ""
-- select * from hht_lawyer_bsgs where zhuanye is not null and zhuanye != ""
-- select * from hht_lawyer_bsgs where edu_origin is not null and edu_origin != ""

-- ==============================================================
-- ==============================================================
-- ==============================================================

-- 根据行政区域代码，更新省、市
-- select * from hht_lawyer_gansu a join area_code_v3 b on left(a.area_code,4) = b.area_id
-- update hht_lawyer_gansu a join area_code_v3 b on left(a.area_code,4) = b.area_id
-- set a.province = b.province,a.city = b.city ;
-- 
-- update hht_lawyer_gansu_add a join area_code_v3 b on left(a.area_code,4) = b.area_id
-- set a.province = b.province,a.city = b.city ;
-- 
-- update hht_lawyer_gansu_match a join area_code_v3 b on left(a.area_code,4) = b.area_id
-- set a.province = b.province,a.city = b.city ;
-- 
-- update hht_lawyer_gansu set province = "甘肃省";
-- update hht_lawyer_gansu_match set province = "甘肃省";
-- update hht_lawyer_gansu_add set province = "甘肃省";
-- =========================================================
-- 
hht_lawyer_all_collect_add去重：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_all_collect_add where pra_number = "" or pra_number is null;
delete from hht_lawyer_all_collect_add where name = "" or name is null;
delete from hht_lawyer_all_collect_add where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_all_collect_add where pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

SELECT name,org_name,count(*) from hht_lawyer_all_collect_add where 
pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89' 
group by name,org_name 
having(count(*) > 1);

SELECT * from hht_lawyer_all_collect_add where name = "于彬"

hht_lawyer_all_collect_add按正则与hht_lawyer_12348gov_v3_missing

SELECT * from hht_lawyer_all_collect_add a join hht_lawyer_12348gov_v3_missing b 
on a.pra_number = b.pra_number and a.name = b.name 
where a.pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' 
or hex(a.pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89' 
order by a.pra_number,a.name,a.org_name; 


统计删除重复的数据：
SELECT * from hht_lawyer_12348gov_v3 a join hht_lawyer_12348gov_v3_missing b 
on a.pra_number = b.pra_number and a.name = b.name ;

delete b from hht_lawyer_12348gov_v3 a join hht_lawyer_12348gov_v3_missing b 
on a.pra_number = b.pra_number and a.name = b.name ;

select * from hht_lawyer_12348gov_v3 a join hht_lawyer_12348gov_v3_missing b 
on a.pra_number = b.pra_number and a.name = b.name ;

insert into hht_lawyer_all_collect_add(name,pra_number,org_name,area,years,province,city,source)
select name,pra_number,org_name,area,years,province,city,source from hht_lawyer_12348gov_v3_missing;

select * from hht_lawyer_all_collect_add where pra_number in (
select pra_number from hht_lawyer_12348gov_v3_missing
)
SELECT count(*) from hht_lawyer_12348gov_v3 a join hht_lawyer_all_collect_match b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name;
完全属于hht_lawyer_12348gov_v3；

-- SELECT count(*) from hht_lawyer_12348gov_v3 a join hht_lawyer_all_collect_add b 
-- on a.name = b.name and a.org_name = b.org_name where a.id < 100000;

SELECT count(*) from hht_lawyer_12348gov_v3 a join hht_lawyer_all_collect_add b 
on a.pra_number = b.pra_number;
为0；


select * from hht_lawyer_all_collect_add where 
pra_number in 
(select pra_number from hht_lawyer_all_collect_add group by pra_number,name,org_name having(count(*) > 1)) 
order by pra_number;

create table hht_lawyer_all_collect_add_distinct like hht_lawyer_all_collect_add;
spark合并处理三字段一样的重复数据；

重复数据已另外合并，在这里删除；
delete from hht_lawyer_all_collect_add where 
pra_number in (
select b.pra_number from 
(select pra_number from hht_lawyer_all_collect_add group by pra_number,name,org_name having(count(*) > 1)) b
)

删除执业证号重复的数据，查询与删除是同一个表，不能直接删除，需内嵌一个查询；
delete from hht_lawyer_all_collect_add where 
pra_number in (select b.pra_number from  
(SELECT pra_number from hht_lawyer_all_collect_add group by pra_number having(count(*) > 1)) b )
and source is null;

delete from hht_lawyer_all_collect_add where id in (43993,43998,44032,44036,44592,44941,44955,44956,45065,45213,45215,45243)

查询按pra_number,name,org_name分组后大于1的数据：
select * from hht_lawyer_all_collect_add_distinct where 
pra_number in (
select b.pra_number from 
(select pra_number from hht_lawyer_all_collect_add_distinct group by pra_number,name,org_name having(count(*) > 1)) b
)
order by pra_number

create table hht_lawyer_all_collect_add_distinct_v2 like hht_lawyer_all_collect_add_distinct;

select * from hht_lawyer_all_collect_add a join hht_lawyer_12348gov_v3 b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 
order by a.id;

重新插入去重后的数据：
insert into hht_lawyer_all_collect_add(name,pra_number,org_name,age,area,birth_date,biyexueyuan,city,edu_origin,first_pra_time,gender,id_num,mail,nation,org_identity,phone,politics,practicestatus,pra_course,pra_type,province,qua_number,qua_time,xuewei,zhuanye,years)
 select name,pra_number,org_name,age,area,birth_date,biyexueyuan,city,edu_origin,first_pra_time,gender,id_num,mail,nation,org_identity,phone,politics,practicestatus,pra_course,pra_type,province,qua_number,qua_time,xuewei,zhuanye,years from hht_lawyer_all_collect_add_distinct;

准备合并hht_lawyer_all_collect_add到hht_lawyer_all_collect_match中：

insert into hht_lawyer_all_collect_match(name,pra_number,org_name,age,area,birth_date,biyexueyuan,city,edu_origin,first_pra_time,gender,id_num,mail,nation,org_identity,phone,politics,practicestatus,pra_course,pra_type,province,qua_number,qua_time,xuewei,zhuanye,years)
 select name,pra_number,org_name,age,area,birth_date,biyexueyuan,city,edu_origin,first_pra_time,gender,id_num,mail,nation,org_identity,phone,politics,practicestatus,pra_course,pra_type,province,qua_number,qua_time,xuewei,zhuanye,years from hht_lawyer_all_collect_add;

准备合并hht_lawyer_12348gov_v3到hht_lawyer_all_collect_match中：
insert into hht_lawyer_all_collect_match(pra_number,name,org_name,gender,province,city,nation,edu_origin,politics,org_identity,birth_date,pra_type,pra_course,first_pra_time,qua_number,qua_time,years)
 select pra_number,name,org_name,gender,province,city,nation,edu_origin,politics,org_identity,birth_date,pra_type,pra_course,first_pra_time,qua_number,qua_time,years from hht_lawyer_12348gov_v3;



gov_v3中的字段：
pra_number,name,org_name,gender,province,city,nation,edu_origin,politics,org_identity,
birth_date,pra_type,pra_course,first_pra_time,qua_number,qua_time,years

create table hht_lawyer_all_collect_match_result like hht_lawyer_all_collect_match;
使用spark进行汇总处理；

select count(*) from hht_lawyer_all_collect_match_result where source = "gov_v3"
select * from hht_lawyer_all_collect_match_result where source is null  

针对source is null 单独处理每个字段：
create table hht_lawyer_all_collect_match_result_add as 
select * from hht_lawyer_all_collect_match_result where source is null ;



SELECT * from hht_lawyer_all_collect_match_result where 
pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' or
hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89'


update hht_lawyer_all_collect_match_result set pra_number = replace(pra_number,"	","");
update hht_lawyer_all_collect_match_result set pra_number = replace(pra_number,"a","A");
update hht_lawyer_all_collect_match_result set pra_number = replace(pra_number,"b","B");
update hht_lawyer_all_collect_match_result set pra_number = replace(pra_number,"c","C");

删除pra_number除去带+和-的，且符合正则的数据：
delete from hht_lawyer_all_collect_match_result where 
pra_number REGEXP '[ 	,:;\\()!@.|"\'/]|\\?|\\]|\\[' or
hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89'

delete from hht_lawyer_all_collect_match_result where id in (130381,73908,208747)


select * from hht_lawyer_all_collect_match_result where 
pra_number REGEXP '[m-p 	,:;\\()!@.|"\'/]|\\?|\\]|\\[' or
hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89'

update hht_lawyer_all_collect_match_result set pra_number = "16401201011165313" where pra_number = "16401201011165313ljn"

SELECT * from hht_lawyer_all_collect_match_result where name REGEXP '[a-z0-9A-Z 	,:;-\\()!+@|"\'/]|\\?|\\]|\\[' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

select * from hht_lawyer_all_collect_match_result where CHAR_LENGTH(name) > 3 and name not like "%.·%"
delete from hht_lawyer_all_collect_match_result where name = "文"

select name,count(*) from hht_lawyer_all_collect_match_result  where CHAR_LENGTH(name) > 4 and (name like "%.%" or name like "%·%") group by name having(count(*) > 1)

update hht_lawyer_all_collect_match_result set name = replace(name,".","·")

select name,count(*) from hht_lawyer_all_collect_match_result  where CHAR_LENGTH(name) > 4 and (name like "%.%" or name like "%·%") group by pra_number,name,org_name having(count(*) > 1)
无结果；

update hht_lawyer_all_collect_match_result set org_name = replace(org_name,"（","(");
update hht_lawyer_all_collect_match_result set org_name = replace(org_name,"）",")");

SELECT * from hht_lawyer_all_collect_match_result where org_name REGEXP '[a-z0-9A-Z 	,:;-\\+!@.|"\'/]|\\?|\\]|\\[' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

select * from hht_lawyer_all_collect_match_result  where CHAR_LENGTH(org_name) < 7

delete from hht_lawyer_all_collect_match_result where CHAR_LENGTH(org_name) = 2

执业证号、律所一样，姓名不一样：
select pra_number,org_name,count(*) from hht_lawyer_all_collect_match_result  group by pra_number,org_name having(count(*)>1)
无结果；

姓名、律所一样，执业证号不一样：
select * from hht_lawyer_all_collect_match_result a join 
(select name,org_name from hht_lawyer_all_collect_match_result  group by name,org_name having(count(*)>1) ) b
on a.name=b.name and a.org_name=b.org_name  order by a.name,a.org_name;


select * from hht_lawyer_all_collect_match_result a join 
(select name,org_name from hht_lawyer_all_collect_match_result  group by name,org_name having(count(*)>1) ) b
on a.name=b.name and a.org_name=b.org_name 
where a.pra_number not in (select pra_number from zy_lawyer_12348gov) order by a.name,a.org_name;

update hht_lawyer_all_collect_match_result set politics = "中国共产党员",practicestatus = "正常" where id = 52881
delete from hht_lawyer_all_collect_match_result where id = 121173;
delete from hht_lawyer_all_collect_match_result where id = 208331;


SELECT * from hht_lawyer_all_collect_match_result where org_name = "湖南衡州律师事务所" and name = "丁卫平"
SELECT * from hht_lawyer_all_collect_match_result where right(pra_number,2) = "00"


delete a  from hht_lawyer_all_collect_match_result a join 
(select name,org_name from hht_lawyer_all_collect_match_result  group by name,org_name having(count(*)>1) ) b
on a.name=b.name and a.org_name=b.org_name where right(a.pra_number,2) = "00" ;

delete a  from hht_lawyer_all_collect_match_result a join 
(select name,org_name from hht_lawyer_all_collect_match_result  group by name,org_name having(count(*)>1) ) b
on a.name=b.name and a.org_name=b.org_name where a.source is null or  a.source = "" ;

删除不在原始12348中的数据：
delete a from hht_lawyer_all_collect_match_result a join 
(select name,org_name from hht_lawyer_all_collect_match_result  group by name,org_name having(count(*)>1) ) b
on a.name=b.name and a.org_name=b.org_name 
where a.pra_number not in (select pra_number from zy_lawyer_12348gov)


select count(*) from hht_lawyer_all_collect_match_result where source is not null and source != "gov_v3"

姓名、执业证号一样，律所不一样：
select * from hht_lawyer_all_collect_match_result a join 
(select pra_number,name from hht_lawyer_all_collect_match_result  group by pra_number,name having(count(*)>1) ) b
on a.name=b.name and a.pra_number=b.pra_number order by a.pra_number,a.name;
无结果；

-- 统计hht_lawyer_all_collect_match_result中的数据：
-- select * from hht_lawyer_all_collect_match_result
-- where name in (
-- SELECT name from hht_lawyer_all_collect_match_result 
-- group by name,right(pra_number,12)
-- having(count(*) > 1)) 
-- order by name desc;
-- 
-- 
-- select * from hht_lawyer_all_collect_match_result
-- where name in (
-- SELECT name,concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7)) as p from hht_lawyer_all_collect_match_result 
-- group by name,concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7))
-- having(count(*) > 3)) 
-- order by name desc;
-- 
-- create table hht_lawyer_all_collect_match_result_pra_number_part_group as 
-- select a.* from hht_lawyer_all_collect_match_result a join 
-- (SELECT name,concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7)) as p from hht_lawyer_all_collect_match_result 
-- group by name,concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7))
-- having(count(*) > 1)) b  
-- on a.name = b.name and concat(substr(a.pra_number,1,1),substr(a.pra_number,6,4),substr(a.pra_number,11,7)) = b.p 
-- order by b.name,b.p desc;
-- 


-- select a.* from hht_lawyer_all_collect_match_result a join 
-- (SELECT name,concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7)) as p from hht_lawyer_all_collect_match_result 
-- group by name,concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7))
-- having(count(*) > 1)) b  
-- on a.name = b.name and concat(substr(a.pra_number,1,1),substr(a.pra_number,6,4),substr(a.pra_number,11,7)) = b.p 
-- -- where CHAR_LENGTH(a.pra_number) < 17 
-- order by b.name,b.p desc;
-- 


select * from hht_lawyer_all_collect_match_result where pra_number = "16540199611165956hs"
group by practicestatus ;


select * from hht_lawyer_all_collect_match_result CHAR_LENGTH(pra_number) < 17
group by practicestatus ;

update hht_lawyer_all_collect_match_result set practicestatus = "" where practicestatus = "其他";
update hht_lawyer_all_collect_match_result set practicestatus = "正常执业" where practicestatus = "执业";
update hht_lawyer_all_collect_match_result set practicestatus = "正常执业" where practicestatus = "正常";
update hht_lawyer_all_collect_match_result set practicestatus = "正常执业" where practicestatus = "正常";

create table zy_lawyer_12348gov_pra_number as select id,pra_number from zy_lawyer_12348gov;



SELECT * from zy_lawyer_12348gov_pra_number where pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number," ","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,'"',"");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"。","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"？","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"?","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"‘","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"：","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"‘","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"，","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,".","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,"’","");
update zy_lawyer_12348gov_pra_number set pra_number = replace(pra_number,",","");
delete from zy_lawyer_12348gov_pra_number where CHAR_LENGTH(pra_number) < 6;

select * from hht_lawyer_all_collect_match_result where practicestatus = "注销" and source = "gov_v3";
select pra_number,org_name,pra_course,pra_course_not,area,province,city from hht_lawyer_all_collect_match_result where pra_course is not null;
select pra_number,org_name,pra_course,pra_course_not from hht_lawyer_all_collect_match_result where pra_number like "144042017_0093226";


select * from hht_lawyer_all_collect_match_result where name like "%龙雄%";
select * from hht_lawyer_all_collect_match_result_pra_number_part_group where name like "%龙雄%";


select org_name,pra_course,pra_course_not from hht_lawyer_all_collect_match_result 
where pra_course is null 
and pra_course_not is not null 
and pra_course_not != "" 
and pra_course_not not like  '%首次执业"}';

update hht_lawyer_all_collect_match_result set pra_course = NULL 
where pra_course is not null and pra_course = "" 

update hht_lawyer_all_collect_match_result set pra_course = NULL 
where pra_course is not null and pra_course = "" 

update hht_lawyer_all_collect_match_result set pra_course = NULL 
where pra_course is not null and pra_course like  '%首次执业"}';

update hht_lawyer_all_collect_match_result set pra_course = NULL 
where pra_course is not null and pra_course  like  '%首次执业';

update hht_lawyer_all_collect_match_result 
set pra_course = pra_course_not 
where pra_course is null 
and pra_course_not is not null 
and pra_course_not != "" 
and pra_course_not not like  '%首次执业"}';

update hht_lawyer_all_collect_match_result set pra_course = replace(pra_course,"）",")");
update hht_lawyer_all_collect_match_result set pra_course = replace(pra_course,"（","(");
update hht_lawyer_all_collect_match_result_pra_number_part_group set pra_course = replace(pra_course,"（","(");
update hht_lawyer_all_collect_match_result_pra_number_part_group set pra_course = replace(pra_course,"）",")");


select name, concat(substr(pra_number,1,1),substr(pra_number,6,4),substr(pra_number,11,7)) as p 
from hht_lawyer_all_collect_match_result_pra_number_part_group 
group by name, p 
order by name;

select * from hht_lawyer_all_collect_match_result_pra_number_part_group  
where CHAR_LENGTH(pra_number) > 17

delete from hht_lawyer_all_collect_match_result 
where pra_number in (select pra_number from hht_lawyer_all_collect_match_result_pra_number_part_group)

create table hht_lawyer_all_collect_match_result_111 like hht_lawyer_all_collect_match_result;

select id,name,org_name,pra_course,org_names,practicestatus from hht_lawyer_all_collect_match_result 
where pra_course is not null and pra_course like "%:%";

select id,name,org_name,pra_course,org_names,practicestatus from hht_lawyer_all_collect_match_result 
where pra_course is not null order by id

update hht_lawyer_all_collect_match_result_pra_number_part_group 
set pra_course = replace(pra_course,":","：")

update hht_lawyer_all_collect_match_result  
set pra_course = replace(pra_course,":","：")

查看并更新直辖市：
select pra_number,province,city,area from hht_lawyer_all_collect_match_result
where (province = "" or city = "" or province is null or city is null )
and CHAR_LENGTH(pra_number) = 17 and city in ("上海市","北京市","天津市","重庆市");

update hht_lawyer_all_collect_match_result set province = city 
where (province = "" or city = "" or province is null or city is null )
and CHAR_LENGTH(pra_number) = 17 and city in ("上海市","北京市","天津市","重庆市");

select a.pra_number,a.province,a.city,a.area,b.province,b.city 
from hht_lawyer_all_collect_match_result a 
join area_code_v3 b on substr(a.pra_number,2,4) = b.area_id 
where CHAR_LENGTH(a.pra_number) = 17;


关联行政代码，更新省市：
update hht_lawyer_all_collect_match_result a 
join area_code_v3 b on substr(a.pra_number,2,4) = b.area_id 
set a.province = b.province,
a.city = b.city 
where CHAR_LENGTH(a.pra_number) = 17;

select pra_number,province,city,area from hht_lawyer_all_collect_match_result
where (province = "" or province is null  )
and CHAR_LENGTH(pra_number) = 17 ;




关联行政代码，查看省市：
select a.pra_number,a.province,a.city,a.area,b.province,b.city from hht_lawyer_all_collect_match_result a 
join area_code_v3 b on concat(substr(a.pra_number,2,2),"01") = b.area_id 
where CHAR_LENGTH(a.pra_number) = 17 and (a.province = "" or a.province is null  ) 
order by b.province;

关联行政代码，更新省市：
update hht_lawyer_all_collect_match_result a 
join area_code_v3 b on concat(substr(a.pra_number,2,2),"01") = b.area_id 
set a.province = b.province 
where CHAR_LENGTH(a.pra_number) = 17 and (a.province = "" or a.province is null  );

=======================================================================
================通过查看area，关联行政代码，统计省市数据，完善省市字段：
=======================================================================
update  hht_lawyer_all_collect_match_result 
set city = SUBSTRING_INDEX(area,'-',1) 
where (province = "" or province is null  )
and CHAR_LENGTH(pra_number) = 17
and area like "%-%" ;


update  hht_lawyer_all_collect_match_result a join area_code_v3 b 
on a.city = b.city 
set a.province = b.province 
where CHAR_LENGTH(a.pra_number) != 17 


update  hht_lawyer_all_collect_match_result a join area_code_v3 b 
on a.city = b.city 
set a.province = b.province 
where (a.province = "" or a.province is null  )
and CHAR_LENGTH(a.pra_number) = 17
and a.area like "%-%" ;

update  hht_lawyer_all_collect_match_result  
set province = "河南省",
city = "郑州市" where pra_number = "14015201410517150";



update hht_lawyer_all_collect_match_result a 
set a.province = a.city 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and city = "上海市" ;

select a.pra_number,a.province,a.city,a.area from hht_lawyer_all_collect_match_result a 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and area is not null 
and area != "" 
and area like "%省";

update hht_lawyer_all_collect_match_result a 
set a.province = a.area  
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and area is not null 
and area != "" 
and area like "%省";


select a.pra_number,a.province,a.city,a.area,SUBSTRING_INDEX(a.area,'-',1) from hht_lawyer_all_collect_match_result a 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and area is not null 
and area != "" 
and area not like "河南省" 
and area like "%-%" 
;


update  hht_lawyer_all_collect_match_result a join area_code_v3 b 
on a.city = b.city 
set a.province = b.province 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and a.area is not null 
and a.area != "" 
and a.area not like "河南省" 
and a.area like "%-%" 
;

select a.pra_number,a.province,a.city,a.area,SUBSTRING_INDEX(a.area,'-',1) from hht_lawyer_all_collect_match_result a 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and area is not null 
and area != "" 
and area not like "河南省" 
and area not like "%-%" 
;

update hht_lawyer_all_collect_match_result a join area_code_v3 b 
on concat(substr(a.area,1,2),"01") = b.area_id 
set a.province = b.province 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null or a.city = "" or a.city is null) 
and area is not null 
and area != "" 
and area not like "河南省" 
and area not like "%-%" 
;

select a.pra_number,a.province,a.city,a.area,SUBSTRING_INDEX(a.area,'-',1) from hht_lawyer_all_collect_match_result a 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null) 
and area is not null 
and area != "" 
and area not like "河南省" 
and area not like "%-%" 
;

update hht_lawyer_all_collect_match_result 
set province = "海西蒙古族藏族自治州" 
where pra_number in ("163282041510857793","1632820170429600");


update hht_lawyer_all_collect_match_result a
set province = "新疆维吾尔自治区" 
where CHAR_LENGTH(a.pra_number) != 17 
and 
(a.province = "" or a.province is null) 
and area is not null 
and area != "" 
and area not like "河南省" 
and area not like "%-%" 
and area = "新疆建设兵团";



update hht_lawyer_all_collect_match_result a
set city = "西宁市" ,
province = "青海省"
where pra_number = "28631705120058";


select * from area_code_v3 where area_id like "41%";
select * from area_code_v3 where city = "西宁市";

select * from hht_lawyer_all_collect_match_result where 
 province is null or ( province is not null and province = "" )

select substr(org_name,1,2),count(*) from hht_lawyer_all_collect_match_result where 
 province is null or ( province is not null and province = "" ) group by substr(org_name,1,2)
order by substr(org_name,1,2) desc

select a.pra_number,a.org_name,substr(a.org_name,1,2),b.province from hht_lawyer_all_collect_match_result a 
join area_code_v3 b 
on substr(a.org_name,1,2) = substr(b.province,1,2)
where  a.province is null or ( a.province is not null and a.province = "" ) 
and substr(b.area_id,3,2) = "01" ;


update hht_lawyer_all_collect_match_result a 
join area_code_v3 b 
on substr(a.org_name,1,2) = substr(b.province,1,2)
set a.province = b.province 
where  a.province is null or ( a.province is not null and a.province = "" ) 
and substr(b.area_id,3,2) = "01" ;


update hht_lawyer_all_collect_match_result a 
join area_code_v3 b 
on substr(a.org_name,1,2) = substr(b.city,1,2)
set a.province = b.province,
a.city = b.city  
where a.province is null or ( a.province is not null and a.province = "" ) ;

select * from area_code_v3 where city = "仙桃市"

select pra_number,org_name,province,city,area,
SUBSTRING_INDEX(SUBSTRING_INDEX(org_name,")",1),"(",-1) from hht_lawyer_all_collect_match_result where 
 org_name like "%(%)%" 
 and substr(city,1,2) != substr(SUBSTRING_INDEX(SUBSTRING_INDEX(org_name,")",1),"(",-1),1,2)

-- ( province = substr(org_name,1,2) is not null or ( province is not null and province = "" ))
-- and org_name like "%(%)%"

update hht_lawyer_all_collect_match_result 
set city_tmp = 
SUBSTRING_INDEX(SUBSTRING_INDEX(org_name,")",1),"(",-1)  where 
 org_name like "%(%)%" 
 and substr(city,1,2) != substr(SUBSTRING_INDEX(SUBSTRING_INDEX(org_name,")",1),"(",-1),1,2)


select * from hht_lawyer_all_collect_match_result a join area_code_v3 b 
on substr(a.city_tmp,1,2) = substr(b.city,1,2) 
where a.city_tmp is not null;

update hht_lawyer_all_collect_match_result a join area_code_v3 b 
on substr(a.city_tmp,1,2) = substr(b.city,1,2) 
set a.province = b.province,
a.city = b.city 
where a.city_tmp is not null;

update hht_lawyer_all_collect_match_result set province = "黑龙江省" where id = 247639

有很多不是省份、城市开头的，以及类似：北京金杜上海分所律师事务所，不能从字面断定"北京";
,粗略统计也就几百条，无法通过律所直接判断，需要通过去爬取律所的基本信息；

-- select pra_number,org_name,province,city,area 
-- from hht_lawyer_all_collect_match_result 
-- where substr(org_name,1,2) != substr(province,1,2) 
-- and org_name not like "%(%)%" 
--  and substr(city,1,2) != substr(SUBSTRING_INDEX(SUBSTRING_INDEX(org_name,")",1),"(",-1),1,2)


==============================================================================
==============================================================================
==============================================================================
性别、执业类型处理：
select gender,count(*) from hht_lawyer_all_collect_match_result group by gender;
update hht_lawyer_all_collect_match_result 
set pra_type = 
case
when SUBSTR(pra_number,10,1) = "1" then "专职律师"
when SUBSTR(pra_number,10,1) = "2" then "兼职律师"
when SUBSTR(pra_number,10,1) = "3" then "香港律师"
when SUBSTR(pra_number,10,1) = "4" then "澳门律师"
when SUBSTR(pra_number,10,1) = "5" then "台湾律师"
when SUBSTR(pra_number,10,1) = "6" then "公职律师"
when SUBSTR(pra_number,10,1) = "7" then "公司律师"
when SUBSTR(pra_number,10,1) = "8" then "法律援助律师"
when SUBSTR(pra_number,10,1) = "9" then "军队律师"
else pra_type end,
gender = 
case SUBSTR(pra_number,11,1)
when "0" then "男"
when "1" then "女"
else gender end
where CHAR_LENGTH(pra_number) = 17;

select gender,count(*) from hht_lawyer_all_collect_match_result group by gender;
update hht_lawyer_all_collect_match_result set gender = "" where gender in ("1","2")

select edu_origin,count(*) from hht_lawyer_all_collect_match_result group by edu_origin;
-- '[a-z0-9A-Z 	,:;-\\()!+@|"\'/]|\\?|\\]|\\[' 
update hht_lawyer_all_collect_match_result set edu_origin = "" 
where edu_origin REGEXP '[a-z0-9A-Z]' 

select biyexueyuan,count(*) from hht_lawyer_all_collect_match_result 
where biyexueyuan REGEXP '[a-z0-9A-Z 	,:;-\\()!+@|"\'/]|\\?|\\]|\\['
group by biyexueyuan  
order by count(*) desc ;

update  hht_lawyer_all_collect_match_result set biyexueyuan = "" 
where biyexueyuan = "1399000001107"

update hht_lawyer_all_collect_match_result set biyexueyuan = "" 
where biyexueyuan in ("不详","无","0","00","1") 


select * from hht_lawyer_all_collect_match_result where 
(first_pra_time = "" or first_pra_time is null ) 
and first_pra_time != "" ;
结果为空；


select * from hht_lawyer_all_collect_match_result where 
(birth_date = "" or birth_date is null ) 
and birth_date_not != "" ;
有结果，需要合并birth_date_not 到 birth_date字段；

update hht_lawyer_all_collect_match_result 
set birth_date = birth_date_not 
where (birth_date = "" or birth_date is null ) 
and birth_date_not != "" ;


select first_pra_time,
case SUBSTRING_INDEX(from_unixtime(first_pra_time)," ",1)
when "1970-01-01" then ""
else SUBSTRING_INDEX(from_unixtime(first_pra_time)," ",1) end
 from hht_lawyer_all_collect_match_result where 
first_pra_time is not null 
and first_pra_time != "" 
-- and CHAR_LENGTH(first_pra_time) > 4 
and CHAR_LENGTH(first_pra_time) <= 13 
and first_pra_time not like "%-%"; 


处理首次执业时间、出生日期：
update hht_lawyer_all_collect_match_result 
set first_pra_time = 
case SUBSTRING_INDEX(from_unixtime(first_pra_time)," ",1)
when "1970-01-01" then ""
else SUBSTRING_INDEX(from_unixtime(first_pra_time)," ",1) end 
where 
first_pra_time is not null 
and first_pra_time != "" 
and CHAR_LENGTH(first_pra_time) > 4 
and CHAR_LENGTH(first_pra_time) <= 13 
and first_pra_time not like "%-%"; 

处理带/的日期类型：
select birth_date_not,right(birth_date_not,4) as a,
lpad(SUBSTRING_INDEX(birth_date,"/",1),2,"0") as b,
lpad(SUBSTRING_INDEX(SUBSTRING_INDEX(birth_date,"/",2),"/",-1),2,"0") as c,
concat(right(birth_date,4),"-",lpad(SUBSTRING_INDEX(birth_date,"/",1),2,"0"),"-",lpad(SUBSTRING_INDEX(SUBSTRING_INDEX(birth_date,"/",2),"/",-1),2,"0")) 
from hht_lawyer_all_collect_match_result where 
birth_date like "%/%";

select birth_date,right(birth_date,4) as a,
lpad(SUBSTRING_INDEX(birth_date,"/",1),2,"0") as b,
lpad(SUBSTRING_INDEX(SUBSTRING_INDEX(birth_date,"/",2),"/",-1),2,"0") as c,
concat(right(birth_date,4),"-",lpad(SUBSTRING_INDEX(birth_date,"/",1),2,"0"),"-",lpad(SUBSTRING_INDEX(SUBSTRING_INDEX(birth_date,"/",2),"/",-1),2,"0")) 
from hht_lawyer_all_collect_match_result where 
birth_date like "%/%";

update hht_lawyer_all_collect_match_result 
set birth_date = concat(right(birth_date,4),"-",lpad(SUBSTRING_INDEX(birth_date,"/",1),2,"0"),"-",lpad(SUBSTRING_INDEX(SUBSTRING_INDEX(birth_date,"/",2),"/",-1),2,"0")) 
where birth_date like "%/%";

select birth_date,
case SUBSTRING_INDEX(from_unixtime(birth_date)," ",1)
when "1970-01-01" then ""
else SUBSTRING_INDEX(from_unixtime(birth_date)," ",1) end
 from hht_lawyer_all_collect_match_result where 
birth_date is not null 
and birth_date != "" 
and CHAR_LENGTH(first_pra_time) > 4 
and CHAR_LENGTH(birth_date) <= 13 
and birth_date not like "%-%"; 


update hht_lawyer_all_collect_match_result 
set birth_date = 
case SUBSTRING_INDEX(from_unixtime(birth_date)," ",1)
when "1970-01-01" then ""
else SUBSTRING_INDEX(from_unixtime(birth_date)," ",1) end 
where 
birth_date is not null 
and birth_date != "" 
and CHAR_LENGTH(birth_date) > 4 
and CHAR_LENGTH(birth_date) <= 13 
and birth_date not like "%-%"; 



select pra_number,substring_index(first_pra_time,"-",1),first_pra_time,
substr(pra_number,6,4) 
from hht_lawyer_all_collect_match_result 
where CHAR_LENGTH(first_pra_time) > 4 
and substring_index(first_pra_time,"-",1) < substr(pra_number,6,4) 
and CHAR_LENGTH(pra_number) = 17; 

update hht_lawyer_all_collect_match_result 
set first_pra_time = substr(pra_number,6,4) 
where substring_index(first_pra_time,"-",1) < substr(pra_number,6,4) 
and CHAR_LENGTH(pra_number) = 17; 


select substring_index(first_pra_time,"-",1),first_pra_time,
 birth_date 
from hht_lawyer_all_collect_match_result 
where birth_date != ""  
and substring_index(birth_date,"-",1) + 18 > substr(first_pra_time,1,4) 
and CHAR_LENGTH(pra_number) = 17 
and first_pra_time != ""; 

update  hht_lawyer_all_collect_match_result 
set birth_date = "" 
where birth_date != ""  
and substring_index(birth_date,"-",1) + 18 > substr(first_pra_time,1,4) 
and CHAR_LENGTH(pra_number) = 17 
and first_pra_time != ""; 


select pra_number,birth_date,first_pra_time from hht_lawyer_all_collect_match_result 
where birth_date REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';

select pra_number,birth_date,first_pra_time from hht_lawyer_all_collect_match_result 
where first_pra_time REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';

身份证处理：
select pra_number,id_num from hht_lawyer_all_collect_match_result 
where id_num REGEXP '[ 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';


update hht_lawyer_all_collect_match_result set id_num = replace(id_num," ","")
update hht_lawyer_all_collect_match_result set id_num = replace(id_num,"x","X")
update hht_lawyer_all_collect_match_result set id_num = "" where pra_number = "11201201810046875"

民族处理：
select nation,count(*) from hht_lawyer_all_collect_match_result 
group by nation order by nation;

select pra_number,nation from hht_lawyer_all_collect_match_result 
where nation REGEXP '[0-9a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';

update hht_lawyer_all_collect_match_result set nation = replace(nation," ","")
update hht_lawyer_all_collect_match_result set nation = "" where nation = "361a460e552b4cfaa3dd2a5d0"
update hht_lawyer_all_collect_match_result set nation = "蒙古族" where nation = "蒙";
update hht_lawyer_all_collect_match_result set nation = "蒙古族" where nation = "蒙古";
update hht_lawyer_all_collect_match_result set nation = "蒙古族" where nation = "蒙族";
update hht_lawyer_all_collect_match_result set nation = "" where nation = "其他民族";
update hht_lawyer_all_collect_match_result set nation = "" where nation = "其他";
update hht_lawyer_all_collect_match_result set nation = "回族" where nation = "回";
update hht_lawyer_all_collect_match_result set nation = "汉族" where nation = "汉";
delete from hht_lawyer_all_collect_match_result where nation = '测试族';
delete from hht_lawyer_all_collect_match_result where nation = '族';
delete from hht_lawyer_all_collect_match_result where nation = '男族';

update hht_lawyer_all_collect_match_result set nation = "满族" where nation = "满";
update hht_lawyer_all_collect_match_result set nation = "锡伯族" where nation = "锡伯";

所内身份处理：
select org_identity,count(*) from hht_lawyer_all_collect_match_result 
group by org_identity order by count(*) desc;

select pra_number,org_identity from hht_lawyer_all_collect_match_result 
where org_identity like "%无%"


update hht_lawyer_all_collect_match_result set org_identity = "律师" 
-- where org_identity = "lawyer";
where org_identity in ("lvshi","l律师") ;

update hht_lawyer_all_collect_match_result set org_identity = "" 
-- where org_identity like "%事务所";
-- where org_identity like "%无%";
where org_identity in ("是","否");


update hht_lawyer_all_collect_match_result set org_identity = "" 
where org_identity in ("0","123","58224131","*","/","root_khlblsywxt_zw_hhr","root_khlblsywxt_zw_ls");

邮箱、电话处理：
select mail,count(*) from hht_lawyer_all_collect_match_result 
where mail like "%11111%" or mail like "%11." group by mail;

update hht_lawyer_all_collect_match_result set mail = "" 
where mail like "%11111%" or mail like "%11.";

select pra_number,phone from hht_lawyer_all_collect_match_result 
where phone REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';

update hht_lawyer_all_collect_match_result set phone = replace(phone," ","");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'"',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'u3000',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'，(',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'/1',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'?',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,',0',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,',1',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,';1',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'手机号码	150766',"");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'（',"(");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'）',")");
update hht_lawyer_all_collect_match_result set phone = replace(phone,'\\',"/");

update hht_lawyer_all_collect_match_result set phone = replace(phone,',',"") 
where pra_number in ("15133201311741887","12102200311688799","15133201110767724");

政治面貌处理：
select politics,count(*) from hht_lawyer_all_collect_match_result 
where politics REGEXP '[0-9a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[' 
group by politics order by count(*) desc;


select pra_number,phone from hht_lawyer_all_collect_match_result 
where phone REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';

update hht_lawyer_all_collect_match_result 
set politics = replace(politics," ","") 
where politics REGEXP '[0-9a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';


update hht_lawyer_all_collect_match_result 
set politics = "" 
where politics REGEXP '[0-9a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';

执业状态处理：
select practicestatus,count(*) from hht_lawyer_all_collect_match_result 
-- where politics REGEXP '[0-9a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[' 
group by practicestatus order by count(*) desc;

资格证号、资格证获取时间：
select qua_number,qua_number_not from hht_lawyer_all_collect_match_result 
where left(qua_number,1) not in ("A","B","C") 
and left(qua_number_not,1) in ("A","B","C") 

update hht_lawyer_all_collect_match_result 
set qua_number = qua_number_not 
where left(qua_number,1) not in ("A","B","C") 
and left(qua_number_not,1) in ("A","B","C") ;

select qua_number,qua_number_not from hht_lawyer_all_collect_match_result 
where (qua_number is null or qua_number = "" ) 
and qua_number_not != "" 
and CHAR_LENGTH(qua_number_not) > 4;

update hht_lawyer_all_collect_match_result 
set qua_number = qua_number_not,
qua_time = qua_time_not 
where (qua_number is null or qua_number = "" ) 
and qua_number_not != "" 
and CHAR_LENGTH(qua_number_not) > 4;

============================================

select pra_number,qua_number,qua_time,SUBSTRING_INDEX(from_unixtime(qua_time)," ",1) from hht_lawyer_all_collect_match_result 
-- where phone REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';
where 
qua_time != "" and (
CHAR_LENGTH(qua_time) < 4 or CHAR_LENGTH(qua_time) > 4 ) 
and qua_time not like "%-%";

update hht_lawyer_all_collect_match_result set qua_time = "" 
where qua_time != "" and (CHAR_LENGTH(qua_time) < 4 ) ;

update hht_lawyer_all_collect_match_result 
set qua_time = SUBSTRING_INDEX(from_unixtime(qua_time)," ",1)
where qua_time != "" and CHAR_LENGTH(qua_time) > 4 
and qua_time not like "%-%" ;


select pra_number,qua_number,substr(qua_number,2,4) from hht_lawyer_all_collect_match_result 
where substr(qua_number,1,1) in ("A","B","C");



update hht_lawyer_all_collect_match_result 
set qua_time = "" 
where SUBSTRING_INDEX(first_pra_time,"-",1) <= SUBSTRING_INDEX(qua_time,"-",1) 
and qua_time != "" and first_pra_time != "" ;

update hht_lawyer_all_collect_match_result 
set qua_time = substr(qua_number,2,4)  
where SUBSTRING_INDEX(qua_time,"-",1) < substr(qua_number,2,4)
and qua_time != "" 
and substr(qua_number,1,1) in ("A","B","C");

===========================================
学位处理：
select xuewei,count(*) as c from hht_lawyer_all_collect_match_result 
-- where phone REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';
where xuewei != "" group by xuewei order by c desc;


select xuewei,count(*) c  from hht_lawyer_all_collect_match_result 
where CHAR_LENGTH(xuewei) > 2 and xuewei != "" group by xuewei order by c desc

select xuewei from hht_lawyer_all_collect_match_result 

-- where xuewei like "%不%" group by xuewei;
-- where xuewei like "%未%" group by xuewei;
-- where CHAR_LENGTH(xuewei) < 2 and xuewei != ""  ;
where CHAR_LENGTH(xuewei) = 2 and xuewei != "" and xuewei like "%无%" group by xuewei ;


update  hht_lawyer_all_collect_match_result 
set xuewei = "" 
-- where xuewei like "%不%"; 
-- where xuewei like "%未%" ;
-- where CHAR_LENGTH(xuewei) < 2 and xuewei != ""  ;
-- where CHAR_LENGTH(xuewei) = 2 and xuewei != "" and xuewei like "%无%"  ;
where CHAR_LENGTH(xuewei) = 2 and xuewei != "" and xuewei = "正常"  ;
======================
专业处理：

select zhuanye,count(*) as c from hht_lawyer_all_collect_match_result 
-- where phone REGEXP '[a-zA-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[';
where zhuanye != "" group by zhuanye order by c desc;

update hht_lawyer_all_collect_match_result 
set zhuanye = "法学" where zhuanye = "法学g" ;
=============
years 执业年限处理：
select *  from hht_lawyer_all_collect_match_result 
where years_not is not null or years_not != "";

select pra_number,first_pra_time,years from hht_lawyer_all_collect_match_result 
where first_pra_time is null or first_pra_time = ""

update hht_lawyer_all_collect_match_result 
set years = 2018-substr(first_pra_time,1,4)+1 
where first_pra_time != "";

select pra_number,name,org_name,years,qua_time,org_names from hht_lawyer_all_collect_match_result 
where pra_number = "920072102707"

select pra_number,first_pra_time,years from hht_lawyer_all_collect_match_result 
where first_pra_time is null or first_pra_time = "" and years != "" and qua_time != "";
无结果；(有结果的话需要判断法网的原始years与qua_time的关系，进行取舍)

select pra_number,phone from hht_lawyer_all_collect_match_result 
where (phone like "%-%" or CHAR_LENGTH(phone) < 11 ) 
and phone != "";

select * from hht_lawyer_all_collect_match_result 
where phone != "" and CHAR_LENGTH(phone) > 11;



过滤并合并执业证号后六位+名字重复的数据：
（这里筛选数据，根据情况可能需要使用join更准确，加上name条件）
create table hht_lawyer_all_collect_match_result_right_6_distinct as 
select a.* from hht_lawyer_all_collect_match_result a ,
(select right(pra_number,6) as p6,name from hht_lawyer_all_collect_match_result 
where CHAR_LENGTH(pra_number) = 17 group by right(pra_number,6),name having(count(*) > 1)
) b 
where 
right(a.pra_number,6) = b.p6 
and a.name = b.name 
and CHAR_LENGTH(a.pra_number) = 17 
order by right(a.pra_number,6);


select a.* from hht_lawyer_all_collect_match_result a ,
(select right(pra_number,6) as p6,name from hht_lawyer_all_collect_match_result 
where CHAR_LENGTH(pra_number) = 17 group by right(pra_number,6),name having(count(*) > 1)
) b 
where 
right(a.pra_number,6) = b.p6 
and a.name = b.name 
and CHAR_LENGTH(a.pra_number) = 17 
order by right(a.pra_number,6);

select pra_number,name,years,first_pra_time 
from hht_lawyer_all_collect_match_result  
where years <= 0 or years >= 69 
or first_pra_time < 1949 or first_pra_time > 2018 
or CHAR_LENGTH(first_pra_time) < 4 
or CHAR_LENGTH(first_pra_time) > 10;


update hht_lawyer_all_collect_match_result_right_6_distinct_result 
set years = 0,
first_pra_time = "" 
where years <= 0 or years >= 69 
or first_pra_time < 1949 or first_pra_time > 2018 
or CHAR_LENGTH(first_pra_time) < 4 
or CHAR_LENGTH(first_pra_time) > 10 ;


select pra_number,org_name,name,pra_course from hht_lawyer_all_collect_match_result_right_6_distinct 
where pra_course != "" order by right(pra_number,6)

合并输出结果到：hht_lawyer_all_collect_match_result_right_6表，
合并后在hht_lawyer_all_collect_match_result表中删除hht_lawyer_all_collect_match_result_right_6_distinct中的数据：

delete from hht_lawyer_all_collect_match_result where pra_number in 
(select pra_number from hht_lawyer_all_collect_match_result_right_6_distinct);

合并结果到hht_lawyer_all_collect_match_result中：

insert into hht_lawyer_all_collect_match_result 
select * from hht_lawyer_all_collect_match_result_right_6_distinct_result;

#以下两个sql不能合并
update hht_lawyer_all_collect_match_result 
set years = 0,first_pra_time = "" 
where (first_pra_time < "1949" or first_pra_time > "2018" 
or CHAR_LENGTH(first_pra_time) < 4 
or CHAR_LENGTH(first_pra_time) > 10) and first_pra_time != "" ;

update hht_lawyer_all_collect_match_result 
set years = 0,first_pra_time = "" 
where years <= 0 or years >= 69 ;

修改years的属性为varchar后，更新0为空字符串：
update hht_lawyer_all_collect_match_result  
set years = "" where years <= 0 or years >= 69 ;  #此处比较时会自动将字符串转为整型。
 
=======================================================================
=======================================================================
=======================================================================
从法律快车中补充电话、邮箱到
SELECT * from hht_lawyer_lawtime_filter where pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_lawtime_filter set pra_number = replace(pra_number,".","");
update hht_lawyer_lawtime_filter set pra_number = replace(pra_number,"?","");
=============
SELECT * from hht_lawyer_lawtime_filter where name REGEXP '[a-z0-9A-Z 	,:;-\\()!+@|"\'/]|\\?|\\]|\\[' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
=============
update hht_lawyer_lawtime_filter set org_name = replace(org_name,"（","(");
update hht_lawyer_lawtime_filter set org_name = replace(org_name,"）",")");

SELECT * from hht_lawyer_lawtime_filter where org_name REGEXP '[a-z0-9A-Z 	,:;-\\!+@|"\'/]|\\?|\\]|\\[' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

delete from hht_lawyer_lawtime_filter where org_name = "0"
==============
select * from hht_lawyer_all_collect_match_result a join hht_lawyer_lawtime_filter b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 
where (a.phone is null or a.phone = "") and b.phone != "" ;


SELECT * from hht_lawyer_lawtime_filter where phone REGEXP '[a-zA-Z 	,:;\\!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(phone) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_lawtime_filter set phone = replace(phone,"-","");
update hht_lawyer_lawtime_filter set phone = replace(phone," ","");

update hht_lawyer_all_collect_match_result a join hht_lawyer_lawtime_filter b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 
set a.phone = b.phone 
where (a.phone is null or a.phone = "") and b.phone != "" ;



SELECT * from hht_lawyer_all_collect_match_result where phone REGEXP '[a-zA-Z 	,:;\\!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(phone) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

SELECT phone from hht_lawyer_all_collect_match_result 
where phone != "" and CHAR_LENGTH(phone) != 11

update hht_lawyer_all_collect_match_result set mobile_phone = phone 
where phone != "" and CHAR_LENGTH(phone) = 11;

update hht_lawyer_all_collect_match_result set phone = "" 
where phone != "" and CHAR_LENGTH(phone) = 11;

select phone,mobile_phone from hht_lawyer_all_collect_match_result;
================================================================
生成自己的律师ID，使用lawyers生成：
-- In [10]: print uuid.uuid3(uuid.NAMESPACE_DNS,"http://uat_datalaw.fy13322.com")
-- e779e0fa-5386-3732-b1ab-5252efcbe561
-- ==========lawyers===============
-- 使用"lawyers"生成域名空间
-- print uuid.uuid3(uuid.NAMESPACE_DNS,"lawyers")
-- 1fbcb6db-b89d-3b5d-8059-86ba0e7ef925
-- 基于"lawyers"生成的域名空间"1fbcb6db-b89d-3b5d-8059-86ba0e7ef925",为每个id生成uuid，
-- 为id范围1-100万生成uuid，截取每个uuid的前13位作为lawyer_id（id值100万以内的uuid前13位，
-- 统计后是无重复得）。

-- NAMESPACE_DNS2 = UUID('e779e0fa-5386-3732-b1ab-5252efcbe561')  #法律大数据平台网址生成的域名
-- NAMESPACE_DNS_LAWYERS = UUID('1fbcb6db-b89d-3b5d-8059-86ba0e7ef925')  #律师生成的域名

select count(DISTINCT left(id2,13)) from hht_lawyer_all_collect_match_result_id_to_uuid
结果：100万，说明无重复；
update hht_lawyer_all_collect_match_result_id_to_uuid set 
lawyer_id = left(uuid,13);

update hht_lawyer_all_collect_match_result a 
join hht_lawyer_all_collect_match_result_id_to_uuid b 
on a.id = b.id 
set a.lawyer_id = b.lawyer_id where b.id <= 362293 ;

==================
添加个人简介：
在爬虫数据库汇总带自我简介的字段：
-- select resume from hht_lawyer_anhui where resume != ""; 无数据
select resume from hht_lawyer_bingtuan where resume != "";
-- select resume from hht_lawyer_bsgs where resume != ""; 无数据
select resume from hht_lawyer_guizhou where resume != "";
select resume from hht_lawyer_heilongjiang where resume != "";
select resume from hht_lawyer_jiangxi where resume != "";
select resume from hht_lawyer_lawtime where resume != "";
select resume from hht_lawyer_ningxia where resume != "";
select resume from hht_lawyer_qinghai where resume != "";
select resume from hht_lawyer_shandong where resume != "";


create table lawyers_resume as 
select pra_number,name,org_name,resume from hht_lawyer_bingtuan where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_guizhou where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_heilongjiang where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_jiangxi where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_lawtime where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_ningxia where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_qinghai where resume != "" 
union all
select pra_number,name,org_name,resume from hht_lawyer_shandong where resume != "" ;
===========
针对三字段处理：


delete from lawyers_resume where pra_number is null or pra_number = "" or CHAR_LENGTH(pra_number) < 8;
delete from lawyers_resume where name is null or name = "" or CHAR_LENGTH(name) < 2;
delete from lawyers_resume where org_name is null or org_name = "" or CHAR_LENGTH(org_name) < 5;


SELECT * from lawyers_resume where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

delete from lawyers_resume where pra_number like "%执业律师%";
update lawyers_resume set pra_number  = replace(pra_number," ","");
update lawyers_resume set pra_number  = replace(pra_number,"‘","");
update lawyers_resume set pra_number  = replace(pra_number,"'","");
update lawyers_resume set pra_number  = replace(pra_number,"	","");
update lawyers_resume set pra_number  = replace(pra_number,'"',"");
update lawyers_resume set pra_number  = replace(pra_number,'，',"");
update lawyers_resume set pra_number  = replace(pra_number,',',"");
update lawyers_resume set pra_number  = replace(pra_number,'？',"");

==========
SELECT * from lawyers_resume where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update lawyers_resume set name  = replace(name,' ',"");
update lawyers_resume set name  = replace(name,'	',"");

update lawyers_resume set org_name = replace(org_name,"（","(");
update lawyers_resume set org_name = replace(org_name,"）",")");
update lawyers_resume set org_name = replace(org_name,"服务所","事务所");

带中文（）不带()的正则来匹配
SELECT * from lawyers_resume where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update lawyers_resume set org_name  = replace(org_name,' ',"");
update lawyers_resume set org_name  = replace(org_name,'	',"");

update hht_lawyer_all_collect_match_result a join lawyers_resume b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 
set a.resume = b.resume ;

select years from hht_lawyer_all_collect_match_result where years = "" or years is null;
update hht_lawyer_all_collect_match_result set years = NULL where years = "" or years is null;

==================
根据年度审核，合并"曾执业律所":
有年度审核，且有效的数据，过滤后有：hht_lawyer_jiangsu_annualass,hht_lawyer_hunan_annualass
处理三字段：

delete from hht_lawyer_jiangsu_annualass where pra_number is null or pra_number = "" or CHAR_LENGTH(pra_number) < 8;
delete from hht_lawyer_jiangsu_annualass where name is null or name = "" or CHAR_LENGTH(name) < 2;
delete from hht_lawyer_jiangsu_annualass where org_name is null or org_name = "" or CHAR_LENGTH(org_name) < 5;

delete from hht_lawyer_hunan_annualass where pra_number is null or pra_number = "" or CHAR_LENGTH(pra_number) < 8;
delete from hht_lawyer_hunan_annualass where name is null or name = "" or CHAR_LENGTH(name) < 2;
delete from hht_lawyer_hunan_annualass where org_name is null or org_name = "" or CHAR_LENGTH(org_name) < 5;

SELECT * from hht_lawyer_jiangsu_annualass where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

SELECT * from hht_lawyer_hunan_annualass where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

=========
SELECT * from hht_lawyer_jiangsu_annualass where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

SELECT * from hht_lawyer_hunan_annualass where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_jiangsu_annualass set name  = replace(name,' ',"");
update hht_lawyer_jiangsu_annualass set name  = replace(name,'	',"");
update hht_lawyer_hunan_annualass set name  = replace(name,' ',"");
update hht_lawyer_hunan_annualass set name  = replace(name,'	',"");
delete from hht_lawyer_hunan_annualass where pra_number = "14301201010875767";
=========
update hht_lawyer_jiangsu_annualass set org_name = replace(org_name,"（","(");
update hht_lawyer_jiangsu_annualass set org_name = replace(org_name,"）",")");
update hht_lawyer_jiangsu_annualass set annualass = replace(annualass,"（","(");
update hht_lawyer_jiangsu_annualass set annualass = replace(annualass,"）",")");
update hht_lawyer_jiangsu_annualass set org_name = replace(org_name,"服务所","事务所");

update hht_lawyer_hunan_annualass set org_name = replace(org_name,"（","(");
update hht_lawyer_hunan_annualass set org_name = replace(org_name,"）",")");
update hht_lawyer_hunan_annualass set annualass = replace(annualass,"（","(");
update hht_lawyer_hunan_annualass set annualass = replace(annualass,"）",")");
update hht_lawyer_hunan_annualass set org_name = replace(org_name,"服务所","事务所");
=======
SELECT * from hht_lawyer_jiangsu_annualass where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

SELECT * from hht_lawyer_hunan_annualass where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


delete from hht_lawyer_jiangsu_annualass where org_names is null;
delete from hht_lawyer_hunan_annualass where org_names is null;

==================
新增执业律所合并到hht_lawyer_all_collect_match_result：
update hht_lawyer_all_collect_match_result a join lawyers_resume b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 
set a.resume = b.resume ;


select a.id,a.org_names,b.org_names from hht_lawyer_all_collect_match_result a join hht_lawyer_jiangsu_annualass b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name; 

合并hht_lawyer_jiangsu_annualass、hht_lawyer_hunan_annualass：
insert into hht_lawyer_jiangsu_annualass(pra_number,name,org_name,org_names) 
select pra_number,name,org_name,org_names from hht_lawyer_hunan_annualass;


select * from  hht_lawyer_all_collect_match_result where lawyer_id = "80951b3a-a290"
select * from  hht_lawyer_all_collect_match_result where pra_number = "14403201310092076"

select * from  hht_lawyer_all_collect_match_result where lawyer_id in (
"84754ced-ce73","0a948859-4654","1d6bd182-b0f2","5d38cb4a-6ad6"
) 

select * from  hht_lawyer_all_collect_match_result where lawyer_id in (
"f1f71130-1a6d","1e769630-b3a7","6f6b8414-f796","9b68aad1-ceaa","441d1b9c-af90","fb152bed-6498","fc229095-e0d3",
"df074ba3-463e","63127a2d-55ad","3557a2dd-089f","b6add0cc-ba8f","3557a2dd-089f","3557a2dd-089f","2ca40b55-c417")

select * from  hht_lawyer_all_collect_match_result where name = "付三元";
select * from  hht_lawyer_all_collect_match_result where name = "高亚兰";
select * from  hht_lawyer_all_collect_match_result where name = "史敦定";
select * from  hht_lawyer_all_collect_match_result where name = "龙雄彪";
select * from  hht_lawyer_all_collect_match_result where name = "付伟";
select * from  hht_lawyer_all_collect_match_result where name = "蒋海亮";
select * from  hht_lawyer_all_collect_match_result where name = "林杨";
select * from  hht_lawyer_all_collect_match_result where name = "李贞";
select * from  hht_lawyer_all_collect_match_result where name = "孙嘉宏";
select * from  hht_lawyer_all_collect_match_result where name = "梁兴来";
select * from  hht_lawyer_all_collect_match_result where name = "何小波";
select * from  hht_lawyer_all_collect_match_result where practicestatus = "注销";


============================================================
============================================================
============================================================
以律师姓名+ 执业证号前15位 进行去重合并，合并org_names、resume等字段；


统计处理org_names中的不规则律所，有：*律师||*、*律师、%律师事务、*律师事务||* 四种情况：

select *  from hht_lawyer_all_collect_match_result 
where org_names like "%律师||%";
无结果；

select *  from hht_lawyer_all_collect_match_result 
where org_names like "%律师" ;

update hht_lawyer_all_collect_match_result set 
org_name =replace(org_name,"河北陈丽萍律师事务所律师","河北陈丽萍律师事务所"),
org_names =replace(org_names,"河北陈丽萍律师事务所律师","河北陈丽萍律师事务所")
where org_name = "河北陈丽萍律师事务所律师" ;



select *  from hht_lawyer_all_collect_match_result 
where org_names like "%律师事务" or org_names like "%律师事务||%";

以上查询，每条只包含一个律所，且以"律师事务"结尾，可使用以下语句更新：
update hht_lawyer_all_collect_match_result set 
org_name =replace(org_name,"律师事务","律师事务所"),
org_names =replace(org_names,"律师事务","律师事务所")
where org_names like "%律师事务" or org_names like "%律师事务||%";

===============
#律师姓名一样，执业证号后两三位不一样，其中一个执业证号后面两三位都是0，律所在org_names中相互包含的：
select name,pra_number,org_name,org_names from  hht_lawyer_all_collect_match_result where pra_number like "%000";

select left(pra_number,15),count(*) from  hht_lawyer_all_collect_match_result where pra_number like "%00" 
 group by left(pra_number,15) having(count(*) > 1 ) ;

过滤出按pra_15,name分组后重复的数据，单独处理；
create table hht_lawyer_all_collect_match_result_duplicate_hebing as 
select a.* from hht_lawyer_all_collect_match_result a 
join (
select left(pra_number,15) as pra_15,name from  hht_lawyer_all_collect_match_result 
 group by pra_15,name having(count(*) > 1 )) b 
on left(a.pra_number,15) = b.pra_15 and a.name = b.name 
order by name ;


在原表中删除重复数据；
delete from hht_lawyer_all_collect_match_result where lawyer_id in (
select lawyer_id from hht_lawyer_all_collect_match_result_duplicate_hebing
)

重复数据处理后的结果再重新插入原始表中；
insert into hht_lawyer_all_collect_match_result select * from hht_lawyer_all_collect_match_result_duplicate_hebing_result;


-- 合并hht_lawyer_all_collect_match_result,hht_lawyer_jiangsu_annualass的org_names，并去重:
-- 使用程序处理；
-- ============================
-- 导入律师原始数据到ES中，方便定位问题；
-- 1）先导入hbase，使用表名+id作为rowkey；
-- 2）导入ES时，使用rowkey作为ES索引中的ID；
-- 3）索引：lawyers-origin，类型：hht_lawyer(新律协数据),12348gov（法网）,lawyer_info（旧律协）
-- hht_lawyer_anhui
-- hht_lawyer_bingtuan
-- hht_lawyer_bsgs
-- hht_lawyer_chongqing
-- hht_lawyer_gansu
-- hht_lawyer_gds_gdlawyer
-- hht_lawyer_guangxi
-- hht_lawyer_guizhou
-- hht_lawyer_hainan
-- hht_lawyer_hebei
-- hht_lawyer_heilongjiang
-- hht_lawyer_henan
-- hht_lawyer_hubei
-- hht_lawyer_hunan
-- hht_lawyer_jiangsu
-- hht_lawyer_jiangxi
-- hht_lawyer_lawtime
-- hht_lawyer_liaoning
-- hht_lawyer_ningxia
-- hht_lawyer_qinghai
-- hht_lawyer_shandong
-- hht_lawyer_shanxi
-- hht_lawyer_sichuan
-- hht_lawyer_tianjin
-- hht_lawyer_xinjiang
-- hht_lawyer_xizang
-- hht_lawyer_yunnan
-- hht_lawyer_zhejiang
-- lawyer_info
-- zy_lawyer_12348gov

