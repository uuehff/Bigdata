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
FLUSH PRIVILEGES;


创建新用户：
GRANT ALL PRIVILEGES ON *.* TO 'hzj'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'hzj';
FLUSH PRIVILEGES;

查看新用户权限：
SHOW GRANTS FOR 'raolu';
===================================

-- 注意回收权限后，生效时间:
-- 用GRANT、REVOKE或SET PASSWORD对授权表施行的修改会立即被服务器注意到。
-- 如果你手工地修改授权表(使用INSERT、UPDATE等等)，你应该执行一个FLUSH PRIVILEGES语句或运行mysqladmin flush-privileges告诉服务器再装载授权表，否则你的改变将不生效，除非你重启服务器。
-- 当服务器注意到授权表被改变了时，现存的客户连接有如下影响：
-- * 表和列权限在客户的下一次请求时生效。
-- * 数据库权限改变在下一个USE db_name命令生效。
-- 全局权限的改变和口令改变在下一次客户连接时生效。

查看所有用户、权限、回收权限：
SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;
SHOW GRANTS FOR 'liuf';
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'test';
FLUSH PRIVILEGES;


回收权限：(注意，navicat中，权限回收后，需重连下数据库)
REVOKE DROP,SHUTDOWN,PROCESS,GRANT OPTION,CREATE USER ON *.* FROM 'xubin';
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
FLUSH PRIVILEGES;


所有的权限有：
GRANT SELECT, INSERT, UPDATE, DROP, DELETE, CREATE, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, 
ALTER, SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, 
REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, 
TRIGGER, CREATE TABLESPACE ON *.* TO 'liuf'@'%' WITH GRANT OPTION

SHOW GRANTS FOR 'liuf';

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
