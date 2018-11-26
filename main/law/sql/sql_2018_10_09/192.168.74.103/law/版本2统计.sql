select * from law_rule_result2  where CHAR_LENGTH(law_id) <3  limit 120
select * from law_rule_result2  where law_id = 15002923  limit 120

update law_rule_result2 set law_id = id ;

update law_rule_result_article set law_id = id ;

update law_rule_result2 set lawlist_id = CONCAT_WS("",law_id,LPAD(art_digit,4,0)) ;
select id,law_id,art_digit,CONCAT_WS("",law_id,LPAD(art_digit,4,0)) from  law_rule_result2 where id < 100  ;

create table id_uuid as select id,law_id from law_rule_result_article;


update law_rule_result2 a,id_uuid b set a.law_id = b.id  where a.law_id = b.law_id ;

select a.id,a.law_id, a.art_digit ,a.lawlist_id, b.id,b.law_id from  law_rule_result2 a,id_uuid b  where a.law_id = b.law_id and  a.id < 20;


select id,law_id from id_uuid where law_id = 95697

348353	95697
select id,law_id from id_uuid where id = 95697
95697	219792