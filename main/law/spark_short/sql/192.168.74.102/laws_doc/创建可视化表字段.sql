select * from laws_doc2.judgment2_main_etl where uuid = '04214a1d-d28d-499e-8f33-a7b4017c2927'

select court,province,city from judgment_etl where city is null or city = '';

update court a ,laws_doc2.judgment2_main_etl b set b.province = a.province,b.city = a.city,b.court_cate = a.court_cate 
where a.name = b.court;


update court a ,laws_doc2.judgment2_etl b set b.province = a.province,b.city = a.city,b.court_cate = a.court_cate where a.name = b.court;

update court a ,judgment_main_etl b set b.province = a.province,b.city = a.city,b.court_cate = a.court_cate 
where a.name = b.court;

create table judgment_part_v2 as select id,uuid,caseid,result_type,title,
party_info,trial_process,court_find,judge_type from judgment where is_format = 1;



create table judgment_visualization as select 
id,uuid,court_cate,province,casedate,duration,age_year,
edu,nation,if_accumulate,gender,if_adult,if_nosuccess,
if_surrender,if_team,punish_money,punish_date,delay_date,
if_delay,punish_cate,reason,new_lawyer,new_office,fact_finder,court from judgment_etl;


update judgment_etl set judge_chief_origin = '' ;

=============================================================
create table uuid_judge as select uuid,judge from judgment_etl;

update uuid_judge a ,judgment_main_etl b set b.judge = a.judge where a.uuid = b.uuid;

update judgment_visualization set judge = ''





