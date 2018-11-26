
select * from lawyer_info_new where pra_number = "14401200410457998"

select name ,count(*) from hht_lawyer_12348gov_v3 
group by name,SUBSTR(pra_number,6,4),SUBSTR(pra_number,11,1) having(count(*) > 1) 
order by count(*) desc

select * from hht_lawyer_12348gov_v3 where name = "李春燕" order by pra_number

select pra_number from hht_lawyer_12348gov where CHAR_LENGTH(pra_number) != 17 order by pra_number

select *
from information_schema.tables 
where table_schema in 
(select schema_name from information_schema.SCHEMATA  
where schema_name like "laws_doc_%" and schema_name != "laws_doc2" 
and schema_name not like "laws_doc_lawyers%" and schema_name != "laws_doc_mediate"
)
and (table_name like "%_field" or table_name like "%_lawyer" or table_name like "%_organization" ) 
order by right(table_name,1)


-- select * 
-- from information_schema.tables 
-- where table_schema = "laws_doc_zhangye_v2" and (table_name like "%_field" or table_name like "%_lawyer" or table_name like "%_organization")

create table lawyers_table as 
select table_name 
from information_schema.tables 
where table_schema = "laws_doc_lawyers_new" and 
table_name like "hht_lawyer%" 
and table_name not like "%_add" 
and table_name not like "%_match"
and table_name not like "hht_lawyer_12348gov%"
and table_name not like "hht_lawyer_v2"


hht_lawyer_bingtuan
hht_lawyer_guangxi
hht_lawyer_guizhou
hht_lawyer_henan
hht_lawyer_liaoning
hht_lawyer_qinghai
hht_lawyer_shanxi
hht_lawyer_sichuan
hht_lawyer_tianjin
hht_lawyer_xinjiang
hht_lawyer_xizang
hht_lawyer_yunnan
hht_lawyer_gds_gdlawyer
hht_lawyer_heilongjiang

