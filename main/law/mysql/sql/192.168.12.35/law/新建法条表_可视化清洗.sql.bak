create table law_rule_result3 as select 
id,law_id,cate_a,cate_b,department,publish_date,effective_date,
effective_range,effective_status,title_short,art,area,doc_num,art_digit from law_rule_result2 where id <= 2880869 and error = '';


select id,law_id,art  from law_rule_result3 where art like '%作面...%'

select art  from law_rule_result4 where art like '%作面...%'

select * from law_rule_result2 where law_id = '143423'

update law_rule_result2 set lawlist_id = CONCAT(law_id,LPAD(art_digit,4,'0')) where id >= 2880870;

id[2880870

select art_digit,lawlist_id from law_rule_result2 where id >= 2880870 limit 10


select id,lawlist_id  from law_rule_result2 where id in (5759,6123,5773,1245146,5731,6068,5816)


select *  from law_rule_result_article where department like "%。%" 

update law_rule_result_article set department = "劳动保障部、财政部" where id = 532622

create table law_rule_result2_error as 
select *  from law_rule_result2 where error != "" ;

delete from law_rule_result2 where error != "" ;










