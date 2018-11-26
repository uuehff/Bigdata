一审：
create table judgment_main_etl as select id,uuid,court_idea,judge_result,doc_footer,plt_claim,dft_rep,crs_exm,
court,type,province,city,if_surrender,if_nosuccess,if_guity,
if_accumulate,if_right,if_team,if_adult,age_year,law_id,reason_uid,court_uid,
reason,org_plaintiff,org_defendant,dispute,court_cate,casedate,if_delay,age_min,duration from judgment_etl



update judgment_main_etl a , judgment_etl b set 
a.casedate = b.casedate,
a.if_delay = b.if_delay,
a.age_min = b.age_min,
a.duration = b.duration where a.uuid = b.uuid

update judgment_etl a , tmp_hzj_pltdft b set 
a.plt_claim = b.plt_claim,
a.dft_rep = b.dft_rep,
a.crs_exm = b.crs_exm  where a.uuid = b.uuid


update judgment_main_etl a , tmp_hzj_pltdft b set 
a.plt_claim = b.plt_claim,
a.dft_rep = b.dft_rep,
a.crs_exm = b.crs_exm  where a.uuid = b.uuid

select uuid from tmp_hzj_pltdft group by uuid HAVING(count(*) > 1)
delete from tmp_hzj_pltdft where uuid = 'b21cde66-d0b9-432e-81aa-a76801369ee7'

select * from tmp_hzj_pltdft where uuid = 'b21cde66-d0b9-432e-81aa-a76801369ee7'


INSERT INTO tmp_hzj_pltdft (`uuid`, `id`, `trial_request`, `trial_reply`, `plt_claim`, `dft_rep`, `crs_exm`, `judge_type`) VALUES ('b21cde66-d0b9-432e-81aa-a76801369ee7', '1876055', '公诉机关指控：2017年1月2日22时18分许，被告人胡俊豪饮酒后驾驶鄂Ｆ×××××号小型面包车沿福银高速由东向西行驶至福银向1295KM+400M附近时发生道路交通事故，胡俊豪受伤，造成伤人交通事故后被民警查获。经湖北省公安厅高警总队四支队十堰市大队认定，胡俊豪负此次事故全部责任。经湖北医药学院法医司法鉴定所法医毒物检验鉴定，在胡俊豪的血液中检出乙醇成份含量为236mg/100ml，为醉酒驾驶机动车。', '', '公诉机关指控：2017年1月2日22时18分许，被告人胡俊豪饮酒后驾驶鄂Ｆ×××××号小型面包车沿福银高速由东向西行驶至福银向1295KM+400M附近时发生道路交通事故，胡俊豪受伤，造成伤人交通事故后被民警查获经湖北省公安厅高警总队四支队十堰市大队认定，胡俊豪负此次事故全部责任经湖北医药学院法医司法鉴定所法医毒物检验鉴定，在胡俊豪的血液中检出乙醇成份含量为236mg/100ml，为醉酒驾驶机动车', '', '', '判决书');




select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'judgment2' and table_schema='laws_doc2' order by COLUMN_NAME

select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'judgment2_etl' and table_schema='laws_doc2' order by COLUMN_NAME

二审：
create table laws_doc2.judgment2_main_etl as select 
id,uuid,court_idea,judge_result,doc_footer,plt_claim,dft_rep,crs_exm,
court,history,reason,type,province,city,if_surrender,if_nosuccess,
if_guity,if_accumulate,if_right,if_team,if_adult,age_year,law_id,reason_uid,
court_uid,org_plaintiff,org_defendant,dispute,casedate from laws_doc2.judgment2_etl


update laws_doc2.judgment2_main_etl a , laws_doc2.judgment2_etl b set 
a.history_title = b.history_title where a.uuid = b.uuid

update laws_doc2.judgment2_main_etl a , laws_doc2.judgment2_etl b set 
a.casedate = b.casedate where a.uuid = b.uuid

update laws_doc2.judgment2_etl a , laws_doc2.tmp_hzj_pltdft b set 
a.plt_claim = b.plt_claim,
a.dft_rep = b.dft_rep,
a.crs_exm = b.crs_exm  where a.uuid = b.uuid


update laws_doc2.judgment2_main_etl a , laws_doc2.tmp_hzj_pltdft b set 
a.plt_claim = b.plt_claim,
a.dft_rep = b.dft_rep,
a.crs_exm = b.crs_exm  where a.uuid = b.uuid

