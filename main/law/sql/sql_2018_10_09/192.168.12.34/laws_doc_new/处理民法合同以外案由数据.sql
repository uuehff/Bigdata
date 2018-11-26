create table tmp_weiwc as select id,uuid,lawlist from judgment_new;

select * from tmp_weiwc where id <= 10 


select max(id) from tmp_hzj



17df0acd-0dc0-4adf-86d6-817416c6b00c	4179070144
390d255c-db77-4d16-894a-39007837cf5f	4179070144||4179070064
80560322-46cc-4a5d-ae52-15e91384889a	4179070144||4179070064||20279770002

select * from tmp_weiwc where uuid = "390d255c-db77-4d16-894a-39007837cf5f"


create table judgment_new1 as select 
id,uuid,caseid,title,casedate,party_info,trial_process,
trial_request,trial_reply,court_find,court_idea,judge_result,
doc_footer,type,reason from judgment_new where id <= 2780000

create table judgment_new2 as select 
id,uuid,caseid,title,casedate,party_info,trial_process,
trial_request,trial_reply,court_find,court_idea,judge_result,
doc_footer,type,reason from judgment_new where id > 2780000

create table judgment_new3 as select 
id,uuid,caseid,title,casedate,party_info,trial_process,
trial_request,trial_reply,court_find,court_idea,judge_result,
doc_footer,type,reason from judgment_new2 where id > 2780000 and id <= 4500000


create table judgment_new4 as select 
id,uuid,caseid,title,casedate,party_info,trial_process,
trial_request,trial_reply,court_find,court_idea,judge_result,
doc_footer,type,reason from judgment_new2 where id > 4500000




select count(*) from zzz group by uuid,reason,reason_uid,province,court_uid


select count(*) from judgment_new where casedate = ""

select type,reason_type,judge_type,count(*) from adjudication_xingshi_etl group by type,reason_type,judge_type


update judgment_new4
set type = 
case 
when type = "一审" then "1"
when type = "二审" then "2"
when type = "再审" then "3"
when type = "其他" then "4"
end;



id,uuid,caseid,title,casedate,party_info,trial_process,
trial_request,trial_reply,court_find,court_idea,judge_result,
doc_footer,type,reason

update judgment_part set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n') ;


select * from judgment_new where id < 1000 and court_find like "%\\n%"
select count(*) from tmp_lifeng where mark = "0"


update judgment_new1 set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n') ;

update judgment_new3 set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n') ;


update judgment_new4 set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n') ;


update tmp_footer set 
doc_footer = replace(doc_footer,'\\n','\n');

update tmp_hzj_new set 
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');

select id,plt_claim from tmp_hzj_new where id < 10000 and plt_claim like "%\\n%" ;

update court_reason_uid set reason_uid = "" where reason_uid = "||"

select court,court_uid from laws_doc.judgment_main_etl where uuid in 
("5a800987-31df-4674-9bc0-a7100097edcc",
"cf31be71-fd80-4ae7-b329-0c0eeaf9938d",
"307d8adf-bee3-4b75-8495-f39c15e90830",
"665f7807-b163-4bed-89db-159f5403ae33",
"cad6c70a-b93c-4436-9eea-f796a5d954ba",
"b8d53496-c7f3-4d7a-acd5-b44bbf1417ef",
"165d81a7-7dda-4d00-8558-e8459accfd26",
"882e2dcc-3b0f-45b3-892f-e0f2e9fbc12e",
"3fd99825-538a-4101-b48f-2428c5526194",
"b5aa68c0-ed0c-450e-83a0-145b399ff9b5",
"8e085bf6-3c01-40e0-a5c1-d89a2b652a1c")


create table casedate_validate2 as 
select * from judgment_new where id in (select id from casedate_validate);

update judgment_new1 a,casedate_validate2 b set a.casedate = b.casedate where a.id = b.id


update casedate_validate2 set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n') ;


