select id,doc_footer,judge_result from civil_etl_v2_800w_01  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；

select id,doc_footer,judge_result from civil_etl_v2_800w_02  
where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%" limit 100;
无结果；
以下两个id有U3000,而不是u3000；
select id,doc_footer,court_idea,judge_result from civil_etl_v2_800w_02 where id = 9661125 or id = 13842027



create table casedate_error_uuid_old_01 as 
SELECT * from civil_etl_v2_800w_01 where SUBSTR(casedate,1,4) > 2018 ;
#7

SELECT id,uuid,casedate from civil_etl_v2_800w_01 where casedate > "2018-07-27" ;
空；

create table casedate_error_uuid_2018 as 
SELECT id,uuid,caseid,casedate from civil_etl_v2_800w_02 where casedate > "2018-07-27" ;
受影响的行: 38


update casedate_error_uuid_2018 set casedate = CONCAT("2017",SUBSTR(casedate,5,10));

create table casedate_error_uuid_old_02 as 
SELECT * from civil_etl_v2_800w_02 where SUBSTR(casedate,1,4) > 2018 ;

#35行

select max(id) from civil_etl_v2_800w_02;
#16437623
select min(id) from civil_etl_v2_800w_02;
#8000001


lawyer_id处理==================================
create table civil_etl_v2_1600w_lawyer_test as select * from civil_etl_v2_1600w_lawyer limit 100;
create table civil_etl_v2_1600w_lawyer_id like  civil_etl_v2_1600w_lawyer ;

select * from civil_etl_v2_1600w_lawyer_test where id not in (select id from civil_etl_v2_1600w_lawyer_id);


select * from civil_etl_v2_1600w_lawyer where plaintiff_info != "" and plaintiff_info not like "{%}" limit 100
select * from civil_etl_v2_1600w_lawyer where defendant_info != "" and defendant_info not like "{%}" limit 100
update civil_etl_v2_1600w_lawyer set plaintiff_info = "" where uuid = "93d494a717d3367bb44bd25bbb53598f"

-- or  defendant_info not like "{%}"


create table adjudication_civil_etl_v2_lawyer like civil_etl_v2_1600w_lawyer_id


select * from civil_etl_v2_800w_01 where judge_type = "通知" limit 100;


update civil_etl_v2_800w_01 a ,casedate_error_uuid_old_01 b set a.casedate = b.casedate where a.uuid = b.uuid;
update civil_etl_v2_800w_02 a ,casedate_error_uuid_old_02 b set a.casedate = b.casedate where a.uuid = b.uuid;


judgment_new_v2_court_cate_judge_footer


select * from civil_etl_v2_800w_01_court_cate_judge_footer where court_cate = "最高" limit 100;





