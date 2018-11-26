UNION 用于合并两个或多个 SELECT 语句的结果集，并消去表中任何重复行。
UNION 内部的 SELECT 语句必须拥有相同数量的列，列也必须拥有相似的数据类型。
同时，每条 SELECT 语句中的列的顺序必须相同.

SQL UNION 语法：
复制代码 代码如下:
SELECT column_name FROM table1
UNION
SELECT column_name FROM table2

注释：默认地，UNION 操作符选取不同的值。如果允许重复的值，请使用 UNION ALL。
当 ALL 随 UNION 一起使用时（即 UNION ALL），不消除重复行
SQL UNION ALL 语法
复制代码 代码如下:
SELECT column_name FROM table1
UNION ALL
SELECT column_name FROM table2