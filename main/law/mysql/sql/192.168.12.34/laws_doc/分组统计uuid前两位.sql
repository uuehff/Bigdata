SELECT SUBSTRING(uuid,1,2) u,count(uuid) from judgment_etl group by u order by u 


SELECT SUBSTRING(uuid,1,1) u,count(uuid) from judgment_etl group by u order by u 