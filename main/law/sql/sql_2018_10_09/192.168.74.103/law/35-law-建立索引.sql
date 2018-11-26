GRANT ALL PRIVILEGES ON *.* TO 'lifeng'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
FLUSH PRIVILEGES;


alter table tb_doc add unique index union_index(casedate,title,caseid);
alter table judgment add index doc_from(doc_from);
ALTER TABLE  judgment_etl ADD INDEX law_office(law_office), ADD INDEX province(province), ADD INDEX court_cate(court_cate), ADD INDEX court_new(court_new); 

alter table criminal_case add unique index criminal_case_title_court_caseid_key(title,court,caseid);

criminal_case_title_court_caseid_key (title, court, caseid)


SELECT casedate,court_new, LENGTH(casedate),CHAR_LENGTH(casedate),LENGTH(court_new),CHAR_LENGTH(court_new), (LENGTH(casedate)+LENGTH(court_new)) as sums  from judgment_etl where id < 100 order by (LENGTH(casedate)+LENGTH(court_new)) desc 
alter table law_rule_result2 add unique index unique_key(law_id,art_num,publish_data),ADD INDEX title_index(title_short);
