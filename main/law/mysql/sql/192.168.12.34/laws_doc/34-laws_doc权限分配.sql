查看binlog-format格式：

show variables like 'BINLOG_FORMAT';
SHOW GLOBAL variables like "BINLOG_FORMAT";

修改binlog-format，编辑my.cnf:
log-bin=mysql-bin 
binlog-format=ROW 
server_id=1

注意：修改字段名称，立刻生效，不用耗时去倒腾表数据。
alter table test rename test1; --修改表名
alter table test add  column name varchar(10); --添加表列
alter table test drop  column name; --删除表列
alter table test modify address char(10) --修改表列类型
或者：	alter table test change address address  char(40)
alter table test change column address address1 varchar(30)--修改表列名

alter table judgment_etl add  column name varchar(10); --添加表列
alter table tmp_wxy change column update_flag type varchar(2);

alter table judgment_etl modify law_id text;



alter table judgment_etl add column lawlist text;

CREATE TABLE judgment SELECT * from tb_doc where 1 = 2 

SHOW INDEX from adjudication
SHOW INDEX from tb_doc
判决：judgment
	裁定：adjudication
	其他：other
	通知；inform
	决定：decision
	调解：mediate
alter table mediate add unique index union_index(casedate,title,caseid);
alter table mediate add unique index uuid(uuid);
SHOW INDEX from civil.adjudication

同时添加多个字段和索引：
alter table judgment_etl 
add court_uid varchar(255),
add reason_uid varchar(255),
add law_id varchar(255),
add reason varchar(255),
add history text,
add unique index uuid(uuid),
add index court(court);



alter table judgment_etl 
add province varchar(255),
add city varchar(255),
add court_cate varchar(10),
drop judge_chief_origin2,
drop history_origin;


alter table judgment_etl add type varchar(2);


alter table party_info_result_ids add id int auto_increment primary key;

alter table uuid_court_history add id int auto_increment primary key;
alter table judgment_civil_56w add id int auto_increment primary key;
alter table judgment_civil_56w add primary key (id);

ALTER TABLE  add unique index uuid(uuid), ADD INDEX court(court);


创建新用户：
GRANT ALL PRIVILEGES ON laws.* TO 'u01'@'%' IDENTIFIED BY 'u01@13322.com' WITH GRANT OPTION;
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'u01';
FLUSH PRIVILEGES;

查看新用户权限：
SHOW GRANTS FOR 'tzp';
===================================

GRANT ALL PRIVILEGES ON *.* TO 'xubin'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'liuf'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'wxy'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'hzj'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'raolu'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'xwx'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'zipeng'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'lifeng'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'guoliang'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'weiwc'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'tzp'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'caitinggui'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'HHly2017.' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'weiwc'@'%' IDENTIFIED BY 'HHly2017.' WITH GRANT OPTION;


GRANT ALL PRIVILEGES ON laws_doc_v2.* TO 'raolu'@'%' IDENTIFIED BY 'raolu123' WITH GRANT OPTION;

FLUSH PRIVILEGES;

注意回收权限后，生效时间:
用GRANT、REVOKE或SET PASSWORD对授权表施行的修改会立即被服务器注意到。
如果你手工地修改授权表(使用INSERT、UPDATE等等)，你应该执行一个FLUSH PRIVILEGES语句或运行mysqladmin flush-privileges告诉服务器再装载授权表，否则你的改变将不生效，除非你重启服务器。
当服务器注意到授权表被改变了时，现存的客户连接有如下影响：
* 表和列权限在客户的下一次请求时生效。
* 数据库权限改变在下一个USE db_name命令生效。
全局权限的改变和口令改变在下一次客户连接时生效。

回收权限：(注意，navicat中，权限回收后，需重连下数据库)
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'liuf';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'wxy';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'hzj';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'raolu';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'xwx';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'zipeng';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'lifeng';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'guoliang';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'tzp';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'caitinggui';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'xubin';
FLUSH PRIVILEGES;


所有的权限有：
GRANT SELECT, INSERT, UPDATE, DROP, DELETE, CREATE, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, 
ALTER, SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, 
REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, 
TRIGGER, CREATE TABLESPACE ON *.* TO 'liuf'@'%' WITH GRANT OPTION

SHOW GRANTS FOR 'xwx';

mysql权限级别分为全局权限（包括所有库及库下的表）、库权限（包括该库下的表）、表权限（只包括具体的一个表），
对应于mysql库里面的user表、db表、tables_priv表。
grant all privileges on *.*  :操作mysql.user表
grant all privileges on db.*  :操作mysql.db表
grant all privileges on db.table :操作mysql.tables_priv表

这三种操作分别对应不同的表，互不影响，赋予一个用户大粒度的权限，并不能收回小粒度的权限。

SELECT * from mysql.user
SELECT * from mysql.db
SELECT * from  mysql.tables_priv

因此权限赋予和权限回收是对应的，以什么级别赋权，就只能以什么级别回收权限，即：只能ON *.*, ON db.*, ON db.table,

查看所有用户、权限、回收权限：
SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;

SHOW GRANTS FOR 'liuf';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'test';
FLUSH PRIVILEGES;

修改表名：
rename table MyClass to YouClass;
注意：当你执行 RENAME 时，你不能有任何锁定的表或活动的事务。你同样也必须有对原初表的 ALTER 和 DROP 权限，
以及对新表的 CREATE 和 INSERT 权限。

rename过程：
1.lock table a
2.create table b （同结构）
3.insert into b select * from a
4.unlock and drop table a
这个过程.应该没有真实使用insert导出导入，而是直接修改.frm文件。





数据库/数据表/数据列权限：
Drop: 删除数据表或数据库。
Alter: 修改已存在的数据表(例如增加/删除列)和索引。
Delete: 删除表的记录。
INDEX: 建立或删除索引。
Insert: 增加表的记录。
Update: 修改表中已存在的记录。
Create: 建立新的数据库或数据表。
Select: 显示/搜索表的记录。

全局管理MySQL用户权限：
file: 在MySQL服务器上读写文件。
PROCESS: 显示或杀死属于其它用户的服务线程。
RELOAD: 重载访问控制表，刷新日志等。
SHUTDOWN: 关闭MySQL服务。

特别的权限：
ALL: 允许做任何事(和root一样)。
USAGE: 只允许登录--其它什么也不允许做。
=======================================================

alter table judgment add index doc_from(doc_from);

SELECT COUNT(*) from tb_court;

INSERT  into tmp_weiwenchao2(id,uuid,type,casedate) SELECT id,uuid,type,casedate from judgment where id > 1800000

DELETE from tmp_weiwenchao2 WHERE 1 = 1 

SELECT *  from tmp_weiwenchao where id  < 1800000 and  lawlist_1r = '0' and lawlist

SELECT * from  where id > 1876050 and id < 1876080
SELECT * from tmp_weiwenchao where id > 2127296 and id < 2127400


gender,nation,edu,crml_team,j_adult,prvs,crime_reason,law_office,province,court_cate,court_new

select * from information_schema.innodb_trx


ALTER TABLE  judgment_etl ADD INDEX law_office(law_office), ADD INDEX province(province), ADD INDEX court_cate(court_cate), ADD INDEX court_new(court_new); 

select tmp_wxy.uuid,tmp_raolu.uuid,judgment.uuid,court_new,duration,casedate_new,law_office,court_cate,reason,fact_finder from tmp_wxy,tmp_raolu,judgment where tmp_wxy.id=tmp_raolu.id and tmp_wxy.id=judgment.id and judgment.id = 10000 

SELECT COUNT(*) from tmp_wxy where id <= 1000

select court_new,duration,casedate_new,law_office,court_cate,reason,fact_finder from tmp_wxy,tmp_raolu,judgment where tmp_wxy.id=tmp_raolu.id and tmp_wxy.id=judgment.id 

SELECT law_office,COUNT(*) from tmp_raolu where id <= 10000 GROUP BY law_office;

select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_weiwenchao2' and table_schema='laws_doc'
