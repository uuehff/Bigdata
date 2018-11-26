create table hht_lawyer_12348gov_v2 as 
select * from hht_lawyer_12348gov where pra_number is not null and pra_number != "";

select * from hht_lawyer_12348gov_v2 where name like "%马方平%";

select SUBSTR(pra_number,1,1),SUBSTR(pra_number,6,4),SUBSTR(pra_number,10,1),SUBSTR(pra_number,11,1)pra_number 
from hht_lawyer_12348gov_v2 
where CHAR_LENGTH(pra_number) = 17 
and SUBSTR(pra_number,1,1) = "1" 
and SUBSTR(pra_number,6,4) > "1970" and SUBSTR(pra_number,6,4) < "2019" 
and SUBSTR(pra_number,10,1) >= "1" and SUBSTR(pra_number,10,1) <= "9" 
and SUBSTR(pra_number,11,1) in ("0","1") and id < 10000;

select SUBSTR(pra_number,1,1),SUBSTR(pra_number,6,4),SUBSTR(pra_number,10,1),SUBSTR(pra_number,11,1)pra_number 
from hht_lawyer_12348gov_v2 where id < 10000;

select * from hht_lawyer_12348gov_v2 
where not (CHAR_LENGTH(pra_number) = 17 
and SUBSTR(pra_number,1,1) = "1" 
and SUBSTR(pra_number,6,4) > "1970" and SUBSTR(pra_number,6,4) < "2019" 
and SUBSTR(pra_number,10,1) >= "1" and SUBSTR(pra_number,10,1) <= "9" 
and SUBSTR(pra_number,11,1) in ("0","1"));

create table hht_lawyer_12348gov_v3 as 
select * from hht_lawyer_12348gov_v2 
where CHAR_LENGTH(pra_number) = 17 
and SUBSTR(pra_number,1,1) = "1" 
and SUBSTR(pra_number,11,1) in ("0","1");

select * from hht_lawyer_12348gov_v3 where pra_number in (
select pra_number from hht_lawyer_12348gov_v3 
group by pra_number having(count(*) > 1)) order by pra_number;



11101009710853440 执业证号为17位，但是6-9位不是年份；且在全国律师执业证查询平台

========================================================
create table lawyer_info_new_v2 as 
select * from lawyer_info_new where pra_number is not null and pra_number != "";

select * from lawyer_info_new_v2 where CHAR_LENGTH(pra_number) != 17 and SUBSTR(pra_number,1,1) = "1";
select * from lawyer_info_new_v2 where pra_number like "135052013106003%";
select * from lawyer_info_new_v2 where name like "%进辉%";
select * from lawyer_info_new_v2 where name like "%马方平%";
select * from lawyer_info_new_v2 where name like "%王一";


select name,area from lawyer_info_new_v2 where 
CHAR_LENGTH(pra_number) != 17 and SUBSTR(pra_number,1,1) = "1" 
group by name,area having(count(*) > 1);



create table lawyer_info_new_v3 as 
select * from lawyer_info_new_v2 
where CHAR_LENGTH(pra_number) = 17 
and SUBSTR(pra_number,1,1) = "1" 
and SUBSTR(pra_number,11,1) in ("0","1");


select * from lawyer_info_new_v3 where pra_number in (
select pra_number from lawyer_info_new_v3 
group by pra_number having(count(*) > 1)) order by pra_number;


select count(*) from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number ;  
#217402


select name,pra_number from lawyer_info_new_v3 where pra_number in (
(
select pra_number from lawyer_info_new_v3 
group by pra_number having(count(*) > 1)) 
) group by pra_number,name having(count(*) < 2) order by pra_number
;

create table pra_number_gov_join as 
select a.* from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number ;  


create table pra_number_gov_join_out as 
select a.* from hht_lawyer_12348gov_v3 a left join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number where b.pra_number is null; 

select a.name,b.name from hht_lawyer_12348gov_v3 a join test_zy_lawyer b 
on a.pra_number = b.pra_number and a.name != b.name order by a.name; 

select a.name,b.name from hht_lawyer_12348gov_v3 a join test_zy_lawyer b 
on a.pra_number = b.pra_number and replace(a.name," ","") != replace(b.name," ","") order by a.name;  

select * from hht_lawyer_12348gov_v3 a join test_zy_lawyer b 
on a.pra_number = b.pra_number and replace(a.name," ","") != replace(b.name," ","") order by a.name;  


于新峰	晁晓朋 这二人名字和执业证号在法网上有相互调换，且法网上"晁晓朋"为"晁晓鹏"：11301200910613382 、11301201410757999
与博信律师、律所真伪平台中名字、执业证号刚好相反；
有天眼查案件：https://zhongshan.tianyancha.com/lawsuit/bf37f1ed3fbe489a9c448eb569392de5

中发现委托代理人"晁晓朋"，且从二人的执业证号的获取时间（可以看出年龄大小）、及法网上二人的头像（头像正确、人名正确，就是执业证号调换了）可以看出，博信律师真伪平台是正确的；
律师真伪平台中可以输入身份证、律师执业证查询，因此有身份证这一选项，更加确认他的正确性。

处理流程: 通过执业证号、律师姓名个字段去确定哪个数据更准确，也可以使用律所字段辅佐去判断：
1、gov、lawyer_info表先过滤：17位，第一位是1，第十一位是0或1；

2、辨别执业证号、姓名真伪：执业证号、姓名是固定的；

关联数据：hht_lawyer_12348gov_v3 和 zy_lawyer
select a.pra_number,a.name,a.org_name,b.name,b.org_name from hht_lawyer_12348gov_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and (replace(a.name," ","") != replace(b.name," ","") or a.org_name != b.org_name) order by a.name;  


select a.pra_number,a.name,a.org_name,b.name,b.org_name from lawyer_info_new_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and (replace(a.name," ","") != replace(b.name," ","") or a.org_name != b.org_name) order by a.name;  


3、当gov和真伪平台中的执业证号一样，律所或律师名字不一样时：
 1.将gov律所 + 空格 + gov律师,在我们平台中搜索案例，看是否有结果、及查看文书中的律师姓名
 2.将真伪平台律所 + 空格 + 真伪平台律师,在我们平台中搜索案例，看是否有结果、及查看文书中的律师姓名

 经统计排查发现：真伪律师平台数据准确！

4、律师流动、执业类型变化，会造成执业证号的变化：说明：http://www.66law.cn/laws/86844.aspx
执业证号2-5位是执业机构所在行政区域，市内、市外、省外转所都会修改这2位或4位，其他不变。

因此，执业行政区域，以2-5为为准即可。

5、

46679	http://www.12348.gov.cn/imagetype/1100/lsfw/lsuser/47927/jpg	130105	11301201410757999	114.451996	4792713	河北陆港律师事务所	38.076585	于新峰	晁晓朋	河北陆港律师事务所	10	{u"value": u""}	37318	11301201410757999	11301201410757999	男	专职律师	正常执业	A20114110250301	河北省司法厅	1	1

平台法规搜索：司法部律师司关于进一步规范律师事务所名称、律师名片的通知


select a.name,b.name from lawyer_info_new_v3 a join test_zy_lawyer b 
on a.pra_number = b.pra_number and a.name != b.name order by a.name;  

select * from lawyer_info_new_v3 where name = "巴信萍"
12102201421108856
12113199911660646
12111200911526834
12101198511706724
12107200110413721
select * from test_zy_lawyer where name = "白云艳"
12113199911660646
select * from hht_lawyer_12348gov_v3 where name = "白云艳"
12113199911660646


select * from lawyer_info_new_v3 where pra_number = "11504201511607305"
select * from hht_lawyer_12348gov_v3 where pra_number = "11301200910613382"
select * from test_zy_lawyer where pra_number = "11301200910613382"

select * from lawyer_info_new_v3 where CHAR_LENGTH(pra_number) != 17


46679	http://www.12348.gov.cn/imagetype/1100/lsfw/lsuser/47927/jpg	130105	11301201410757999	114.451996	4792713	河北陆港律师事务所	38.076585	于新峰	10	{u"value": u""}	37318	晁晓朋	11301201410757999	11301201410757999	男	河北陆港律师事务所	专职律师	正常执业	A20114110250301	河北省司法厅	1	1

行政区域划分：《中华人民共和国行政区划代码》由中华人民共和国国家统计局发布。该标准对我国县以上行政区划的代码做了规定，
用六位阿拉伯数字分层次代表我国的
省（自治区、直辖市）、
地区（市、州、盟）、县（区、市、旗）的名称。

area_code_v2 表中ID为行政编码；与律师执业证号中的2-5位，
对应匹配，可得到律师的执业区域；（4位只匹配到市）

create table area_code_v2 as select * from area_code where right(ID,2) = "00";

create table area_code_v3 as 
select left(ID,4),Name,province from area_code_v2 where right(ID,4) != "0000";

update area_code_v2 a join area_code_v2 b on a.ParentID = b.ID set a.province = b.Name ; 

select count(distinct left(ID,4) ) from area_code_v2 ;


delete from zy_lawyer where pra_no is null;
delete from test_zy_lawyer where name is null;

select a.pra_number,a.name,a.org_name,b.name,b.org_name from hht_lawyer_12348gov_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and (replace(a.name," ","") != replace(b.name," ","") or a.org_name != b.org_name) order by a.name;  

select a.pra_number,a.name,a.org_name,b.name,b.org_name from hht_lawyer_12348gov_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and replace(a.name," ","") != replace(replace(b.name," ",""),"　","") order by a.name;  

create table gov_v3_join_zy_lawyer as 
select a.pra_number,a.name as a_name,a.org_name as a_org_name,b.name as b_name,b.org_name as b_org_name from hht_lawyer_12348gov_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and replace(a.name," ","") != replace(replace(b.name," ",""),"　","") order by a.name;  

select a.*,b.name,b.org_name from gov_v3_join_zy_lawyer a join lawyer_info_new_v3 b on a.pra_number = b.pra_number;

13101198911865675	孙红	上海市世通律师事务所	孙虹	上海市世通律师事务所	孙红	上海世通律师事务所
百度搜索含有：上海市世通律师事务所 孙虹： 的文书http://www.51djl.com/document/0/266/3329/2e6f226a-e4e2-45a7-9ed7-5cba3c0b7b23.html

select a.*,b.name,b.org_name from gov_v3_join_zy_lawyer a join lawyer_info_new_v3 b on a.pra_number = b.pra_number;

select a.name,a.org_name,b.name,b.org_name,c.name,c.org_name from hht_lawyer_12348gov_v3 a 
join lawyer_info_new_v3 b on a.pra_number = b.pra_number 
join zy_lawyer c on b.pra_number = c.pra_number and a.name = b.name;


select a.name,a.org_name from hht_lawyer_12348gov_v3 a 
join lawyer_info_new_v3 b on a.pra_number = b.pra_number 
join zy_lawyer c on b.pra_number = c.pra_number and a.name = b.name ;

update zy_lawyer set 
name = replace(replace(name," ",""),"　",""),
org_name = replace(replace(org_name," ",""),"　","");

update zy_lawyer set org_name = replace(org_name,",","")  where CHAR_LENGTH(org_name) < 9;


update zy_lawyer set qua_number = "" where left(qua_number,1) not in ("A","B","C") 
or CHAR_LENGTH(qua_number) != 15;

delete from zy_lawyer where 
CHAR_LENGTH(name) < 2 
or name is null 
or name = "" 
or org_name  = "null" 
or org_name = ",政法";


select a.pra_number,a.name,a.org_name,b.pra_number,b.name,b.org_name,c.pra_number,c.name,c.org_name 
from hht_lawyer_12348gov_v3 a 
join lawyer_info_new_v3 b on a.pra_number = b.pra_number 
join zy_lawyer c on b.pra_number = c.pra_number 
and a.name = b.name 
and b.name = c.name 
and a.org_name != b.org_name;

create table z_lawyers as 
select a.pra_number,a.name,a.org_name 
from hht_lawyer_12348gov_v3 a 
join lawyer_info_new_v3 b on a.pra_number = b.pra_number 
join zy_lawyer c on b.pra_number = c.pra_number ;

select a.pra_number,a.name,a.org_name,b.pra_number,b.name,b.org_name,c.pra_number,c.name,c.org_name 
from hht_lawyer_12348gov_v3 a 
join lawyer_info_new_v3 b on a.pra_number = b.pra_number 
join zy_lawyer c on b.pra_number = c.pra_number 
and (a.name != c.name ) ;


update hht_lawyer_12348gov_v3 set name = replace(replace(name," ","")," ","")
A开头的可能是法律职业资格证号，但法律职业资格证A后面应该有14位数字。比如：A20164401000001，A是证书类型，2016是参考年份，44是省代码，01是市代码。

select name  from hht_lawyer_12348gov_v4 group by name 

select name from hht_lawyer_12348gov_v4 where name REGEXP '[a-z1-9A-Z?:;,]'
select org_name from hht_lawyer_12348gov_v4 where org_name REGEXP '[a-z1-9A-Z?:;,]'

update hht_lawyer_12348gov_v4 set org_name = "新疆纪全律师事务所" where org_name = "新疆纪全律师事务所lssws"

delete from  hht_lawyer_12348gov_v4 where name REGEXP '[a-z1-9A-Z?:;,]' 

-- select name from hht_lawyer_12348gov_v3 where name like "%？；。，%"
-- select name from hht_lawyer_12348gov_v3 where org_name like "%？；。，%"
select org_name from hht_lawyer_12348gov_v3 where org_name like "新疆纪全律师事务所lssws%"






create table lawyer_info_5w as 
select a.* from lawyer_info_new_v3 a left join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number where b.pra_number is null;



create table lawyer_tmp as 
select * from lawyer_info_new_v3 where pra_number in (
select pra_number from lawyer_info_new_v3 
group by pra_number having(count(*) > 1)
)

update lawyer_duplicate a join area_code_v3 b on substr(pra_number,2,4) = b.area_id 
set a.city_add = replace(b.city,"市",""),
a.province_add = replace(b.province,"省","");

update lawyer_duplicate set province_add = replace(province_add,"市","");

delete from lawyer_duplicate where area != province_add;

delete a from lawyer_info_new_v3 a join aaa b on 
a.pra_number = b.pra_number;


select * from lawyer_duplicate where pra_number in (
select pra_number from lawyer_duplicate
group by pra_number having(count(*) > 1)
)  order by pra_number;


select * from lawyer_info_new_v3 where pra_number in (
(
select pra_number from lawyer_info_new_v3 
group by pra_number having(count(*) > 1)) 
) order by pra_number;

select name from lawyer_info_new_v3 where name REGEXP '[a-z1-9A-Z?:;,]' ;
select org_name from lawyer_info_new_v3 where org_name REGEXP '[a-zA-Z?:;,]' ;
select name from lawyer_info_new_v3 where name like "%？；。，%";
select name from lawyer_info_new_v3 where org_name like "%？；。，%";
delete from  lawyer_info_new_v3 where name REGEXP '[a-z1-9A-Z?:;,]' ;

select org_name from lawyer_info_new_v3 where org_name REGEXP '[a-zA-Z?:;,]' ;


update lawyer_duplicate set 
qua_number = "",
qua_time = ""
 where left(qua_number,1) not in ("A","B","C") 
or CHAR_LENGTH(qua_number) != 15;

select * from lawyer_duplicate  where  
 CHAR_LENGTH(name) < 2 or CHAR_LENGTH(name) > 3 ;
update lawyer_duplicate set name = "叶培芬" where name = "+叶培芬"
update lawyer_duplicate set name = "郑家红" where name = "郑家红律师"
update lawyer_duplicate set name = "佘昌浩" where name = "佘昌浩　"

select * from lawyer_info_new_v3  where  
 CHAR_LENGTH(name) < 2 or CHAR_LENGTH(name) > 3 ;

update lawyer_info_new_v3 set name = replace(name,"。",".")
update lawyer_info_new_v3 set name = replace(name," ","")
update lawyer_info_new_v3 set name = replace(name,"：","")
update lawyer_info_new_v3 set name = replace(name,"+","")
update lawyer_info_new_v3 set name = replace(name,"()","")
update lawyer_info_new_v3 set name = replace(name," ","")
update lawyer_info_new_v3 set name = replace(name," ","")



delete from lawyer_info_new_v3  where  name like "%？%";
delete from lawyer_info_new_v3  where  CHAR_LENGTH(name) < 2;
delete from lawyer_info_new_v3  where  pra_number = "" or name = "" or org_name = "";
delete from lawyer_duplicate  where  pra_number = "" or name = "" or org_name = "";
update lawyer_info_new_v3 set 
qua_number = "",
qua_time = ""
 where left(qua_number,1) not in ("A","B","C") 
or CHAR_LENGTH(qua_number) != 15;

update lawyer_duplicate set name = replace(name,"。",".")
update lawyer_duplicate set name = replace(name,"+","")

insert into lawyer_info_new_v3(name,pra_number,nation,edu_origin,politics,org_name,org_identity,birth_date,first_pra_time,qua_number,qua_time
) 
select name,pra_number,nation,edu_origin,politics,org_name,org_identity,birth_date,first_pra_time,qua_number,qua_time 
from lawyer_duplicate_v2;



delete from hht_lawyer_12348gov_v3  where  pra_number = "" or name = "" or org_name = "";
update zy_lawyer set 
qua_number = "" where left(qua_number,1) not in ("A","B","C") 
or CHAR_LENGTH(qua_number) != 15;


select * from lawyer_info_new_v3 where pra_number = "11101202010412436"
select * from hht_lawyer_12348gov_v3 where pra_number = "13704201180820410"
select * from zy_lawyer where pra_number = "张兴"

update hht_lawyer_12348gov_v3 set org_name = "新疆纪全律师事务所" where org_name = "新疆纪全律师事务所lssws"



select pra_number,birth_date,first_pra_time,SUBSTR(pra_number,6,4) - SUBSTR(birth_date,1,4) from lawyer_info_new_v3 
where SUBSTR(pra_number,6,4) - SUBSTR(birth_date,1,4) < 20 order by SUBSTR(pra_number,6,4) - SUBSTR(birth_date,1,4);

update lawyer_info_new_v3 set birth_date = "" where CHAR_LENGTH(birth_date) < 10 

select DISTINCT pra_number from lawyer_duplicate 
出生日期、执业证号等等都需要用正则过一遍，再用逻辑过一遍；


select * from lawyer_info_new_v3 where pra_course is not null and pra_course != "";

更新hht_lawyer_12348gov_v3：

select count(*) from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b
on a.pra_number = b.pra_number and a.name = b.name;


select count(*) from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name;




select * from lawyer_info_new_v3 a left join hht_lawyer_12348gov_v3 b 
on a.pra_number = b.pra_number where b.pra_number is null;

update lawyer_info_new_v3 set flag = "1" 

insert into hht_lawyer_12348gov_v3(pra_number,name,org_name,nation,edu_origin,politics,org_identity,birth_date,pra_type,pra_course,first_pra_time,qua_number,qua_time,flag) 
select a.pra_number,a.name,a.org_name,a.nation,a.edu_origin,a.politics,a.org_identity,a.birth_date,a.pra_type,a.pra_course,a.first_pra_time,a.qua_number,a.qua_time,a.flag 
from lawyer_info_new_v3 a left join hht_lawyer_12348gov_v3 b 
on a.pra_number = b.pra_number where b.pra_number is null;

pra_number,name,org_name,gender,province,city,nation,
edu_origin,politics,org_identity,birth_date,pra_type,pra_course,
first_pra_time,qua_number,qua_time,years,flag

select * from lawyer_info_new_v3 where pra_number like "%1210720082197895%"
select * from hht_lawyer_12348gov_v3 where pra_number = "13704201180820410"
select * from zy_lawyer where pra_number like  "%1210720082197895%"

13101200-11124168	罗冰	广东安华理达上海分所律师事务所	女	上海市	上海市	汉族	硕士	共青团员	律师		专职律师		2009-11-19	A20051101082169	2006-02-01		1
select * from zy_lawyer a left join hht_lawyer_12348gov_v3 b on a.pra_number = b.pra_number 
where b.pra_number is null;


update hht_lawyer_12348gov_v3 a join hht_lawyer_12348gov_v2 b on 
a.pra_number = b.pra_number set a.years = b.years;


pra_number:
select * from hht_lawyer_12348gov_v3 where left(pra_number,1) != "1" or 
SUBSTR(pra_number,6,4) > 2018 or SUBSTR(pra_number,6,4) < 1970 or 
SUBSTR(pra_number,11,1) not in ("0","1");
结果：274条，经过百度文书，或者三个表查看，都有对应的数据，所以也认为是OK的。
其中所有数据第一位和性别位数据都是正确的。
delete from hht_lawyer_12348gov_v3 where pra_number = "13101200-11124168"
delete from hht_lawyer_12348gov_v3 where pra_number like "%B%"
delete from hht_lawyer_12348gov_v3 where pra_number like "% %"

name :
select * from hht_lawyer_12348gov_v3 where name like "%\n%"
update hht_lawyer_12348gov_v3 set name = replace(name,"\n","")


org_name:
update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"\n","")
update hht_lawyer_12348gov_v3 set org_name = replace(org_name," ","")
update hht_lawyer_12348gov_v3 set org_name = "福建名仕（南平）律师事务所" where org_name = "福建名仕（南平）？律师事务所"

pra_type,gender,province,city：
pra_type：依据执业证号第10位处理：
专职为1，兼职律师为2，香港为3，澳门为4，台湾为5，公职律师为6，公司律师为7，法律援助为8，军队律师为9。
gender：依据执业证号第11位处理，男为0，女为1；

update hht_lawyer_12348gov_v3
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
else gender end;

-- select 
-- SUBSTR(pra_number,10,2) as a,
-- case
-- when SUBSTR(pra_number,10,1) = "1" then "专职律师"
-- when SUBSTR(pra_number,10,1) = "2" then "兼职律师"
-- when SUBSTR(pra_number,10,1) = "3" then "香港律师"
-- when SUBSTR(pra_number,10,1) = "4" then "澳门律师"
-- when SUBSTR(pra_number,10,1) = "5" then "台湾律师"
-- when SUBSTR(pra_number,10,1) = "6" then "公职律师"
-- when SUBSTR(pra_number,10,1) = "7" then "公司律师"
-- when SUBSTR(pra_number,10,1) = "8" then "法律援助律师"
-- when SUBSTR(pra_number,10,1) = "9" then "军队律师"
-- else '' end as b,
-- 
-- case SUBSTR(pra_number,11,1)
-- when "0" then "男"
-- when "1" then "女"
-- else "" end as c 
-- from  hht_lawyer_12348gov_v3 limit 100;

-- select pra_number,name,
-- case SUBSTR(pra_number,11,1)
-- when "0" then "男"
-- else name end as c 
-- from  hht_lawyer_12348gov_v3 limit 100;


province,city：依据执业证号第2-5位关联area_code_v3处理；

update hht_lawyer_12348gov_v3 a join area_code_v3 b 
on SUBSTR(a.pra_number,2,4) = b.area_id set 
a.province = b.province,
a.city = b.city;

-- select * from hht_lawyer_12348gov_v3 where province is null;

select * from hht_lawyer_12348gov_v3 a 
left join area_code_v3 b 
on SUBSTR(a.pra_number,2,4) = b.area_id 
join area_code_v3 c on SUBSTR(a.pra_number,2,2) = SUBSTR(c.area_id,1,2)
where b.area_id is null;

update hht_lawyer_12348gov_v3 a join 
area_code_v3 b 
on SUBSTR(a.pra_number,2,2) = SUBSTR(b.area_id,1,2) 
set a.province = b.province where a.pra_number in (select pra_number from ttt);


years：执业年限，根据执业证号：
1、在这个范围之外的，以原始数据为准，为0的话赋值为空：SUBSTR(pra_number,6,4) > 2018 or SUBSTR(pra_number,6,4) < 1970
select * from hht_lawyer_12348gov_v3 where 
SUBSTR(pra_number,6,4) > 2018 or SUBSTR(pra_number,6,4) < 1970 order by years desc;

update hht_lawyer_12348gov_v3 set years = "" where years = "0" or years is null;


select years from hht_lawyer_12348gov_v3 where CHAR_LENGTH(years) > 2 or left(years,1) = "-"
update hht_lawyer_12348gov_v3 set years = "" where CHAR_LENGTH(years) > 2 or left(years,1) = "-"

select years from hht_lawyer_12348gov_v3 where CHAR_LENGTH(years) > 1 and years > 30 order by years desc

2、在SUBSTR(pra_number,6,4) <= 2018 and SUBSTR(pra_number,6,4) >= 1970
这个范围之内的，years=2018-SUBSTR(pra_number,6,4)+1。
select years from hht_lawyer_12348gov_v3 order by  years desc

select pra_number,name,org_name,SUBSTR(pra_number,6,4),2018-SUBSTR(pra_number,6,4)+1 as y ,
years from hht_lawyer_12348gov_v3 
where SUBSTR(pra_number,6,4) <= 2018 and SUBSTR(pra_number,6,4) >= 1970 
order by y desc

update hht_lawyer_12348gov_v3 
set years = 2018-SUBSTR(pra_number,6,4)+1
where 
SUBSTR(pra_number,6,4) <= 2018 and SUBSTR(pra_number,6,4) >= 1970 ;


nation,edu_origin,politics,birth_date,first_pra_time,qua_number,qua_time:
按执业证号、姓名一样关联，用lawyer_info_new_v3来更新：

update hht_lawyer_12348gov_v3 set qua_number = "A20124401141912" where pra_number = "14401201410064673"
update hht_lawyer_12348gov_v3 set qua_number = "" where pra_number = "13301199610352614"

update hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number and a.name = b.name 
set a.nation = b.nation,
a.edu_origin = b.edu_origin,
a.politics = b.politics,
a.birth_date = b.birth_date,
a.first_pra_time = b.first_pra_time,
a.qua_number = b.qua_number,
a.qua_time = b.qua_time;

update hht_lawyer_12348gov_v3 set 
qua_number = replace(qua_number,"a","A"),
qua_number = replace(qua_number,"b","B"),
qua_number = replace(qua_number,"c","C");

qua_number: A20103502060629 ,qua_time: 2011-03-01
birth_date,first_pra_time,qua_time
select first_pra_time from hht_lawyer_12348gov_v3 where CHAR_LENGTH(first_pra_time)> 10
update hht_lawyer_12348gov_v3 set first_pra_time = "2016-10-27" where first_pra_time = "2016-10-27上海"
delete from  hht_lawyer_12348gov_v3 where first_pra_time = replace(birth_date," ","")

select first_pra_time from hht_lawyer_12348gov_v3 where CHAR_LENGTH(first_pra_time)<4 and first_pra_time is not null and first_pra_time != ""
select birth_date from hht_lawyer_12348gov_v3 where CHAR_LENGTH(birth_date)<4 and birth_date is not null and birth_date != ""
select qua_time from hht_lawyer_12348gov_v3 where CHAR_LENGTH(qua_time) < 4 and qua_time is not null and qua_time != ""
select qua_time from hht_lawyer_12348gov_v3 where qua_time like "%年%"
update hht_lawyer_12348gov_v3 set qua_time = "2016-03" where qua_time = "2016年3月"

select * from hht_lawyer_12348gov_v3 
where (qua_number is null or qua_number = "") and 
(qua_time is not null or  qua_time != "")

select a.pra_number,a.name,a.qua_number,b.name,b.qua_number from hht_lawyer_12348gov_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and a.name = b.name 
where (a.qua_number is null or a.qua_number = "") and b.qua_number is not null and b.qua_number != ""


update hht_lawyer_12348gov_v3 a join zy_lawyer b 
on a.pra_number = b.pra_number and a.name = b.name 
set a.qua_number = b.qua_number 
where (a.qua_number is null or a.qua_number = "") and b.qua_number is not null and b.qua_number != ""

select * from hht_lawyer_12348gov_v3 a 
where (a.qua_number is null or a.qua_number = "") and a.qua_time is not null and a.qua_time != ""
为空；

pra_number,qua_number,birth_date,first_pra_time,qua_time
处理规则：
1、在范围之外的，资格证时间+8 < 2018,数据较少肉眼观察都合适。
select * from hht_lawyer_12348gov_v3 where 
SUBSTR(pra_number,6,4) > 2018 or SUBSTR(pra_number,6,4) < 1970 order by years desc;

2、

select * from hht_lawyer_12348gov_v3 
where 
(SUBSTR(pra_number,6,4) <= 2018 or SUBSTR(pra_number,6,4) >= 1970) 
and SUBSTR(qua_number,2,4) - SUBSTR(pra_number,6,4) > 0 order by years desc;


一、时间编号
　　第一至四位数字表示时间，以年为序编单位。如2010（年）。
二、区域编号
　　第五、六位数字表示省、自治区、直辖市。如江西省代码为“36”。
　　第七、八位数字表示省直辖市、地区（州、盟）。如江西省南昌市代码为“3601”。
　　第九、十位数字表示县（市辖区、地辖市、旗、省直辖县级市）。如江西省南昌市东湖区代码为“360102”。
三、证书编号
　　第十一至十四位数字表示法律职业资格证书编排序号。


org_identity,pra_course:
按执业证号、姓名、律所一样关联，用lawyer_info_new_v3来更新：
update hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 
set a.org_identity = b.org_identity,
a.pra_course = b.pra_course;


select * from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number and a.name = b.name 
where a.org_name != b.org_name and b.pra_course != "" and right(b.pra_course,4) != "首次执业";

可以通过执业历程去找出最新的律所：
执业证号一样,姓名一样，律所不一样的才4千多条：
select a.pra_number,a.name,a.org_name,b.pra_number,b.name,b.org_name,b.pra_course 
from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number and a.name = b.name
where a.org_name != b.org_name and b.pra_course is not null and b.pra_course != "" and right(b.pra_course,4) != "首次执业";
2470条;

根据执业历程找出最新的律所，并更新律所、所内身份，执业历程字段；
select a.pra_number,a.name,a.org_name,b.pra_number,b.name,b.org_name,b.pra_course 
from hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number and a.name = b.name
where 
a.org_name != b.org_name and 
replace(replace(b.pra_course,"（","("),"）",")") like  CONCAT("%",a.org_name,"%") 
and b.pra_course is not null and b.pra_course != "" and right(b.pra_course,4) != "首次执业";

update hht_lawyer_12348gov_v3 a join lawyer_info_new_v3 b 
on a.pra_number = b.pra_number and a.name = b.name 
set 
a.org_name = b.org_name,
a.org_identity = b.org_identity,
a.pra_course = b.pra_course 
where 
a.org_name != b.org_name and 
replace(replace(b.pra_course,"（","("),"）",")") like  CONCAT("%",a.org_name,"%") 
and b.pra_course is not null and b.pra_course != "" and right(b.pra_course,4) != "首次执业";

update hht_lawyer_12348gov_v3 a 
join hht_lawyer_12348gov_v3_time_result b 
on a.pra_number = b.pra_number 
set 
a.birth_date = b.birth_date,
a.first_pra_time = b.first_pra_time,
a.qua_time = b.qua_time,
a.years = b.years;

select * from hht_lawyer_12348gov_v3 where CHAR_LENGTH(years) >= 2 and years > 50 
and (SUBSTR(pra_number,6,4) <= 2018 and SUBSTR(pra_number,6,4) >= 1970)

select * from hht_lawyer_12348gov_v3 where 
(SUBSTR(first_pra_time,1,4) < 1970 ) 
and first_pra_time is not null and first_pra_time != ""

select * from hht_lawyer_12348gov_v3 where years = "0"
update hht_lawyer_12348gov_v3 set years = 2018-SUBSTR(pra_number,6,4) + 1 where years = "0"
update hht_lawyer_12348gov_v3 set first_pra_time = SUBSTR(pra_number,6,4) where 
(SUBSTR(first_pra_time,1,4) > 2018 ) 
and first_pra_time is not null and first_pra_time != ""


select * from lawyer_info_new where name = "龙雄彪"

select * from hht_lawyer_12348gov_v3 where pra_course like "%注销%"


select name ,count(*) from hht_lawyer_12348gov_v3 group by name having(count(*) > 1) order by count(*) desc

select * from hht_lawyer_12348gov_v3 where name = "王伟"

select name ,count(*) from hht_lawyer_12348gov group by name having(count(*) > 1) order by count(*) desc

select * from lawyer_info_new where name = "熊微"
select * from hht_lawyer_12348gov_v3 where name = "王济"


select * from lawyer_info_new where name = "程美忠"

create table hht_lawyer_12348gov_v3_missing as 
select a.* from zy_lawyer_12348gov a left join hht_lawyer_12348gov_v3 b 
on a.pra_number = b.pra_number where b.pra_number is null;










