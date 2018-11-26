select area,count(*) from law_rule_result_article group by area;
|湖北	1
上海	24284
云南	7125
全国	170512
内蒙古	7657
北京	26781
台湾	59
吉林	10219
四川	17038
天津	9566
宁夏	4887
安徽	15246
山东	22741
山西	10132
广东	35056
广西	13436
新疆	7868
江苏	27091
江西	11191
河北	13547
河南	16022
浙江	23967
海南	7328
湖北	14236
湖南	12527
澳门	34
甘肃	8190
福建	23780
西藏	1584
贵州	8118
辽宁	17089
重庆	11852
陕西	14440
青海	4240
香港	52
黑龙江	11767
select province,city from province_city_full_uid group by province,city

select count(distinct law_id) from law_rule_result_article   609662

select count(law_id) from law_rule_result_article   609663


select law_id from law_rule_result_article group by law_id having(count(law_id) > 1)
select * from law_rule_result_article where law_id = "5321"

update law_rule_result_article a,law_area_uid b 
set a.city = b.city,
a.area_uid = b.area_uid where a.law_id = b.law_uid;

update law_rule_result2 a,law_area_uid b 
set a.city = b.city,
a.area_uid = b.area_uid where a.law_id = b.law_uid;



update law_rule_result2 set area_uid = "00" where  area = "全国";
update law_rule_result_article set area_uid = "00" where  area = "全国";



update province_city_full_uid 
set uid = full_uid,
parent = "00" where city is null;


update province_city_full_uid 
set uid = SUBSTRING(full_uid,5),
parent = SUBSTRING(full_uid,1,2),
province = city where id > 31;

select SUBSTRING(full_uid,1,2),SUBSTRING(full_uid,5) from province_city_full_uid where id > 31

select * from law_rule_result3 where id = 2408949


create table law_rule_result_part as 
select id,law_id,cate_a,department,area,area_uid,city from law_rule_result_article where area = "全国";


select department,count(*) from law_rule_result_part group by department order by count(*) desc;

create table law_rule_result_part_filter as 
select * from law_rule_result_part where area != "全国";


update law_rule_result_article a ,law_rule_result_part_filter b 
set a.area= b.area,
a.area_uid = b.area_uid,
a.city = b.city where a.law_id = b.law_id;


update law_rule_result2 a ,law_rule_result_part_filter b 
set a.area= b.area,
a.area_uid = b.area_uid,
a.city = b.city where a.law_id = b.law_id;


