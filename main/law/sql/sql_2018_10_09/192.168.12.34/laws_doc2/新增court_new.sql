create table reason_add as 
SELECT uuid,court_new,province,city,district,court_uid,court_cate from judgment2_etl where court_uid is null or court_uid = ''


SELECT * from laws_doc.court where court_cate = '高级' and  court_new in (
SELECT court_new from court_add where court_cate = '高级' group by court_new,province)

SELECT * from laws_doc.court where court_new in (
SELECT court_new from court_add where court_cate != '高级' group by court_new)

SELECT court_new,province from court_add where court_cate = '高级' group by court_new,province

create table court_add_distinct as 
SELECT court_new,province,city,district,court_cate from court_add  group by court_new,province,city,district,court_cate

update laws_doc.court_province a, court_add_distinct b set b.uid = CONCAT(a.uid,'000'), b.pid = a.uid 
where a.province=b.province and b.court_cate = '高级'

SELECT court_new,province,uid,pid,court_cate from laws_doc.court where uid like '%000'

SELECT * from court_add_distinct where court_cate != '高级'

select * from laws_doc.court where court_new = '吉林省%铁路运输中级法院'

SELECT a.province,a.city from laws_doc.court_province_city a,court_add_distinct b where a.province =b.province 
and a.city=b.city and b.court_cate = '中级'


SELECT province,city from court_add_distinct where court_cate = '中级' and city not in (
SELECT a.city from laws_doc.court_province_city a,court_add_distinct b where a.province =b.province 
and a.city=b.city and b.court_cate = '中级'
)

select count(*) from laws_doc.court where pid = '03006'

update laws_doc.court_province_city a,court_add_distinct b set 
b.pid = a.pid_uid where a.province = b.province and a.city=b.city and b.court_cate = '中级'

SELECT province,city,pid,count(*) from laws_doc.court where pid in (SELECT pid from court_add_distinct where uid is null) 
group by province,city,pid order by pid

select pid from laws_doc2.court_add_distinct where uid is null group by pid

select id,pid from court_add_distinct where uid is null

update laws_doc.court set pid = '14033',uid = CONCAT('14033',SUBSTRING(uid,6,3)) where pid = '14001'

INSERT into laws_doc.court(court_new,province,city,court_cate,pid,uid) SELECT court_new,province,city,court_cate,pid,uid from court_add_distinct;



