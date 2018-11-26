create table judgment_visualization_v2 as 
select id,uuid,age_year,casedate,court_cate,delay_date,duration,edu,gender,
if_accumulate,if_adult,if_delay,if_surrender,if_team,new_lawyer,nation,new_office
province,punish_cate,punish_date,punish_money,reason from judgment_visualization;

select * from judgment_visualization_v2 where uuid = '1ea6dfb0-ba27-442b-a525-9a55e809f567';

select lawyer_id from judgment_main_etl where uuid = 'c0cdfbd6-7de2-4bce-aec9-ab8af9cf8381'
select lawyer_id from judgment_visualization_v2 where uuid = 'c0cdfbd6-7de2-4bce-aec9-ab8af9cf8381'

update judgment_visualization_v2 a,judgment_main_etl b set a.lawyer_id = b.lawyer_id where a.lawyer_id != '' and a.uuid = b.uuid;

update judgment_visualization_v2 a,judgment_main_etl b set a.plaintiff_id = b.plaintiff_id,a.defendant_id=b.defendant_id where a.uuid = b.uuid;

update judgment_visualization_v2 a,tmp_lawyers b set a.law_office = b.law_office where a.uuid = b.uuid;

select count(*) from judgment_visualization_v2 where LOCATE("||",lawyer_id)>0



INSERT into lawyers(id,lawyer,office) SELECT id,lawyer,office from lawyer

