create table uuid_reason_lawlist as select uuid,doc_reason,lawlist from judgment where is_format = 1 and judge_type = '判决';

create table judgment_etl as select * from tmp_wxy where update_flag = '1';

create table uuid_court_history as select uuid,court,history_origin from judgment_etl;


select distinct(court) from uuid_court_history where court not in (select name from court);

同时添加多个字段和索引：
alter table judgment_etl 
add court_uid varchar(255),
add reason_uid varchar(255),
add law_id varchar(255),
add reason varchar(255),
add history text,
add unique index uuid(uuid),
add index court(court);


update judgment_etl a,court b set a.court_uid = b.full_uid where a.court = b.name;