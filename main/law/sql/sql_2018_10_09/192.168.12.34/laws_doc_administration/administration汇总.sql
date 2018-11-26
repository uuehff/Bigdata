
select id,caseid,party_info from administration_etl where CHAR_LENGTH(caseid) > 225; #caseid包含当事人信息
DELETE from administration_etl where CHAR_LENGTH(caseid) > 225;

alter table administration_etl
add title varchar(220),
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

update administration_etl a ,administration_part b set 
 a.title = b.title,
 a.lawlist = b.lawlist,
 a.type = b.type,
 a.judge_type = b.judge_type,
 a.reason_type = b.reason_type 
 where a.id = b.id;




