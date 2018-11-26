select * from judgment where uuid = "bf3262c4-cb39-4282-8455-a835012d9432"   句号以后被截断，及000切割问题
select * from judgment where uuid = "18983fe0-f5dd-4990-9aa9-a8b300d00360"   满月酒后面内容被截断！
select * from judgment where uuid = "af859d1c-42ad-4ff6-9bab-a81200a1724e"
select * from judgment where uuid = "4611bcbb-f5c2-4970-9ceb-a8a1009cda29"
party_info,trial_process,trial_request,trial_reply,court_find,court_idea,judge_result,doc_footer


select * from judgment_doc where doc_id = "4611bcbb-f5c2-4970-9ceb-a8a1009cda29"


GRANT ALL PRIVILEGES ON *.* TO 'wxy'@'%' IDENTIFIED BY '!@#$%qwert12345' WITH GRANT OPTION;
FLUSH PRIVILEGES;

SHOW GRANTS FOR "root"


select * from judgment where uuid = "bcbace13-7222-4e36-a297-a89d009cc6f6"


select * from judgment where uuid = "74e17a6b-344a-41f5-b7dd-a8cc0010dd09"

select count(*) from judgment where id <= 500000 and is_crawl = 1


无文本数据统计：
select count(*) from judgment where id < 1000000 and left(doc_content,5) != '$(fun' ;
625
select count(*) from judgment where id > 1000000 and id < 2000000 and  left(doc_content,5) != '$(fun' ;
476
select count(*) from judgment where id > 2000000 and id < 3000000 and  left(doc_content,5) != '$(fun' ;
177
select count(*) from judgment where id > 3000000 and id < 4000000 and  left(doc_content,5) != '$(fun' ;
1177
select count(*) from judgment where id > 4000000 and id < 5000000 and  left(doc_content,5) != '$(fun' ;
2961
select count(*) from judgment where id > 5000000 and id < 6000000 and  left(doc_content,5) != '$(fun' ;
2657
select count(*) from judgment where id > 6000000 and  left(doc_content,5) != '$(fun' ;
72

select id,doc_content,left(doc_content,5) from judgment where left(doc_content,5) != '$(fun' limit 100;

select id,doc_content from judgment where id in (8,16,22,27,34)


select id,doc_content from judgment where is_crawl = '2'
select id,doc_content from judgment where is_format = 3 limit 100;


