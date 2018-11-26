create table uuid_law_id_zhangye_civil_v4 like uuid_law_id_zhangye_civil_v2;
create table uuid_law_id_zhangye_xingshi_v4 like uuid_law_id_zhangye_civil_v2;
create table uuid_law_id_zhangye_xingzheng_v4 like uuid_law_id_zhangye_civil_v2;
create table uuid_law_id_zhangye_zhixing_v4 like uuid_law_id_zhangye_civil_v2;

create table judgment_zhangye_civil_v4_result like judgment_zhangye_civil_v4_result;
create table judgment_zhangye_xingshi_v4_result like judgment_zhangye_civil_v4_result;
create table judgment_zhangye_xingzheng_v4_result like judgment_zhangye_civil_v4_result;
create table judgment_zhangye_zhixing_v4_result like judgment_zhangye_civil_v4_result;


create table judgment_zhangye_civil_v4_result_court_cate_judge_footer like judgment_zhangye_civil_v2_result_court_cate_judge_footer;
create table judgment_zhangye_xingshi_v4_result_court_cate_judge_footer like judgment_zhangye_civil_v2_result_court_cate_judge_footer;
create table judgment_zhangye_xingzheng_v4_result_court_cate_judge_footer like judgment_zhangye_civil_v2_result_court_cate_judge_footer;
create table judgment_zhangye_zhixing_v4_result_court_cate_judge_footer like judgment_zhangye_civil_v2_result_court_cate_judge_footer;


create table judgment_zhangye_civil_v4_result_lawyer_id like judgment_zhangye_civil_v2_v3_result_lawyer_id;
create table judgment_zhangye_xingshi_v4_result_lawyer_id like judgment_zhangye_civil_v2_v3_result_lawyer_id;
create table judgment_zhangye_xingzheng_v4_result_lawyer_id like judgment_zhangye_civil_v2_v3_result_lawyer_id;
create table judgment_zhangye_zhixing_v4_result_lawyer_id like judgment_zhangye_civil_v2_v3_result_lawyer_id;



create table uuids as 
select uuid_old from judgment_zhangye_civil_v4_result 
union all 
select uuid_old from judgment_zhangye_xingshi_v4_result 
union all 
select uuid_old from judgment_zhangye_xingzheng_v4_result 
union all 
select uuid_old from judgment_zhangye_zhixing_v4_result 


select * from judgment_zhangye_xingzheng_v4_result  where uuid = "26849da4b48537ab8de5251166626a50"
select * from uuid_law_id_zhangye_civil_v4_new  where uuid = "5f166c698499343b9eb3d99b4361c0fd"


select * from  judgment_zhangye_civil_v4_result  where  uuid = "0c74ae7f8d2d3c379ac47758be9a3602";


update judgment_zhangye_xingzheng_v4_result a join province b
on b.province like CONCAT(a.province,"%") 
set a.province = b.province 
where a.province is not null and a.province != "";

update judgment_zhangye_xingshi_v4_result a join province b
on b.province like CONCAT(a.province,"%") 
set a.province = b.province 
where a.province is not null and a.province != "";


update judgment_zhangye_zhixing_v4_result a join province b
on b.province like CONCAT(a.province,"%") 
set a.province = b.province 
where a.province is not null and a.province != "";

update judgment_zhangye_civil_v4_result a join province b
on b.province like CONCAT(a.province,"%") 
set a.province = b.province 
where a.province is not null and a.province != "";



select table_name 
from information_schema.tables 
where table_schema='laws_doc_zhangye_v2' and table_name like "%v4%" order by table_name
