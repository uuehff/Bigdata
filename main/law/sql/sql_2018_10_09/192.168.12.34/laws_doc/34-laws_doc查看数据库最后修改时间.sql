-- 查看表的最后mysql修改时间 
-- select TABLE_NAME,UPDATE_TIME from information_schema.TABLES where TABLE_SCHEMA=’数据库名’ order by UPDATE_TIME desc limit 1; 
-- select TABLE_NAME,UPDATE_TIME from information_schema.TABLES where TABLE_SCHEMA=’数据库名’ and information_schema.TABLES.TABLE_NAME = ‘表名’;

select * from information_schema.TABLES where TABLE_SCHEMA='laws_doc' order by UPDATE_TIME desc limit 10; 
select TABLE_NAME,UPDATE_TIME from information_schema.TABLES where TABLE_SCHEMA='laws_doc' and information_schema.TABLES.TABLE_NAME = 'judgment_etl';
