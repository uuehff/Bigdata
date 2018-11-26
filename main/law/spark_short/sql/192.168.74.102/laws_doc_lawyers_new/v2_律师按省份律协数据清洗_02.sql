-- 英文,!:-()+/@空格等都不是特殊符号，可以直接用，空格不区分中英文；
-- 英文特殊字符.|?[]\-
-- .| 直接放在[]之内不转义，或放在[]之外加\\转义，如[a-z0-9A-Z_.|]等价于[a-z0-9A-Z_]|\\.|\\|
-- ?][- 必须放在[]之外加\\转义，如[a-z0-9A-Z_.|()]|\\?|\\]|\\[|\\-|\\-
-- \字符匹配，必须放在[]之内加\转义，使用[\\]进行匹配，不能放在[]之外匹配，如[a-z0-9A-Z_|\\]
-- 
-- 
-- ""双引号匹配,引号放在[]的最后,如'[a-z0-9A-Z()"]'
-- 或者放[]之外使用\\转义：如'[a-z0-9A-Z()]|\\"'
-- 
-- ''单引号匹配，放在[]之内，使用\转义，如'[a-z0-9A-Z()\\|"\']'
-- 或放[]之外使用\\\转义：如'[a-z0-9A-Z()\\|"]|\\\''
-- 
-- 单引号、双引号的匹配，取决于正则表达式字符串使用单还是双引号，如果使用双引号，
-- 则上面单双引号的匹配规则相反。
-- 
-- 注意：\\在[]中不能放在.|?字符之前以及[]中的最前或最后（紧挨着[]号）,否则会报错（可能\\会转义后面的字符，然后报错），
-- 最好放在[]中的()之前，
-- 
-- 匹配英文字符a-z0-9A-Z ,:-\()+!/.|"'@?[]等的正则为：
-- REGEXP '[a-z0-9A-Z 	,:;\\()+!/.|"\'@]|\\?|\\]|\\[|\\-';
-- -- SELECT org_name from hht_lawyer_anhui where org_name REGEXP '[a-z0-9A-Z 	,:;\\().|"\']|\\?|\\]|\\[|\\-';
-- 
-- 注意：^只有在[]中才是取反，取反[]内的任意一个字符，就是除了[]中的字符，否则都是以字符开头的意思；
-- 
-- 汉字、中文字符，。、：；？（）！‘’等不能直接使用[]匹配，需使用hex()函数将原中文字段转为16进制，
-- 也就是python中的str类型，再进行比较:比如冒号：16进制为'\xef\xbc\x9a'，需要使用'efbc9a'进行匹配！
-- ，。、：；？（）！对应16进制为：
-- \xef\xbc\x8c\xe3\x80\x82\xe3\x80\x81\xef\xbc\x9a\xef\xbc\x9b\xef\xbc\x9f\xef\xbc\x88\xef\xbc\x89\xef\xbc\x81\xe2\x80\x98\xe2\x80\x99
-- 去掉\x,匹配规则为：
-- hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc88|efbc89|efbc81|e28098|e28099';
-- utf8编码汉字匹配：hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';


甘肃处理流程：
1、先统计、删除空执业证、去重；：pra_number、name、org_name三个字段；
delete from hht_lawyer_gansu where pra_number = "" or pra_number is null;
delete from hht_lawyer_gansu where name = "" or name is null;
delete from hht_lawyer_gansu where org_name = "" or org_name is null;


select min(id) from hht_lawyer_gansu group by pra_number having(count(*) > 1) 
select * from hht_lawyer_gansu where pra_number in (
select pra_number from hht_lawyer_gansu group by pra_number having(count(*) > 1)) order by pra_number


删除重复数据：甘肃数据执业证号重复67条，且重复数据其他字段不一样，先不删除；
处理三字段后，与30万按三字段匹配，按执业证号不匹配的，再删除掉重复的！


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_gansu where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_gansu where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_gansu set name = replace(name," ","")
update hht_lawyer_gansu set name = replace(name,"?","")
3）org_name：
SELECT * from hht_lawyer_gansu where org_name REGEXP '[a-z0-9A-Z 	,:;\\()+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_gansu set org_name = replace(org_name,"（","(");
update hht_lawyer_gansu set org_name = replace(org_name,"）",")");


2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_gansu_match as
select a.* from hht_lawyer_gansu a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name


去重：过滤所有字段（除id字段外）值都一样的数据；
select * from hht_lawyer_gansu_match where pra_number in (
select pra_number from hht_lawyer_gansu_match group by name,org_name,area_code,gender,pra_number,qua_number,phone having(count(*) > 1)) order by pra_number


delete from hht_lawyer_gansu_match where id in (
select a.id from (
select min(id) as id from hht_lawyer_gansu_match a group by name,org_name,area_code,gender,pra_number,qua_number,phone having(count(*) > 1)
) as a
)

去重：过滤pra_number,name,org_name一样，但phone为空的数据，进行删除；
select * from hht_lawyer_gansu_match where phone = "" and pra_number in (
select pra_number from hht_lawyer_gansu_match group by pra_number having(count(*) > 1)) order by pra_number

delete from hht_lawyer_gansu_match where phone = "" and pra_number in (
select a.pra_number from (
select pra_number from hht_lawyer_gansu_match a group by pra_number having(count(*) > 1) ) as a
)

过滤新增数据：
create table hht_lawyer_gansu_add as 
select * from hht_lawyer_gansu where pra_number not in (
select a.pra_number from hht_lawyer_gansu a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：过滤所有字段（除id字段外）值都一样的数据，删除重复的；
select * from hht_lawyer_gansu_add where pra_number in (
select pra_number from hht_lawyer_gansu_add group by name,org_name,area_code,gender,pra_number,qua_number,phone having(count(*) > 1)) order by pra_number

delete from hht_lawyer_gansu_add where id in (
select a.id from (
select min(id) as id from hht_lawyer_gansu_add a group by name,org_name,area_code,gender,pra_number,qua_number,phone having(count(*) > 1)
) as a
)

新增去重：上面的去重步骤处理之后，过滤pra_number重复的，直接删除，因为不知道哪条才是真确的；
select * from hht_lawyer_gansu_add where  pra_number in (
select pra_number from hht_lawyer_gansu_add group by pra_number having(count(*) > 1)) order by pra_number

delete from hht_lawyer_gansu_add where pra_number in (
select a.pra_number from (
select pra_number from hht_lawyer_gansu_add a group by pra_number having(count(*) > 1) ) as a
)


海南数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；
delete from hht_lawyer_hainan where pra_number = "" or pra_number is null;
delete from hht_lawyer_hainan where name = "" or name is null;
delete from hht_lawyer_hainan where org_name = "" or org_name is null;

select min(id) from hht_lawyer_hainan group by pra_number having(count(*) > 1) 
没有重复数据；


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hainan where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_hainan set pra_number = replace(pra_number,"'","")
2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hainan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

3）org_name：
SELECT * from hht_lawyer_hainan where org_name REGEXP '[a-z0-9A-Z 	,:;\\()+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_hainan set org_name = replace(org_name,"（","(");
update hht_lawyer_hainan set org_name = replace(org_name,"）",")");


2、然后进行关联；
create table hht_lawyer_hainan_match as
select a.* from hht_lawyer_hainan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name


新增数据：
create table hht_lawyer_hainan_add as 
select * from hht_lawyer_hainan where pra_number not in (
select a.pra_number from hht_lawyer_hainan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 



河北数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；
delete from hht_lawyer_hebei where pra_number = "" or pra_number is null;
delete from hht_lawyer_hebei where name = "" or name is null;
delete from hht_lawyer_hebei where org_name = "" or org_name is null;

select min(id) from hht_lawyer_hebei group by pra_number having(count(*) > 1) 

select * from hht_lawyer_hebei where pra_number in (
select pra_number from hht_lawyer_hebei group by pra_number having(count(*) > 1)) order by pra_number

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hebei where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_hebei set pra_number = replace(pra_number,"'","");
update hht_lawyer_hebei set pra_number = replace(pra_number,"。","");
update hht_lawyer_hebei set pra_number = replace(pra_number,"|","");
update hht_lawyer_hebei set pra_number = replace(pra_number,'"',"");
update hht_lawyer_hebei set pra_number = replace(pra_number,'’',"");
update hht_lawyer_hebei set pra_number = replace(pra_number,'l',"1");
2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hebei where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_hebei set name = replace(name," ","");

3）org_name：
SELECT * from hht_lawyer_hebei where org_name REGEXP '[a-z0-9A-Z 	,:;\\()+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_hebei set org_name = replace(org_name,"（","(");
update hht_lawyer_hebei set org_name = replace(org_name,"）",")");
update hht_lawyer_hebei set org_name = replace(org_name," ","");


2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_hebei_match as
select a.* from hht_lawyer_hebei a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name


去重：过滤所有字段（除id字段外）值都一样的数据；
select * from hht_lawyer_hebei_match where pra_number in (
select pra_number from hht_lawyer_hebei_match group by name,org_name,pra_number,phone having(count(*) > 1)) order by pra_number

执行多次，直至结果为0；
delete from hht_lawyer_hebei_match where id in (
select a.id from (
select min(id) as id from hht_lawyer_hebei_match a group by name,org_name,pra_number,phone having(count(*) > 1)
) as a
)

去重：过滤pra_number,name,org_name一样，但phone为空的数据，进行删除；
select * from hht_lawyer_hebei_match where phone = "" and pra_number in (
select pra_number from hht_lawyer_hebei_match group by pra_number having(count(*) > 1)) order by pra_number


delete from hht_lawyer_hebei_match where phone = "" and pra_number in (
select a.pra_number from (
select pra_number from hht_lawyer_hebei_match a group by pra_number having(count(*) > 1) ) as a
)

过滤新增数据：
create table hht_lawyer_hebei_add as 
select * from hht_lawyer_hebei where pra_number not in (
select a.pra_number from hht_lawyer_hebei a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：过滤所有字段（除id字段外）值都一样的数据，删除重复的；
select * from hht_lawyer_hebei_add where pra_number in (
select pra_number from hht_lawyer_hebei_add group by name,org_name,pra_number,phone having(count(*) > 1)) order by pra_number

delete from hht_lawyer_hebei_add where id in (
select a.id from (
select min(id) as id from hht_lawyer_hebei_add a group by name,org_name,pra_number,phone having(count(*) > 1)
) as a
)

新增去重：上面的去重步骤处理之后，过滤pra_number重复的，直接删除，因为不知道哪条才是真确的；
select * from hht_lawyer_hebei_add where  pra_number in (
select pra_number from hht_lawyer_hebei_add group by pra_number having(count(*) > 1)) order by pra_number

delete from hht_lawyer_hebei_add where pra_number in (
select a.pra_number from (
select pra_number from hht_lawyer_hebei_add a group by pra_number having(count(*) > 1) ) as a
)


湖北数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；
select * from hht_lawyer_hubei where org_name != org_name_lately; 
结果为空，说明org_name与org_name_lately一样，因此删除org_name_lately；

delete from hht_lawyer_hubei where pra_number = "" or pra_number is null;
delete from hht_lawyer_hubei where name = "" or name is null;
delete from hht_lawyer_hubei where org_name = "" or org_name is null;

select min(id) from hht_lawyer_hubei group by pra_number having(count(*) > 1) 
没有重复数据；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hubei where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hubei where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

name中包含"/"且"/"对应的是一个字，因此需要删除；
delete from  hht_lawyer_hubei where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


3）org_name：
SELECT * from hht_lawyer_hubei where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_hubei set org_name = replace(org_name,"（","(");
update hht_lawyer_hubei set org_name = replace(org_name,"）",")");

org_name中包含"/"且"/"对应的是一个字，因此需要删除；
delete from  hht_lawyer_hubei where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_hubei_match as
select a.* from hht_lawyer_hubei a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

上面已经统计过，执业证号没有重复的数据；

过滤新增数据：
create table hht_lawyer_hubei_add as 
select * from hht_lawyer_hubei where pra_number not in (
select a.pra_number from hht_lawyer_hubei a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 



湖南数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_hunan where pra_number = "" or pra_number is null;
delete from hht_lawyer_hunan where name = "" or name is null;
delete from hht_lawyer_hunan where org_name = "" or org_name is null;

select min(id) from hht_lawyer_hunan group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_hunan where pra_number in (
-- select pra_number from hht_lawyer_hunan group by pra_number having(count(*) > 1)) order by pra_number

有重复数据,字段都不同，与法网匹配之后再去重；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hunan where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_hunan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update  hht_lawyer_hunan set name = "刘刚" where name = "刘刚（湘楚）";


3）org_name：

update hht_lawyer_hunan set org_name = replace(org_name,"（","(");
update hht_lawyer_hunan set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_hunan where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_hunan_match as
select a.* from hht_lawyer_hunan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select min(id) from hht_lawyer_hunan_match group by pra_number having(count(*) > 1) 
无结果，无重复数据；

过滤新增数据：
create table hht_lawyer_hunan_add as 
select * from hht_lawyer_hunan where pra_number not in (
select a.pra_number from hht_lawyer_hunan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：字段都不一样，因此直接删除，因为不知道哪条才是真确的；
select * from hht_lawyer_hunan_add where  pra_number in (
select pra_number from hht_lawyer_hunan_add group by pra_number having(count(*) > 1)) order by pra_number

delete from hht_lawyer_hunan_add where pra_number in (
select a.pra_number from (
select pra_number from hht_lawyer_hunan_add a group by pra_number having(count(*) > 1) ) as a
)


江苏数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_jiangsu where pra_number = "" or pra_number is null;
delete from hht_lawyer_jiangsu where name = "" or name is null;
delete from hht_lawyer_jiangsu where org_name = "" or org_name is null;

select min(id) from hht_lawyer_jiangsu group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_hunan where pra_number in (
-- select pra_number from hht_lawyer_hunan group by pra_number having(count(*) > 1)) order by pra_number

有重复数据,字段都不同，与法网匹配之后再去重；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_jiangsu where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_jiangsu where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_jiangsu set name = replace(name," ","");

3）org_name：

update hht_lawyer_jiangsu set org_name = replace(org_name,"（","(");
update hht_lawyer_jiangsu set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_jiangsu where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_jiangsu_match as
select a.* from hht_lawyer_jiangsu a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

去重：
select * from hht_lawyer_jiangsu_match where  pra_number in 
(select pra_number from hht_lawyer_jiangsu_match group by pra_number having(count(*) > 1)) order by pra_number

重复数据只有一条，且字段基本都一样；
delete from hht_lawyer_jiangsu_match where id in (
select a.id from (
select min(id) as id from hht_lawyer_jiangsu_match a group by pra_number having(count(*) > 1)
) as a
)


过滤新增数据：
create table hht_lawyer_jiangsu_add as 
select * from hht_lawyer_jiangsu where pra_number not in (
select a.pra_number from hht_lawyer_jiangsu a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：
select * from hht_lawyer_jiangsu_add where  pra_number in 
(select pra_number from hht_lawyer_jiangsu_add group by pra_number having(count(*) > 1)) order by pra_number
没结果，没有重复数据；


江西数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_jiangxi where pra_number = "" or pra_number is null;
delete from hht_lawyer_jiangxi where name = "" or name is null;
delete from hht_lawyer_jiangxi where org_name = "" or org_name is null;

select min(id) from hht_lawyer_jiangxi group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_jiangxi where pra_number in (
-- select pra_number from hht_lawyer_jiangxi group by pra_number having(count(*) > 1)) order by pra_number
-- 
有重复数据,字段都不同，与法网匹配之后再去重；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_jiangxi where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_jiangxi set pra_number = replace(pra_number," ","");
delete from hht_lawyer_jiangxi where pra_number = "NULL"

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_jiangxi where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_jiangxi set name = replace(name," ","");

3）org_name：

update hht_lawyer_jiangxi set org_name = replace(org_name,"（","(");
update hht_lawyer_jiangxi set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_jiangxi where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_jiangxi_match as
select a.* from hht_lawyer_jiangxi a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

去重：
select * from hht_lawyer_jiangxi_match where  pra_number in 
(select pra_number from hht_lawyer_jiangxi_match group by pra_number having(count(*) > 1)) order by pra_number

重复数据只有6条，且字段基本都一样；
delete from hht_lawyer_jiangxi_match where id in (
select a.id from (
select min(id) as id from hht_lawyer_jiangxi_match a group by pra_number having(count(*) > 1)
) as a
)

过滤新增数据：
create table hht_lawyer_jiangxi_add as 
select * from hht_lawyer_jiangxi where pra_number not in (
select a.pra_number from hht_lawyer_jiangxi a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：
select * from hht_lawyer_jiangxi_add where  pra_number in 
(select pra_number from hht_lawyer_jiangxi_add group by pra_number having(count(*) > 1)) order by pra_number
没结果，没有重复数据；


宁夏数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_ningxia where pra_number = "" or pra_number is null;
delete from hht_lawyer_ningxia where name = "" or name is null;
delete from hht_lawyer_ningxia where org_name = "" or org_name is null;

select min(id) from hht_lawyer_ningxia group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_ningxia where pra_number in 
-- (select pra_number from hht_lawyer_ningxia group by pra_number having(count(*) > 1)) order by pra_number

有重复数据,字段都不同，与法网匹配之后再去重；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_ningxia where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_ningxia set pra_number = replace(pra_number,"'","");
update hht_lawyer_ningxia set pra_number = replace(pra_number,",","");
update hht_lawyer_ningxia set pra_number = replace(pra_number,"，","");
update hht_lawyer_ningxia set pra_number = replace(pra_number," ","");
update hht_lawyer_ningxia set pra_number = replace(pra_number,"‘","");
update hht_lawyer_ningxia set pra_number = "16401201211626805" where pra_number = "16401201211626805xl";
update hht_lawyer_ningxia set pra_number = "29041705210199" where pra_number = "29041705210199（实习证）";


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_ningxia where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_ningxia set name = replace(name," ","");

3）org_name：

update hht_lawyer_ningxia set org_name = replace(org_name,"（","(");
update hht_lawyer_ningxia set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_ningxia where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_ningxia_match as
select a.* from hht_lawyer_ningxia a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

去重：
select * from hht_lawyer_ningxia_match where  pra_number in 
(select pra_number from hht_lawyer_ningxia_match group by pra_number having(count(*) > 1)) order by pra_number

没有重复数据；

过滤新增数据：
create table hht_lawyer_ningxia_add as 
select * from hht_lawyer_ningxia where pra_number not in (
select a.pra_number from hht_lawyer_ningxia a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：
select * from hht_lawyer_ningxia_add where  pra_number in 
(select pra_number from hht_lawyer_ningxia_add group by pra_number having(count(*) > 1)) order by pra_number
没结果，没有重复数据；


山东数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_shandong where pra_number = "" or pra_number is null;
delete from hht_lawyer_shandong where name = "" or name is null;
delete from hht_lawyer_shandong where org_name = "" or org_name is null;

select min(id) from hht_lawyer_shandong group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_shandong where pra_number in 
-- (select pra_number from hht_lawyer_shandong group by pra_number having(count(*) > 1)) order by pra_number

有重复数据,字段都不同，与法网匹配之后再去重；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_shandong where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_shandong where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_shandong set name = replace(name,"郭恩ue863","郭恩");
update hht_lawyer_shandong set name = replace(name,"韩晓峰37370622197103","韩晓峰");

3）org_name：

update hht_lawyer_shandong set org_name = replace(org_name,"（","(");
update hht_lawyer_shandong set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_shandong where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_shandong set org_name = replace(org_name," ","");

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_shandong_match as
select a.* from hht_lawyer_shandong a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

去重：
select * from hht_lawyer_shandong_match where  pra_number in 
(select pra_number from hht_lawyer_shandong_match group by pra_number having(count(*) > 1)) order by pra_number

两条重复数据：

delete from hht_lawyer_shandong_match where id = 16462
delete from hht_lawyer_shandong_match where id = 19181


过滤新增数据：
create table hht_lawyer_shandong_add as 
select * from hht_lawyer_shandong where pra_number not in (
select a.pra_number from hht_lawyer_shandong a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

新增去重：
select * from hht_lawyer_shandong_add where  pra_number in 
(select pra_number from hht_lawyer_shandong_add group by pra_number having(count(*) > 1)) order by pra_number

delete from hht_lawyer_shandong_add where pra_number in 
(select pra_number from hht_lawyer_shandong_add group by pra_number having(count(*) > 1)) order by pra_number

没结果，没有重复数据；

==========================================================
浙江数据处理流程：

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_zhejiang where pra_number = "" or pra_number is null;
delete from hht_lawyer_zhejiang where name = "" or name is null;
delete from hht_lawyer_zhejiang where org_name = "" or org_name is null;

select min(id) from hht_lawyer_zhejiang group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_shandong where pra_number in 
-- (select pra_number from hht_lawyer_shandong group by pra_number having(count(*) > 1)) order by pra_number

没有重复数据；

1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_zhejiang where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_zhejiang where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

无结果；

3）org_name：

update hht_lawyer_zhejiang set org_name = replace(org_name,"（","(");
update hht_lawyer_zhejiang set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_zhejiang where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_zhejiang_match as
select a.* from hht_lawyer_zhejiang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name


过滤新增数据：
create table hht_lawyer_zhejiang_add as 
select * from hht_lawyer_zhejiang where pra_number not in (
select a.pra_number from hht_lawyer_zhejiang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 



