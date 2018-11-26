select * from reason where name = "劳动人事纠纷"

查询有多少条重复的数据：
select * from court where name in (select name from court where name is not null and name != "" group by name having(count(*) > 1)) order by name
-- select * from court where id in (select max(id) from court where name is not null and name != "" group by name having(count(*) > 1)) order by name

删除重复中id最大的数据，（可能要执行多次，比如有重复三次的记录）
delete from court where id in (select id from (select max(id) as id from court where name is not null and name != "" group by name having(count(*) > 1)) as t1)


