create table administration_etl_1w like administration_etl_v2
create table administration_etl_2w like administration_etl_1w

select * from administration_etl_1w where uuid like "%-%"