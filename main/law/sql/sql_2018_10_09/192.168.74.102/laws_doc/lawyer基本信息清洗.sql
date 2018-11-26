select a.name,a.org_name,count(a.name) from lawyer_info_new a GROUP BY 
name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time 
having(count(a.name)>1) 


create table lawyer_info3 as select name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time from lawyer_info2 GROUP BY 
name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time 

select a.name,a.org_name,count(a.name) from lawyer_info3 a GROUP BY 
name,org_name having(count(a.name)>1) 

delete from lawyer_info2 where name = "" or org_name = ""


select * from lawyer_info2 where name = "马静"
SELECT count(*) from lawyer_info2   #168033

select count(DISTINCT name,pra
_number,gender,nation,edu_origin,politics,org_name,org_identity,pra_type,pra_course,first_pra_time,qua_number,qua_time) from lawyer_info2

delete from lawyer_info_new where name = "" or org_name = ""

律师基本信息处理步骤：

1、处理律所，将省市县去掉，末尾统一为：律师事务所
		python lawyers_base_info.py
2、从lawyer_info_new中筛选出能与lawyers的lawyer,law_office匹配的。
create table lawyer_info2 as 
select b.* from lawyers a, lawyer_info_new b where a.lawyer = b.name and a.law_office = b.org_name;

3、筛选出分组后的数据（去掉分组字段重复的数据，分组字段重复，就保留一个即可）
create table lawyer_info3 as select name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time from lawyer_info2 GROUP BY 
name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time 

注意：这时要给表lawyer_info3加上个id字段。便于后面处理。

4、统计name,org_name重复的数据
select a.name,a.org_name,count(a.name) from lawyer_info3 a GROUP BY 
name,org_name having(count(a.name)>1)

5、从lawyer_info3中找出name，org_name重复的完整数据
create table lawyer_info4 as 
select a.* from lawyer_info3 a,(select name,org_name from lawyer_info3 GROUP BY 
name,org_name having(count(name)>1) ) b where a.name = b.name and a.org_name = b.org_name 

6、从lawyer_info3中删除name，org_name重复的数据,这些重复的数据将在lawyer_info4中单独清洗，之后合并到lawyer_info3中；
delete from lawyer_info3 where id in (select id from lawyer_info4)

7、从lawyer_info4中，保留name，org_name，pra_number（重复）一样的数据，即删除name，org_name一样，
pra_number不一样的数据（pra_number不一样不知道要哪个，总之lawyers的lawyer,law_office是唯一的）；
将保留的数据按照name，org_name，pra_number一样时互补其它字段，合并为一条数据。
create table lawyer_info5 as 
select a.* from lawyer_info4 a,
(select name,org_name,pra_number from lawyer_info4 GROUP BY name,org_name,pra_number having(count(name)>1) ) b 
where a.name = b.name 
and a.org_name = b.org_name 
and a.pra_number = b.pra_number

8、使用spark，lawyer_base_info2.py读取lawyer_info5表，合并互补name，org_name，pra_number三个字段一样时的其他字段数据为一条，输出lawyer_info6表

9、使用lawyer_info6插入lawyer_info3数据，此时，lawyer_info3表中name,org_name唯一
INSERT into lawyer_info3(name, pra_number, gender, nation, edu_origin, politics, org_name, 
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time) 
SELECT name, pra_number, gender, nation, edu_origin, politics, org_name, 
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time from lawyer_info6

select * from lawyer_info3 where name = "张圣莹" and org_name = "湖北维思德律师事务所"
select * from lawyer_info5 where name = "郭忆惠" and org_name = "湖北维思德律师事务所"
select * from lawyers where lawyer = "刘玉姿" and law_office = "福建夏理律师事务所"

pra_number, gender, nation, edu_origin, politics
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time

update lawyers a,lawyer_info3 b set 
a.pra_number = b.pra_number,
a.gender = b.gender,
a.nation = b.nation,
a.edu_origin = b.edu_origin,
a.politics = b.politics,
a.org_identity = b.org_identity,
a.pra_type = b.pra_type,
a.pra_course = b.pra_course,
a.first_pra_time = b.first_pra_time,
a.qua_number = b.qua_number,
a.qua_time = b.qua_time where a.lawyer = b.name and a.law_office = b.org_name;

填充职业编号：
update lawyers set char_no = pra_number where char_no is null or char_no = "";

14401201511763364
select substr(char_no,6,4) from lawyers where id =72

填充首次执业时间：
update lawyers set first_pra_time = substr(char_no,6,4) 
where char_no is not null 
and char_no != "" and LENGTH(char_no)=17 
and (first_pra_time is null or first_pra_time = "");

select count(*) from lawyers where pra_course is not NULL


create table lawyer_info2 as 
select count(*) from lawyers a, lawyer_info_new b where not (a.lawyer = b.name and a.law_office = b.org_name);

select count(*) from lawyer_info_new
select count(*) from lawyer_info_add

===================================================================
===================================================================================
爬虫爬取的新律师（判决书中没有）信息处理：

求差集，左连接比not in 效率高。
1、求出lawyer_info_new表中与lawyers中lawyer,law_office不匹配的数据
create table lawyer_info_add 
select t1.* FROM lawyer_info_new as t1 LEFT JOIN 
(select b.name,b.org_name from lawyers a, lawyer_info_new b where a.lawyer = b.name and a.law_office = b.org_name) as t2 
ON t1.name=t2.name and t1.org_name = t2.org_name where t2.name is null
2、从律师基本信息清洗的第3步骤开始：
create table lawyer_info_add01 as select name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time from lawyer_info_add GROUP BY 
name,pra_number,gender,nation,edu_origin,politics,org_name,org_identity,
pra_type,pra_course,first_pra_time,qua_number,qua_time

注意：这时要给表lawyer_info_add01加上个id字段。便于后面处理。

3、统计name,org_name重复的数据
select a.name,a.org_name,count(a.name) from lawyer_info_add01 a GROUP BY 
name,org_name having(count(a.name)>1)

4、从lawyer_info_add01中找出name，org_name重复的完整数据
create table lawyer_info_add02 as 
select a.* from lawyer_info_add01 a,(select name,org_name from lawyer_info_add01 GROUP BY 
name,org_name having(count(name)>1) ) b where a.name = b.name and a.org_name = b.org_name 

5、从lawyer_info_add01中删除name，org_name重复的数据；
delete from lawyer_info_add01 where id in (select id from lawyer_info_add02)


7、从name，org_name重复的完整数据中，保留name，org_name，pra_number（重复）一样的数据，认为是同一律师的数据,可以进行合并，
即删除name，org_name一样，pra_number不一样的数据（pra_number不一样无法合并，虽然name，org_name一样，但是不知道取哪一条）。
create table lawyer_info_add03 as 
select a.* from lawyer_info_add02 a,(select name,org_name,pra_number from lawyer_info_add02 GROUP BY 
name,org_name,pra_number having(count(name)>1) ) b where a.name = b.name and a.org_name = b.org_name and a.pra_number = b.pra_number

8、使用spark，lawyer_info_add03.py读取lawyer_info_add03表，合并name，org_name，pra_number三个字段一样的数据，输出lawyer_info_add04表

9、使用lawyer_info_add04插入lawyer_info_add01数据，此时，lawyer_info_add01表中name,org_name唯一
INSERT into lawyer_info_add01(name, pra_number, gender, nation, edu_origin, politics, org_name, 
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time) 
SELECT name, pra_number, gender, nation, edu_origin, politics, org_name, 
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time from lawyer_info_add04

10、新增lawyer_info_add01表数据到lawyers
INSERT into lawyers_new(lawyer, char_no, gender, nation, edu_origin, politics, law_office, 
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time) 
SELECT name, pra_number, gender, nation, edu_origin, politics, org_name, 
org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time from lawyer_info_add01

合并职业历程步骤：

1、lawyers_new新增old_id，保存之前的lawyer_id。
update lawyers_new set old_id  = id

2、清洗出lawyer对应的law_office,pra_course中所有的律所，输出个新的字段lawyer_key；
展开为多条数据，律师名称一样，律所不一样，并且一个律师的多条数据对应的lawyer_key一样。
结果字段：lawyer,law_office,lawyer_key,存入lawyers__lawyer_course表。

python lawyers_base_info_pra_course.py  
-- select lawyer,law_office,pra_course from lawyers_new where pra_course like "%转所%"  is not null and pra_course != "" 

3、增加一个lawyer_key字段到lawyers_new中，根据lawyer，law_office一样，然后更新lawyers__lawyer_course表中的lawyer_key到lawyers_new。

update lawyers_new a,lawyers__lawyer_course b set a.lawyer_key = b.lawyer_key where a.lawyer=b.lawyer and a.law_office=b.law_office;


4、lawyers_new中具有相同lawyer_key的数据，放到lawyers_new_del，单独处理，之后合并到lawyers_new中。
create table lawyers_new_del as 
select a.* from lawyers_new a,(select lawyer_key from lawyers_new where lawyer_key is not null GROUP BY 
lawyer_key HAVING(count(*)>1)) b where a.lawyer_key = b.lawyer_key order by a.lawyer


5、删除lawyers_new中具有相同lawyer_key的数据。
delete a.* from lawyers_new a,(select lawyer_key from lawyers_new where lawyer_key is not null GROUP BY 
lawyer_key HAVING(count(*)>1)) b where a.lawyer_key = b.lawyer_key 

-- select lawyer_key from lawyers_new where lawyer_key is not null GROUP BY lawyer_key HAVING(count(*)>1)   #3253

6、读取lawyers_new_del表，使用spark,lawyers_new_key_union.py合并具有相同lawyer_key的数据，输出lawyers_new_del01表。

7、合并lawyers_new_del01数据到lawyers_new表
INSERT into lawyers_new(lawyer,law_office,char_no,gender,nation,edu_origin,politics,org_identity,pra_type, 
pra_course,first_pra_time,qua_number,qua_time,old_id) 
SELECT lawyer,law_office,char_no,gender,nation,edu_origin,politics,org_identity,pra_type, 
  pra_course,first_pra_time,qua_number,qua_time,old_id from lawyers_new_del01

