
create table imp_other_etl4 like imp_other_etl1;

insert into imp_other_etl1 select * from imp_other_etl3;

alter table imp_other_etl1 rename imp_other_etl;

alter table imp_other_etl
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

update imp_other_etl a ,imp_other_part b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.type = b.type,
 a.judge_type = b.judge_type,
 a.reason_type = "执行",
 a.reason = "其他执行"  
 where a.id = b.id;


