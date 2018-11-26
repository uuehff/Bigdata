show index from judgment_part_v2

民法：
create table civil_finance_all_fields as select a.*,b.keyword,b.child,b.parent from judgment_civil_all a,civil_finance b where a.uuid = b.uuid;

select * from laws_finance where uuid  not in (select uuid from laws_finance_etl);
刑法一审：
create table laws_finance_etl as select a.*,b.keyword,b.child,b.parent from judgment_main_etl a,laws_finance b  where a.uuid = b.uuid;
create table laws_finance_doc_fields as select a.*,b.caseid,b.result_type,b.title,b.party_info,b.trial_process,b.court_find,b.judge_type from laws_finance_etl a,judgment_part_v2 b where  a.uuid = b.uuid;

刑法二审：

create table laws_doc2.laws_finance_etl as select a.*,b.keyword,b.child,b.parent from laws_doc2.judgment2_main_etl a,laws_doc2.laws_finance b  where a.uuid = b.uuid;

create table laws_finance_doc2_fields as select a.*,b.caseid,b.result_type,b.title,b.party_info,b.trial_process,b.court_find,b.judge_type from laws_doc2.laws_finance_etl a,laws_doc2.judgment2 b where  a.uuid = b.uuid;


