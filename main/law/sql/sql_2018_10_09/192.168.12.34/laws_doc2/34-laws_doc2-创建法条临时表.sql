CREATE table judgment2_etl_lawlist as SELECT a.id,a.uuid,b.lawlist,a.casedate from judgment2 a,tmp_weiwenchao b where a.uuid = b.uuid


SELECT id,province,city,district,court,court_cate from tmp_raolu where id < 100;


GRANT ALL PRIVILEGES ON *.* TO 'caitinggui'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'HHly2017.' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'test2'@'%' IDENTIFIED BY 'test2' WITH GRANT OPTION;


FLUSH PRIVILEGES;


GRANT ALL PRIVILEGES ON *.* TO 'test2'@'%'

mysql权限级别分为全局权限（包括所有库及库下的表）、库权限（包括该库下的表）、表权限（只包括具体的一个表），
对应于mysql库里面的user表、db表、tables_priv表。

grant all privileges on *.*  :操作mysql.user表
grant all privileges on db.*  :操作mysql.db表
grant all privileges on db.table :操作mysql.tables_priv表

这三种操作分别对应不同的表，互不影响，赋予一个用户大粒度的权限，并不能收回小粒度的权限。

SELECT * from mysql.user
SELECT * from mysql.db
SELECT * from  mysql.tables_priv


查看所有用户：
SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;

查看权限
SHOW GRANTS FOR 'liuf';

--回收改表、删表权限
REVOKE DROP,Alter,Delete,INDEX,Insert,Update ON laws_doc.test FROM 'test2';
CREATE TABLE test like tmp2_wxy;



REVOKE DROP ON *.* FROM 'liuf';
FLUSH PRIVILEGES;

--回收表记录的增删改权限
REVOKE INSERT ON newythdb.* FROM 'zplat_cen1';
REVOKE UPDATE ON newythdb.* FROM 'zplat_cen1';
REVOKE DELETE ON newythdb.* FROM 'zplat_cen1';

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
