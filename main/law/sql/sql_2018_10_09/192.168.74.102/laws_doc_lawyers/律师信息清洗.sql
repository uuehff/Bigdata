SELECT area from lawyer_info group by area;

update lawyer_info set province = area;



delete from lawyer_info where law_office = "律师事务所"

select LOCATE("省",law_office),count(*) from lawyer_info group by LOCATE("省",law_office)

select lawyer,law_office,char_no from lawyer_info group by lawyer,law_office,char_no having(count(*) > 1)

丁丽萍	辽宁卓政律师事务所	2
丁伽尼	北京大成（沈阳）律师事务所	6
丁剑	湖北维思德律师事务所	2
丁国臣	辽宁泽宇律师事务所	5
丁在元	湖北丁在元律师事务所	2
丁垚	北京炜衡律师事务所	2
丁宁	辽宁一鸣律师事务所	2
丁少飞	辽宁申扬律师事务所	3


select id,pra_course from lawyer_info where pra_course != "" and pra_course is not null 


create table uuid_court_province_city as SELECT uuid,court,province,city from laws_doc.judgment_main_etl


create table uuid_law_office2 as SELECT uuid,law_office from uuid_law_office where law_office != ""

create table law_office_province_city as SELECT a.law_office,b.province,b.city from uuid_law_office a ,uuid_court_province_city b where a.uuid = b.uuid;


select  law_office,count(*) from law_office_province_city group by law_office having(count(*) > 1)


update lawyers_full_outer_join a,id_province_city b 
set a.province = b.province,
a.city = b.city where a.id = b.id;

select * from (
select province,count(*) from lawyers_full_outer_join group by province 
) a
where a.province not like "%省%" and a.province not like "%市%" and a.province not like "%区%";

update lawyers_full_outer_join 
set province = 
case 
when province = "上海" then "上海市"
when province = "北京" then "北京市"
when province = "天津" then "天津市"
when province = "重庆" then "重庆市"
when province = "宁夏" then "宁夏回族自治区"
end;


select gender,count(*) from lawyers_full_outer_join group by gender 

update lawyers_full_outer_join 
set gender = 
case 
when gender = " 女" then "女"
when gender = " 男" then "男"
when gender = "1" then "男"
when gender = "2" then "女"
when gender = "女　" then "女"
when gender = "男　" then "男"
when gender = "高" then "男"
end;


update lawyers_full_outer_join 
set gender = 
case 
when SUBSTRING(char_no,11,1) = "1" then "女"      #17位执业证号的第十一位为性别，0为男，1为女。
when SUBSTRING(char_no,11,1) = "0" then "男"
end 
where (gender is null or gender = "" ) and char_no != "" and char_no is not null and LENGTH(char_no) =17 ; 

select id,gender,SUBSTRING(char_no,11,1) from lawyers_full_outer_join where gender is not null and LENGTH(char_no) = 17 limit 100

select id,char_no,gender from lawyers_full_outer_join where (gender is null or gender = "" ) and char_no != "" and char_no is not null and LENGTH(char_no) =17 ; 


select id,lawyer,char_no,first_pra_time,SUBSTR(char_no,6,4),CHAR_LENGTH(char_no) from lawyers where (first_pra_time like "0%" or first_pra_time like "9%") and CHAR_LENGTH(char_no) = 17 order by id
select id,lawyer,char_no,first_pra_time,SUBSTR(char_no,6,4),CHAR_LENGTH(char_no) from lawyers where (first_pra_time like "0%" or first_pra_time like "9%") 

update lawyers set first_pra_time = SUBSTR(char_no,6,4) where (first_pra_time like "0%" or first_pra_time like "9%") and CHAR_LENGTH(char_no) = 17;
update lawyers set first_pra_time = "" where (first_pra_time like "0%" or first_pra_time like "9%") ;



select id,lawyer,char_no,first_pra_time,2018-SUBSTR(first_pra_time,1,4) from lawyers where first_pra_time != "" and first_pra_time is not null limit 20;

update lawyers set years = 2018-SUBSTR(first_pra_time,1,4) where first_pra_time != "" and first_pra_time is not null ;

update lawyers set years = "" ;


565
25043
34007
50921
55329
59058
62795
66231
148732
156096
168745
181612
185185

update lawyers 
set province = 
case 
when province = "上海" then "上海市"
when province = "北京" then "北京市"
when province = "天津" then "天津市"
when province = "重庆" then "重庆市"
when province = "宁夏" then "宁夏回族自治区"
end;


select id,char_no,birthday,first_pra_time,qua_time,years from lawyers where id in (384487,387249,38885,390207,396374,411044,42399,425893,463716,476305,486837,4995,501338,520269,531926,
411044,531926,295929,327797,351357,355121,357441,360495,364716,367451,374385,152018,
157630,163019,165621,179858,194179,208716,226563,248030,260206,268834,105317) order by id


select count(qua_time)  from lawyers where qua_time != "" and qua_time is not null ;122969


select count(qua_time)  from lawyers where qua_time != "" and
 qua_time is not null and (CHAR_LENGTH(qua_time)=4 or CHAR_LENGTH(qua_time) = 10); #122574

select id,qua_time  from lawyers where qua_time != "" and qua_time is not null 
and CHAR_LENGTH(qua_time)!=4 and CHAR_LENGTH(qua_time) != 10 and CHAR_LENGTH(qua_time) != 7;  #395

select id,qua_time  from lawyers where qua_time != "" and qua_time is not null 
and qua_time like "%年%";  


411044	2016年3月
645906	2010-03-1
531926	2015-3-12
657511	2012-03-1

update lawyers set qua_time = 
case id
when 411044 then "2016-03"
when 645906 then "2010-03-01"
when 531926 then "2015-03-12"
when 657511 then "2012-03-01"
else qua_time end
where qua_time != "" and qua_time is not null 
and CHAR_LENGTH(qua_time)!=4 and CHAR_LENGTH(qua_time) != 10 and CHAR_LENGTH(qua_time) != 7; 


update lawyers set qua_time = 
case id
when 411044 then "2016-03"
else qua_time end
where qua_time != "" and qua_time is not null and qua_time like "%年%"; 


select id,
case lawyer 
WHEN "杨国宏" then "123"
else id end
from lawyers where id < 10;

update lawyers a , id_province_city b set a.province = b.province where a.city = b.city ;

update lawyers a , lawyers_v1 b set a.qua_time = b.qua_time where a.lawyer = b.lawyer and a.law_office = b.law_office;

update lawyers a , lawyer_info b set a.qua_time = b.qua_time where a.lawyer = b.lawyer and a.law_office = b.law_office;

246644
576854
select * from lawyers where law_office like "%黑龙江%" or law_office like "%内蒙古%" or law_office like "%宁夏%"
select law_office ,count(*) from lawyers where law_office like "%黑龙江%" group by law_office order by count(*) desc 
select law_office  from lawyers where law_office = "黑龙江鑫丰律师事务所"

select replace(replace(law_office,"黑龙江省","黑龙江"),"内蒙古自治区","内蒙古") from lawyers where id = 246644 or id = 576854;
内蒙古呼伦贝尔海拉尔区呼伦街道法律服务所律师事务所,黑龙江鑫丰律师事务所
多次替换：
# 内蒙古自治区
# 宁夏回族自治区
# 广西壮族自治区
# 新疆维吾尔自治区
# 西藏自治区
# 黑龙江省
方式一：可使用嵌套方式多次替换：
select replace(replace(law_office,"黑龙江省","黑龙江"),"内蒙古自治区","内蒙古") from lawyers where id = 246644 or id = 576854;

方式二：可连续赋值多次：
update lawyers set 
law_office = replace(law_office,"内蒙古自治区","内蒙古"),
law_office = replace(law_office,"宁夏回族自治区","宁夏"),
law_office = replace(law_office,"广西壮族自治区","广西"),
law_office = replace(law_office,"新疆维吾尔自治区","新疆"),
law_office = replace(law_office,"西藏自治区","西藏"),
law_office = replace(law_office,"黑龙江省","黑龙江") ;

select law_office from lawyers where id = 246644 or id = 576854;

内蒙古自治区呼伦贝尔海拉尔区呼伦街道法律服务所律师事务所
黑龙江省鑫丰律师事务所

select * from lawyers where char_no = ""
select * from lawyers where lawyer like  "张文峰" and law_office like "广东君孺律师事务所"

select * from lawyers_v1 where lawyer like  "张文峰" and law_office like "广东君孺律师事务所"
select * from lawyer_info where lawyer like  "张文峰" and law_office like "广东君孺律师事务所"
select * from law_office_province_city where  law_office like "广东君孺律师事务所"