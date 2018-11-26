INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');
INSERT INTo flume_sql(name) VALUES('121');

INSERT INTo flume_sql(name) select uuid from docs_count.administration where id < 500000 and id < 300000;
INSERT INTo flume_sql(name) select uuid from docs_count.administration where id < 100;
COMMIT;

update flume_sql set count = id where id > 369 and id < 390;

INSERT INTo uuid(uuid) select name from flume_sql where id < 10;
INSERT INTo judgment_doc(uuid) select name from flume_sql where id < 5;

create table judgment_doc_filter as 
select * from judgment_doc where exists(select 1 from uuid where uuid = judgment_doc.uuid);

select unix_timestamp('2018-08-22 18:25:59')

create table flume_wenshu_test as select * from flume_wenshu where count < 20;

update flume_wenshu_test set type = NULL where casedate = "2015-03-30";
update flume_wenshu_test set court = NULL where count = 3 ;

create table flume_wenshu_test_result like flume_wenshu_test;

INSERT INTo flume_wenshu_test select * from flume_wenshu where count < 20;
INSERT INTo flume_wenshu_test select * from flume_wenshu where count > 20 and count < 31;
INSERT INTo flume_wenshu_test select * from flume_wenshu where count > 30 and count < 100;
INSERT INTo flume_wenshu_test select * from flume_wenshu where count > 100 and count < 300;
INSERT INTo flume_wenshu_test select * from flume_wenshu where count > 300 and count < 1300;
INSERT INTo flume_wenshu_test select * from flume_wenshu where count > 1300 and count < 4300;
