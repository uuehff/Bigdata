SELECT province,city,COUNT(*) from court group by province,city
SELECT * from court where province = 'None'

SELECT * from tmp_wwc_court where p = '7004'

SELECT * from tmp_wwc_court where p = '7005'
SELECT * from tmp_wwc_court where p = '7113'
SELECT * from tmp_wwc_court where i = '7120'
SELECT * from tmp_wwc_court where i = '7113'

SELECT province,city,district from court where province = city GROUP BY province,city,district


CREATE table court3 as SELECT * from court2;

CREATE table court_province as SELECT province from court GROUP BY province;
UPDATE court_province a, court b set b.pid = a.uid  where a.province = b.province and  b.court_cate = '高级'

UPDATE court_province a, court_city b set b.pid = a.uid  where a.province = b.province  and  b.court_cate = '高级'

UPDATE court_province a, court_city b set b.pid = a.uid  where a.province = b.province

UPDATE court_city a, court b set b.pid = a.pid, b.uid=a.pid_uid  where a.province = b.province and a.city = b.city and b.court_cate='中级'

UPDATE court set uid = CONCAT(pid,'00') where court_cate='高级'

UPDATE court set city = district where province = city


CREATE table court_city as  SELECT province,city from court group by province,city

SELECT province,city,district  from court GROUP BY province,city,district 


SELECT *  from court_city_null where city = "" 

SELECT *  from court_city_null where city = ''  and court_new like '%市%市%'

select *  from court_city_null where city = ''  and court_new like '%自治区%市%'

create table court_city_null SELECT *  from court where city = ""  


SELECT * from court where (city = "" or city is null) and (district = "" or district is null)

SELECT * from court_city_null where court_new like '%市%市%'

SELECT * from court where city = province
SELECT * from court where  city_api is not null and city != city_api and province not in ("上海市","天津市","北京市","重庆市") and city not like '%市'

SELECT * from court where province in ("上海市","天津市","北京市","重庆市")

SELECT count(*) from court where province = "上海市"  27
SELECT count(*) from court where province = "天津市"  22
SELECT count(*) from court where province = "北京市"  26
SELECT count(*) from court where province = "重庆市"  70



UPDATE court a , court_city_null b  set a.city = b.city where a.city = '' and b.city != ''

SELECT * from court where province in ("上海市","天津市","北京市","重庆市") and province = city


UPDATE court set city = district where province in ("上海市","天津市","北京市","重庆市") and city != district  and district != '' and district is not null 

UPDATE court set city = district_api where province in ("上海市","天津市","北京市","重庆市") and province = city


SELECT * from court where province in ("上海市","天津市","北京市","重庆市") and province != city

SELECT * from court where city not like '%区' and city  not like '%县' and province in ("上海市","天津市","北京市","重庆市")
SELECT * from court where city  like '%县' and province in ("上海市","天津市","北京市","重庆市")
SELECT * from court_city_null where court_new = '重庆市第一中级人民法院'

SELECT * from court where court_new is not null and (city = city_api)

UPDATE court set city_api = city,district_api=district  where court_new is not null and city_api is null and city is not null and city != '' 

UPDATE court set city_api = city  where city = '呼和浩特市' and province in ("上海市","天津市","北京市","重庆市")
select * from court where city_api = '呼和浩特市'
select * from court2 where city_api = '呼和浩特市'

select * from court where city_api is null

select court_new,province,city,district from judgment_etl where city = '呼和浩特市' and province != '内蒙古自治区'

检测结果：
SELECT * from court where court_new is not null and city != city_api and city != district and city != district_api 

SELECT * from court where  court_new is not null and city_api is null
SELECT * from court where  court_new is not null and city_api is null and city is not null

create table hands_etl_city as SELECT * from court where  court_new is not null and city_api is null

UPDATE court a,judgment_etl b set a.province = b.province,a.city = b.city,a.district = b.district where a.court_new = b.court_new


UPDATE court a,judgment_etl b set a.province = b.province where a.court_new = b.court_new


UPDATE court a,hands_etl_city b set a.city = b.city,a.district = b.district,a.city_api = b.city,a.district_api= b.district where a.court_new is not null and a.city_api is null and a.court_new = b.court_new

UPDATE court set city = city_api, district = district_api where court_new is not null

SELECT province,city from court where court_new is not null group by province,city

SELECT * from court where court_new is not null and city_api is null

select court_new,court,province,city,district from judgment_etl where court_new = '福建省福州铁路运输法院'

select court_new,province,city from judgment_etl where court_new = '黑龙江省双鸭山市宝山区人民法院'

select court_new from tmp_wxy where court_new = '黑龙江省双鸭山市宝山区人民法院'

select court,province,city,district from tmp_raolu where court = '黑龙江省双鸭山市宝山区人民法院'

SELECT * from court where (city != city_api or district != district_api
SELECT id from court where court_new is not null and province = city and city != district

SELECT * from court where court_new is not null and province = city and city = district

SELECT * from court where court_new is not null and province in ("上海市","天津市","北京市","重庆市") and id not in 
(SELECT id from court where court_new is not null and province = city and city != district
)

update court set district = '浦东新区' ,district_api = '浦东新区' where court_new = '上海市第三中级人民法院'

update court set city = district ,city_api = district_api where province in ("上海市","天津市","北京市","重庆市")
update court set pid = NULL ,uid = NULL

SELECT count(*) from court where uid is null


CREATE table court_province as SELECT province from court GROUP BY province

SELECT count(province) from court GROUP BY province,city order by count(province) desc

UPDATE court_province set uid = 

SELECT * from judgment_etl where court_new = '河南省高级人民法院' and court_cate = '高级' 

SELECT * from judgment_etl where court_new = '浙江省高级人民法院' and court_cate = '高级' 

SELECT court_new from judgment_etl where court_new = '最高人民法院' and court_cate = '高级'

SELECT * from (SELECT court_new from judgment_etl GROUP BY court_new) a where court_new in (
SELECT court_new from court 
) 

update court a ,court_province b set a.uid = b.uid where a.court_new is null and a.city is null and a.province = b.province 

create table court_province_city as 
select province,city,count(*) from court where court_new is not null and court_cate != '高级' group by province,city 


SELECT province,COUNT(province) from court where province = '上海市' 

SELECT * from court where province = '上海市' and city = '徐汇区' 

update court_province_city a, court_province b set a.pid = b.uid where a.province = b.province 


select province,count(province) from court_province_city group by province

update court a, court_province_city b set a.uid = b.pid_uid,a.pid = b.pid where a.province = b.province and a.city = b.city and a.court_cate != '高级'

SELECT * from court where uid = '01001'

UPDATE court a ,court_province_city b set a.pid = b.pid_uid where a.court_new is not null and a.province = b.province and a.city = b.city and a.court_cate != '高级'

UPDATE court set uid = CONCAT(pid,uid) where court_new is not null and court_cate != '高级'
SELECT * from court where pid is null


UPDATE court a ,court_province b set a.uid = CONCAT(pid,'000') where a.province = b.province and a.court_cate = '高级'
UPDATE court set pid = NULL, uid = NULL 

update court_province_city set pid_uid = CONCAT(pid,uid)
处理流程：
1、分组统计省份创建court_province表，并使用程序填充id。
导入court_province表到court表：
INSERT INTO court(province,uid) SELECT province,uid from court_province
1-1：court_cate为高级的需单独处理！使用court_province更新province字段，再使用concat(pid,'000')更新uid！

2、分组统计province,city同时需要过滤掉court_cate为'高级'的数据：
create table court_province_city as 
select province,city,count(*) from court where court_new is not null and court_cate != '高级' group by province,city 
之后添加uid,pid,uid_pid字段，pid可以使用court_province表更新。uid字段使用court_province_city_uid_pid.py处理填充。

3、将court_province_city数据插入到court表：
INSERT INTO court(province,city,pid,uid) SELECT province,city,pid,pid_uid from court_province_city   

court表按uid升序或pid升序即可查看结构。

更新一审：
UPDATE reason a , judgment_etl b set b.reason_uid = a.uid where a.new_name = b.new_reason
UPDATE court a , judgment_etl b set b.court_uid = a.uid where b.court_new is not null and a.court_new = b.court_new

更新二审：
UPDATE reason a , laws_doc2.judgment2_etl b set b.reason_uid = a.uid where a.new_name = b.new_reason
UPDATE court a , laws_doc2.judgment2_etl b set b.court_uid = a.uid where b.court_new is not null and a.court_new = b.court_new and b.court_uid is not null

UPDATE court a , laws_doc2.judgment2_etl b set b.court_uid = a.uid 
where b.court_new is not null and a.court_new = b.court_new 


create table laws_doc2.judgment2_etl_new_reason_great_2 as 
SELECT id,uuid,new_reason from laws_doc2.judgment2_etl where new_reason is not null and new_reason != ''


UPDATE laws_doc2.judgment2_etl_new_reason_great_2_result a,laws_doc2.judgment2_etl b set b.reason_uid = a.reason_uids where a.uuid = b.uuid



select * from laws_doc2.judgment2_etl where court_new = '四川省高级人民法院'

SELECT uuid ,court_new,court_uid from laws_doc2.judgment2_etl where court_uid is null

SELECT uuid ,new_reason,reason_uid from laws_doc2.judgment2_etl where reason_uid is null 

SELECT court_new, province from court where court_new like '%广西壮族自治区%'

SELECT court_new, province ,SUBSTRING(court_new,1,7) from court where SUBSTRING(court_new,1,7) = '广西壮族自治区'

create table court_orderBy_uid as SELECT * from court order by uid 

UPDATE reason_bashou set new_reason = CONCAT(n,'罪') 

SELECT * from reason_bashou where new_reason in (
SELECT new_name from reason
)



