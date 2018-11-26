create table hht_lawyer_12348gov_v3_missing as 
select a.* from zy_lawyer_12348gov a left join hht_lawyer_12348gov_v3 b 
on a.pra_number = b.pra_number where b.pra_number is null;

select SUBSTR(area,1,2) from hht_lawyer_12348gov_v3_missing group by SUBSTR(area,1,2)
order by SUBSTR(area,1,2)


select a.area,b.area_id,b.province,b.city  from hht_lawyer_12348gov_v3_missing a join area_code_v3 b
on SUBSTR(a.area,1,4) = b.area_id order by SUBSTR(a.area,1,4);

update hht_lawyer_12348gov_v3_missing a join area_code_v3 b
on SUBSTR(a.area,1,4) = b.area_id 
set a.province = b.province,
a.city = b.city ;


select * from hht_lawyer_12348gov_v3_missing where CHAR_LENGTH(pra_number) = 17;
6. “|” 分隔条件匹配指定字符串
SELECT * FROM user WHERE email REGEXP 'qq.com|163.com'
正则表达式可以匹配指定的字符串，字符串之间使用 “|” 分隔。
7. “[]” 表示集合匹配指定字符串中的任意一个
SELECT * FROM user WHERE email REGEXP '[az]'
”[]“ 指定一个集合，以上表示查询邮箱中带有 a或z或两者都有的邮箱。也可以用来匹配数字集合，比如 [0-9] 表示集合区间所有数字，[a-z] 表示集合区间所有字母。
8. “[^]”匹配指定字符以外的字符
SELECT * FROM user WHERE email REGEXP '[^a-d1-3]'
如上匹配邮箱中不包含 a、b、c、d 且 不包含 1、2、3 的记录。
9. 使用{n,} 或 {n,m} 来指定字符串连接出现的次数
SELECT * FROM user WHERE email REGEXP 'b{2}'
表示字母 b 至少出现 2 次。
SELECT * FROM user WHERE email REGEXP 'yu{1,3}'
表示字符串 ba 至少出现1次，至多出现3次。

SELECT name FROM user WHERE NOT (name REGEXP "[u0391-uFFE5]");

select substr(org_name,1,2),count(*) from hht_lawyer_12348gov_v3_missing group by substr(org_name,1,2) order by count(*) desc 

select * from hht_lawyer_12348gov_v3_missing where pra_number REGEXP '[a-z]' and CHAR_LENGTH(pra_number) =17;

select * from hht_lawyer_12348gov_v3_missing where 
pra_number REGEXP '[a-z]' 
and CHAR_LENGTH(pra_number) =17 
and province = "河北省";

select * from hht_lawyer_12348gov_v3_missing a join  where 
pra_number REGEXP '[a-z]' 
and CHAR_LENGTH(pra_number) =17 
and province = "江苏省";


正则：https://www.cnblogs.com/aaronthon/p/8479841.html
https://wenku.baidu.com/view/4f4e211858fb770bf78a5538.html
不像程序中那样使用！

select * from hht_lawyer_12348gov_v3_missing where CHAR_LENGTH(pra_number) < 12;
select * from hht_lawyer_12348gov_v3_missing where pra_number like '%"%' ;
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'"',"") where pra_number like '%"%'  ;
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'。',"")  ;
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'？',"")  ;
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'?',"")  ;
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,' ',"")  ;

select * from hht_lawyer_12348gov_v3_missing where pra_number like '%1611494024'  ;

delete from hht_lawyer_12348gov_v3_missing where id = "293516"
-- ur"[^\u4e00-\u9fa5]"

SELECT pra_number,hex(pra_number) FROM hht_lawyer_12348gov_v3_missing WHERE pra_number = "不详"

SELECT * FROM hht_lawyer_12348gov_v3_missing WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';
SELECT *,pra_number REGEXP '[0-9]' FROM hht_lawyer_12348gov_v3_missing WHERE pra_number REGEXP '^[0-9]+$'
SELECT * FROM hht_lawyer_12348gov_v3_missing WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != ""

update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'陕',"") ;
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'专职',"") ;
update hht_lawyer_12348gov_v3_missing set pra_number = ""  WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';
update hht_lawyer_12348gov_v3_missing set pra_number = ""  WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'-',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,',',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'：',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'’',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'，',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_12348gov_v3_missing set pra_number = replace(pra_number,'‘',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_12348gov_v3_missing set pra_number = "" WHERE pra_number like "%/%";
update hht_lawyer_12348gov_v3_missing set pra_number = "" WHERE pra_number like "%+%";

SELECT * FROM hht_lawyer_12348gov_v3_missing WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';



以这种方式测试正则，返回1匹配，返回0不匹配；
SELECT 'c' REGEXP 'a|b';

select  from hht_lawyer_12348gov_v3 where province = "" or province is null;


delete from hht_lawyer_anhui where pra_number = "" or pra_number is null;

select min(id) from hht_lawyer_anhui group by pra_number having(count(*) > 1) 
select * from hht_lawyer_anhui where  pra_number  =  "11341620161153338800"
select * from hht_lawyer_anhui where  pra_number  =  "120015004458"

select min(id) from hht_lawyer_anhui group by pra_number having(count(*) > 1) 
删除重复数据：执行多次，因为一次只能删除重复中的一条，有的可能重复多次；一直删除到结果为0为止；
delete from hht_lawyer_anhui where id in (
select a.id from (
select min(id) as id from hht_lawyer_anhui a group by pra_number having(count(*) > 1)
) as a
)


SELECT pra_number FROM hht_lawyer_anhui WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';
SELECT *,pra_number REGEXP '[0-9]' FROM hht_lawyer_anhui WHERE pra_number REGEXP '^[0-9]+$'
SELECT pra_number FROM hht_lawyer_anhui WHERE pra_number REGEXP '^[0-9]+$' and CHAR_LENGTH(pra_number) = 17;
SELECT * FROM hht_lawyer_anhui WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "" 


update hht_lawyer_anhui set pra_number = replace(pra_number,'"',"") where pra_number like '%"%'  ;
update hht_lawyer_anhui set pra_number = replace(pra_number,'。',"")  ;
update hht_lawyer_anhui set pra_number = replace(pra_number,'？',"")  ;
update hht_lawyer_anhui set pra_number = replace(pra_number,'?',"")  ;
update hht_lawyer_anhui set pra_number = replace(pra_number,' ',"")  ;


update hht_lawyer_anhui set pra_number = replace(pra_number,'-',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_anhui set pra_number = replace(pra_number,',',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_anhui set pra_number = replace(pra_number,'：',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_anhui set pra_number = replace(pra_number,'’',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_anhui set pra_number = replace(pra_number,'，',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_anhui set pra_number = replace(pra_number,'‘',"") WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "";
update hht_lawyer_anhui set pra_number = "" WHERE pra_number like "%/%";
update hht_lawyer_anhui set pra_number = "" WHERE pra_number like "%+%";

SELECT pra_number FROM hht_lawyer_anhui WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';
delete from hht_lawyer_anhui where hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';

select * from hht_lawyer_12348gov_v4 a join hht_lawyer_anhui b on 
a.pra_number = 

SELECT pra_number FROM hht_lawyer_anhui WHERE hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';
SELECT *,pra_number REGEXP '[0-9]' FROM hht_lawyer_anhui WHERE pra_number REGEXP '^[0-9]+$'
SELECT pra_number FROM hht_lawyer_anhui WHERE pra_number REGEXP '^[0-9]+$' and CHAR_LENGTH(pra_number) = 17;
SELECT * FROM hht_lawyer_anhui WHERE pra_number not REGEXP '^[0-9]+$' and pra_number != "" 

SELECT 'c' REGEXP 'a|b'; 0
SELECT 'b' REGEXP 'ab'; 0







