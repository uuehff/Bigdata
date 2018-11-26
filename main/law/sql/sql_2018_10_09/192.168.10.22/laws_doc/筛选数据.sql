INSERT into judgment_new(id,uuid,caseid,title,court,lawlist,casedate,party_info,trial_process,trial_request,trial_reply,court_find,court_idea,judge_result,doc_footer,type,reason
) SELECT id,uuid,caseid,title,court,lawlist,casedate,party_info,trial_process,trial_request,trial_reply,court_find,court_idea,judge_result,doc_footer,type,reason
) SELECT id,uuid,caseid,title,court,lawlist,casedate,party_info,trial_process,trial_request,trial_reply,court_find,court_idea,judge_result,doc_footer,type,reason
 from judgment where is_format = "1" 

create table adjudication_civil_part as select id,uuid,caseid,title,court,lawlist,casedate,reason_type,type,judge_type from adjudication_civil;
create table adjudication_xingshi_part as select id,uuid,caseid,title,court,lawlist,casedate,reason_type,type,judge_type from adjudication_xingshi;
create table implement_part as select id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type from implement;

create table imp_other_part like implement_part;
INSERT into imp_other_part(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type from imp_other;

create table administration_part like implement_part;
INSERT into administration_part(id,uuid,title,lawlist,reason_type,type,judge_type) select id,uuid,title,lawlist,reason_type,type,judge_type from administration;



INSERT into judgment_new(id,uuid,judge_result,doc_footer) 
SELECT id,uuid,judge_result,doc_footer
 from judgment where is_format = "1" 

create table uuid_judge_type as select uuid,judge_type from  judgment where is_format = "1" 


create table adjudication_civil as select * from adjudication where reason_type = "民事"


select doc_from,count(*) from adjudication_civil where id < 100 group  by doc_from 

limai	3569360
wenshu	217

select max(id) from adjudication_civil 

create table mediate_valid as 
select * from mediate where doc_content like "%litigantpart%" and doc_content like "%result%";



select count(*) from adjudication_civil where id = 82105 and doc_from = "limai"

create table  z1_o as select id from adjudication_civil_part_fields

delete from adjudication_civil where id in (
select id FROM z1_o LEFT JOIN  
(select id as i from z1) as t1  
ON z1_o.id=t1.i where t1.i IS NULL
)

select id FROM z1_o LEFT JOIN  
(select id as i from z1) as t1  
ON z1_o.id=t1.i where t1.i IS NULL 

