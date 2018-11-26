update judgment_main_etl a , judgment_etl b set 
a.casedate = b.casedate,
a.if_delay = b.if_delay,
a.age_min = b.age_min,
a.duration = b.duration where a.uuid = b.uuid