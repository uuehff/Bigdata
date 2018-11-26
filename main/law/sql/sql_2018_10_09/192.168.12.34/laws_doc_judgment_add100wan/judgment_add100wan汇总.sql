select * from judgment where id > 2824880 and id < 2824940; 新增起始id:2824917

create table judgment_add100wan_part as select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where 1=2;
INSERT into judgment_add100wan_part(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 2824916;


alter table judgment_add100wan_etl  
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

update judgment_add100wan_etl a ,judgment_add100wan_part b 
set a.caseid = b.caseid,
 a.title = b.title,
 a.court = b.court,
 a.lawlist = b.lawlist,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;