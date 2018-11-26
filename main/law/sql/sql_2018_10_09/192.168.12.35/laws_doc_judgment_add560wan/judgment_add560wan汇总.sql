create table judgment_add560wan_etl01 like judgment_add560wan_etl

select reason_type,judge_type,type,count(*) from judgment_civil_all group by reason_type,judge_type,type