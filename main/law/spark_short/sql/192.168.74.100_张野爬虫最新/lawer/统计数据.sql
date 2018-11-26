create table test_zy_lawyer as select * from zy_lawyer where name is not null;
select count(*)  from zy_lawyer where name is not null;
select count(*)  from zy_lawyer where pra_no is not null;

select *  from zy_lawyer where name is  null limit 10; 


select * from hht_lawyer_bsgs where name = "龙雄彪"

select pra_number from hht_lawfirm_12348gov where CHAR_LENGTH(pra_number) != 17 
-- and left(pra_number,1) = "0" 
order by pra_number


select * from hht_lawyer_anhui where  pra_number  =  "120015004458"
select * from hht_lawyer_anhui where  phone  =  "18655507896"

select * from hht_lawyer_gansu where pra_number in (
select pra_number from hht_lawyer_gansu group by pra_number having(count(*) > 1)) order by pra_number


SELECT * from hht_lawyer_hubei where org_name REGEXP '[a-z0-9A-Z ,:;-\\+!@.|"\'/]|\\?|\\]|\\[' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';



select *  
from information_schema.tables 
where table_schema = "lawer" and 
table_name not in ( select table_name from lawyers_table ) 
and table_name not like "%12348gov%" 
and table_name like "hht_lawyer_%";



select phone from hht_lawyer_lawtime 
where phone is not null and phone not like "%***%";

create table hht_lawyer_lawtime_filter as 
select * from hht_lawyer_lawtime 
where 
pra_number is not null 
and name is not null 
and org_name is not null 
and phone is not null 
and phone not like "%***%";

hht_lawyer_bingtuan
hht_lawyer_guangxi
hht_lawyer_guizhou
hht_lawyer_henan
hht_lawyer_liaoning
hht_lawyer_qinghai
hht_lawyer_shanxi
hht_lawyer_sichuan
hht_lawyer_tianjin
hht_lawyer_xinjiang
hht_lawyer_xizang
hht_lawyer_yunnan
===================================================
select "123" as table_nme,b.* from hht_lawyer_gansu b where id < 50000

select table_name 
from information_schema.tables 
where table_schema = "lawer" 
and table_name != "hht_lawyer_12348gov" 
and table_name like "hht_lawyer_%" 
or (table_name like "lawyer_info" or table_name = "zy_lawyer_12348gov") ;



============================
hht_lawyer_anhui
hht_lawyer_bingtuan
hht_lawyer_bsgs
hht_lawyer_guizhou
hht_lawyer_heilongjiang
hht_lawyer_jiangxi
hht_lawyer_lawtime
hht_lawyer_ningxia
hht_lawyer_qinghai
hht_lawyer_shandong

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
============================
年度考核统计：
hht_lawyer_bsgs
hht_lawyer_gds_gdlawyer
hht_lawyer_guizhou
hht_lawyer_hunan
hht_lawyer_jiangsu
hht_lawyer_liaoning
hht_lawyer_yunnan

select annualass from hht_lawyer_bsgs where annualass != "" and annualass != "<tbody>\n</tbody>" and annualass like "%事务所%";
结果为空；

select annualass from hht_lawyer_bsgs where annualass != "" and annualass like "%事务所%";
结果为空；

select annualass from hht_lawyer_guizhou where annualass != "" and annualass like "%事务所%";
结果为空；

select org_name,annualass from hht_lawyer_hunan where annualass != "" and annualass like "%事务所%";
有结果；
create table hht_lawyer_hunan_annualass as select pra_number,name,org_name,annualass from hht_lawyer_hunan where annualass != "" and annualass like "%事务所%";

select org_name,annualass from hht_lawyer_jiangsu where annualass != "" and annualass like "%事务所%";
有结果；

create table hht_lawyer_jiangsu_annualass as select pra_number,name,org_name,annualass from hht_lawyer_jiangsu where annualass != "" and annualass like "%事务所%";

select org_name,annualass from hht_lawyer_liaoning where annualass != "" and annualass like "%事务所%";
无结果；

select org_name,annualass from hht_lawyer_yunnan where annualass != "" and annualass like "%事务所%";
无结果；

select * from hht_lawyer_bsgs where name = "向纯华";
select * from hht_lawyer_gds_gdlawyer where name = "向纯华";
select * from hht_lawyer_12348gov where name = "向纯华";


