select * from court where name is null or name = ""

update court set 
full_uid = CONCAT(pid,"||",uid) where name is null or name = ""

update court set 
full_uid = uid where (name is null or name = "" ) and pid is null

create table province_city_full_uid as 
select province,city,full_uid from court where name is null or name = ""