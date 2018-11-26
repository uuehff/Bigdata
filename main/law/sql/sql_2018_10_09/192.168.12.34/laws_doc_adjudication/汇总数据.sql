select min(id),max(id) from adjudication_xingshi_etl where id <= 1000000 and doc_from = "limai"

insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_02;
insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_03;
insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_04;
insert into adjudication_civil_etl_01 select * from adjudication_civil_etl_wenshu;

insert into adjudication_civil_etl_01(id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer
) select * from adjudication_civil_etl_wenshu ;


alter table adjudication_civil_etl_01 
add caseid varchar(80),
add title varchar(220),
add court varchar(255),
add court_uid varchar(255),
add lawlist text,
add law_id text,
add casedate varchar(255),
add reason_type varchar(255),
add type varchar(255),
add judge_type varchar(255),
add reason varchar(255),
add reason_uid varchar(255),
add province varchar(250),
add plt_claim mediumtext,
add dft_rep mediumtext,
add crs_exm mediumtext;

create table z2 select id from adjudication_civil_etl_wenshu

update adjudication_xingshi_etl a ,adjudication_xingshi_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

update adjudication_xingshi_etl_01 a ,adjudication_xingshi_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;


update adjudication_civil_etl a ,adjudication_civil_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

update adjudication_civil_etl_01 a ,adjudication_civil_part_fields b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.casedate = b.casedate,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

select type,reason_type,judge_type,count(*) from adjudication_xingshi_etl group by type,reason_type,judge_type
	刑事	裁定	309492
	民事	裁定	309492


update judgment_new 
set type = 
case 
when type = "一审" then "1"
when type = "二审" then "2"
when type = "再审" then "3"
when type = "其他" then "4"
end
