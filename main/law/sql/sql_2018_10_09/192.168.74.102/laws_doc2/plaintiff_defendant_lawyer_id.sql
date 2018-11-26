update judgment2_main_etl a,tmp_hzj_JudgeResult b set 
a.punish_cate = b.punish_cate,
a.punish_date= b.punish_date,
a.punish_money= b.punish_money,
a.delay_date = b.delay_date where a.uuid = b.uuid ;


update judgment2_main_etl a,tmp_hzj b set 
a.edu = b.edu,
a.gender = b.gender,
a.nation = b.nation where a.uuid = b.uuid ;

update tmp_lawyers set plaintiff_id = NULL,defendant_id = NULL 

update tmp_lawyers a,plain_defen_id b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.defendant_id,
a.lawyer_id = CONCAT_WS("||",b.plaintiff_id,b.defendant_id)   #CONCAT_WS忽略连接中的NULL值。
where a.id = b.id;

==========================================
update judgment2_main_etl a,tmp_lawyers b set 
a.plaintiff_id = b.plaintiff_id,
a.defendant_id = b.defendant_id,
a.lawyer_id = b.lawyer_id   #CONCAT_WS忽略连接中的NULL值。
where a.uuid = b.uuid;


create table judgment2_visualization_v2 as select 
id,uuid,age_year,casedate,court_cate,delay_date,duration,edu,gender,
if_accumulate,if_adult,if_delay,if_surrender,if_team,lawyer_id,nation,
province,punish_cate,punish_date,punish_money,reason,plaintiff_id,
defendant_id from judgment2_main_etl;


update judgment2_visualization_v2 a,tmp_lawyers b set 
a.law_office = b.law_office where b.law_office != '' and a.uuid = b.uuid;

update judgment2_main_etl a,tmp_lawyers b set 
a.lawyer = b.lawyer   #CONCAT_WS忽略连接中的NULL值。
where a.uuid = b.uuid;

select uuid,law_id from judgment2_main_etl where id < 10;
dd608633-e4cb-4ebe-8ccd-efd6bdae3320	5915||5712||5763||5803||5805||6276||5773||5765||5787||5707||6277||5797||5795||6279||5789||6068||5777
d57463b2-2f0a-4991-a67e-6c69f8757717	5712||5763||6276||5709||5773||5765||6283||5787||5707||6068||5777
08314a7a-5401-497b-b594-e3245d2b52a0	5759||6123||5773||5755||5707||5793||6068
290ec86b-fbc9-4fff-8d49-df1bad654316	5712||5763||5785||6276||5709||5773||5765||5787||5707||5795||5793||5779||6068||5777
31f559e0-735f-4f71-9446-094b4629c42b	6276||5773||5787||5789||6068||5777
53ce0796-783f-4f36-928e-c764c0dd561f	5763||5996||6276||5773||5765||5753||5787||5707||5795||5769||5701||5793||5777||5698
043049aa-5b3f-4f73-999a-44709bdac023	5915||5712||5996||6276||5709||5773||6283||5781||5787||5707||5797||5793||5789
d2d318dc-7933-4c3b-835b-ee4c781cfb63	5759||6123||5773||1245146||5731||6068||5816
199cdf42-5739-4ab9-98f6-7e79896ae7fc	5801||6276||5755||5707||5797||6285||5789||6068||5777

tmp_lawlist_id:
select * from tmp_lawlist_id where uuid = 'd2d318dc-7933-4c3b-835b-ee4c781cfb63'
update judgment2_main_etl a, tmp_lawlist_id b set a.law_id = b.law_id where a.uuid = b.uuid ;

select law_id from judgment2_main_etl where law_id = '' or law_id is null

