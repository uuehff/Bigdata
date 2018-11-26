select * from lawyers where id = 528712

34	64da4393-61a9-4ac8-a3f4-6210aaaadf60			{"桂文涛": "安徽克群律师事务所", "鲍克群": "安徽克群律师事务所", "吴何军": "安徽古圣律师事务所"}			

update plain_defen_id set plaintiff_id = NULL where id = 20
update tmp_lawyers set plaintiff_id = NULL,defendant_id = NULL,lawyer_id = NULL


update tmp_lawyers a,plain_defen_id b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.denfendant_id,
a.lawyer_id = CONCAT_WS("||",b.plaintiff_id,b.denfendant_id)   #CONCAT_WS忽略连接中的NULL值。
where a.id = b.id;

update judgment_main_etl set plaintiff_id = NULL,defendant_id = NULL,lawyer_id = NULL
update judgment_etl set plaintiff_id = NULL,defendant_id = NULL,lawyer_id = NULL
update judgment_visualization_v2 set plaintiff_id = NULL,defendant_id = NULL,lawyer_id = NULL


update judgment_etl a,tmp_lawyers b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.defendant_id,
a.lawyer_id = b.lawyer_id   #CONCAT_WS忽略连接中的NULL值。
where a.uuid = b.uuid;

update judgment_main_etl a,tmp_lawyers b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.defendant_id,
a.lawyer_id = b.lawyer_id   #CONCAT_WS忽略连接中的NULL值。
where a.uuid = b.uuid;

update judgment_visualization_v2 a,tmp_lawyers b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.defendant_id,
a.lawyer_id = b.lawyer_id   #CONCAT_WS忽略连接中的NULL值。
where a.uuid = b.uuid;

update judgment_visualization_v2 a,tmp_lawyers b set 
a.law_office = b.law_office where b.law_office != '' and a.uuid = b.uuid;

update judgment_main_etl a,tmp_lawyers b set 
a.lawyer = b.lawyer 
where a.uuid = b.uuid;


update judgment_main_etl a, tmp_lawlist_id b set a.law_id = b.law_id where a.uuid = b.uuid ;

update lawyers a,lawyers_ b set 
a.char_no = b.char_no,
a.years = b.years where a.lawyer= b.lawyer and a.law_office=b.law_office;

select uuid,punish_cate,punish_date,if_delay,delay_date,punish_money from judgment_visualization_v2 where id<100 and punish_cate = '拘役'
select uuid,punish_cate,punish_date,if_delay,delay_date,punish_money from judgment_visualization_v2 where id<10000 and punish_cate = '管制'
select id,uuid,punish_cate,punish_date,if_delay,delay_date,punish_money from judgment_visualization_v2 where id<100000 and punish_cate = '死刑'
select uuid,punish_cate,punish_date,if_delay,delay_date,punish_money from judgment_visualization_v2 where uuid = "799be3b1-39b2-49af-8f92-34fe946ac22c"

update laws_doc2.tmp_hzj_JudgeResult a ,laws_doc2.judgment2_visualization_v2 b set 
b.if_delay = a.if_delay where a.uuid = b.uuid

select * from laws_doc2.judgment2_visualization_v2 where if_delay is not null


