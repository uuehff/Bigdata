select province,count(*) from hht_lawyer_12348gov_v4 group by province;
select * from hht_lawyer_12348gov_v4 where city is null;
select * from hht_lawyer_12348gov_v4 where city = "北京市";

update hht_lawyer_12348gov_v4 set city = province where province in (
"北京市","上海市","天津市","重庆市") and city is null;


select * from hht_lawyer_v2 where org_name != org_full or 
org_full like "%||%" ;