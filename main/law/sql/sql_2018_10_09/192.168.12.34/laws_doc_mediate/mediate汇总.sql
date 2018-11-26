alter table mediate_civil_etl 
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

update mediate_civil_etl a ,mediate_valid b 
set a.title = b.title,
 a.lawlist = b.lawlist,
 a.reason_type = b.reason_type,
 a.type = b.type,
 a.judge_type = b.judge_type where a.id = b.id;

update mediate_civil_etl a ,mediate_civil_etl_court b 
set a.court = b.court where a.id = b.id;


select id,doc_footer from mediate_civil_etl where uuid  in (
select uuid from casedate_validate where casedate = "") order by id

select a.id,a.uuid,a.doc_footer from mediate_civil_etl a where a.doc_footer != "" and a.doc_footer is not null

select id,doc_content from mediate_valid where uuid in (
select uuid from mediate_civil_etl a where a.doc_footer = "" or a.doc_footer is null
)

select uuid from casedate_validate where casedate != ""












