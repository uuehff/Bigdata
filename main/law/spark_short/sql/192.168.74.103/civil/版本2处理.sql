create table judgment__reason_type_type_judge_type like  judgment;

select id,title,judge_type,doc_content from judgment where 
judge_type != "判决" and judge_type != "裁定" and  
judge_type != "调解" and judge_type != "决定" 
limit 1000