select * from court_province where id not in (
select id from court_province 
where province like "%广东%" or province like "%北京%" or province like "%上海%" or province like "%福建%" or 
province like "%浙江%" or province like "%江苏%" or province like "%四川%" or province  like "%重庆%" 
or province like "%辽宁%" )

select 
sum(case when law_office like "%云南%" then 1 else 0 end) as "云南",
sum(case when law_office like "%内蒙%" then 1 else 0 end) as "内蒙",
sum(case when law_office like "%吉林%" then 1 else 0 end) as "吉林",
sum(case when law_office like "%天津%" then 1 else 0 end) as "天津",
sum(case when law_office like "%宁夏%" then 1 else 0 end) as "宁夏",
sum(case when law_office like "%安徽%" then 1 else 0 end) as "安徽",
sum(case when law_office like "%山东%" then 1 else 0 end) as "山东",
sum(case when law_office like "%山西%" then 1 else 0 end) as "山西",
sum(case when law_office like "%广西%" then 1 else 0 end) as "广西",
sum(case when law_office like "%新疆%" then 1 else 0 end) as "新疆",
sum(case when law_office like "%江西%" then 1 else 0 end) as "江西",
sum(case when law_office like "%河北%" then 1 else 0 end) as "河北",
sum(case when law_office like "%河南%" then 1 else 0 end) as "河南",
sum(case when law_office like "%海南%" then 1 else 0 end) as "海南",
sum(case when law_office like "%湖北%" then 1 else 0 end) as "湖北",
sum(case when law_office like "%湖南%" then 1 else 0 end) as "湖南",
sum(case when law_office like "%甘肃%" then 1 else 0 end) as "甘肃",
sum(case when law_office like "%西藏%" then 1 else 0 end) as "西藏",
sum(case when law_office like "%贵州%" then 1 else 0 end) as "贵州",
sum(case when law_office like "%陕西%" then 1 else 0 end) as "陕西",
sum(case when law_office like "%青海%" then 1 else 0 end) as "青海",
sum(case when law_office like "%黑龙江%" then 1 else 0 end) as "黑龙江" 
from lawyers ;