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
==================================================
hht_lawyer_bingtuan
hht_lawyer_guangxi
hht_lawyer_guizhou
hht_lawyer_henan
hht_lawyer_liaoning
hht_lawyer_qinghai
hht_lawyer_shanxi
hht_lawyer_sichuan
hht_lawyer_tianjin
hht_lawyer_xinjiang
hht_lawyer_xizang
hht_lawyer_yunnan
hht_lawyer_gds_gdlawyer
hht_lawyer_heilongjiang
=================================================
新疆兵团数据处理流程：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_bingtuan where pra_number = "" or pra_number is null;
delete from hht_lawyer_bingtuan where name = "" or name is null;
delete from hht_lawyer_bingtuan where org_name = "" or org_name is null;

select min(id) from hht_lawyer_bingtuan group by pra_number having(count(*) > 1) 

-- select * from hht_lawyer_bingtuan where pra_number in 
-- (select pra_number from hht_lawyer_bingtuan group by pra_number having(count(*) > 1)) order by pra_number


重复数据只有10条，且字段基本都一样,直接去重；
delete from hht_lawyer_bingtuan where id in (
select a.id from (
select max(id) as id from hht_lawyer_bingtuan a group by pra_number having(count(*) > 1)
) as a
)


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_bingtuan where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_bingtuan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_bingtuan set name = replace(name," ","");
无结果；

3）org_name：

update hht_lawyer_bingtuan set org_name = replace(org_name,"（","(");
update hht_lawyer_bingtuan set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_bingtuan where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

经统计，删除律所有问题的数据；
delete from hht_lawyer_bingtuan where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_bingtuan_match as
select a.* from hht_lawyer_bingtuan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name


过滤新增数据：
create table hht_lawyer_bingtuan_add as 
select * from hht_lawyer_bingtuan where pra_number not in (
select a.pra_number from hht_lawyer_bingtuan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 
======================================================================
广西数据处理流程：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_guangxi where pra_number = "" or pra_number is null;
delete from hht_lawyer_guangxi where name = "" or name is null;
delete from hht_lawyer_guangxi where org_name = "" or org_name is null;

select min(id) from hht_lawyer_guangxi group by pra_number having(count(*) > 1) 

select * from hht_lawyer_guangxi where pra_number in 
(select pra_number from hht_lawyer_guangxi group by pra_number,name,org_name having(count(*) > 1)) order by pra_number
该表只有三个主字段，且经统计，pra_number,name,org_name三个字段分组结果和pra_number一个字段分组结果条数一样，
因此基本断定重复数据都是三字段一样的；

去重；
delete from hht_lawyer_guangxi where id in (
select a.id from (
select max(id) as id from hht_lawyer_guangxi a group by pra_number having(count(*) > 1)
) as a
)


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_guangxi where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_guangxi where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_guangxi set name = replace(name," ","");
delete from hht_lawyer_guangxi where id = 80051

3）org_name：

update hht_lawyer_guangxi set org_name = replace(org_name,"（","(");
update hht_lawyer_guangxi set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_guangxi where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_guangxi_match as
select a.* from hht_lawyer_guangxi a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name


过滤新增数据：
create table hht_lawyer_guangxi_add as 
select * from hht_lawyer_guangxi where pra_number not in (
select a.pra_number from hht_lawyer_guangxi a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

==================
贵州数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_guizhou where pra_number = "" or pra_number is null;
delete from hht_lawyer_guizhou where name = "" or name is null;
delete from hht_lawyer_guizhou where org_name = "" or org_name is null;

select min(id) from hht_lawyer_guizhou group by pra_number having(count(*) > 1) 

select * from hht_lawyer_guizhou where pra_number in 
(select pra_number from hht_lawyer_guizhou group by pra_number having(count(*) > 1)) order by pra_number
经统计，pra_number一样，名字不一样，需要关联后去重；


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_guizhou where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_guizhou set pra_number = replace(pra_number,'"','');
update hht_lawyer_guizhou set pra_number = replace(pra_number,' ','');
update hht_lawyer_guizhou set pra_number = replace(pra_number,"'",'');
update hht_lawyer_guizhou set pra_number = replace(pra_number,"‘",'');
update hht_lawyer_guizhou set pra_number = replace(pra_number,"’",'');
update hht_lawyer_guizhou set pra_number = replace(pra_number,"	",'');

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_guizhou where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_guizhou set name = replace(name,"	","");
update hht_lawyer_guizhou set name = replace(name,"李娜1","李娜");

3）org_name：

update hht_lawyer_guizhou set org_name = replace(org_name,"（","(");
update hht_lawyer_guizhou set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_guizhou where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_guizhou set org_name = replace(org_name," ","");

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_guizhou_match as
select a.* from hht_lawyer_guizhou a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_guizhou_match where pra_number in 
(select pra_number from hht_lawyer_guizhou_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；

过滤新增数据：
create table hht_lawyer_guizhou_add as 
select * from hht_lawyer_guizhou where pra_number not in (
select a.pra_number from hht_lawyer_guizhou a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_guizhou_add where pra_number in 
(select pra_number from hht_lawyer_guizhou_add group by pra_number having(count(*) > 1)) order by pra_number
共6条数据，执业证号一样，名字不一样，无法取舍，直接删除；

delete from hht_lawyer_guizhou_add where pra_number in (
select a.pra_number from 
(select pra_number from hht_lawyer_guizhou_add group by pra_number having(count(*) > 1)) as a
)

===============================================================
河南数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_henan where pra_number = "" or pra_number is null;
delete from hht_lawyer_henan where name = "" or name is null;
delete from hht_lawyer_henan where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_henan where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_henan set pra_number = replace(pra_number,' ','');
delete from hht_lawyer_henan where pra_number = "1"
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,' ','');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"'",'');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"‘",'');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"’",'');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"	",'');

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_henan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_henan set name = replace(name," ","");

delete from hht_lawyer_henan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

3）org_name：

update hht_lawyer_henan set org_name = replace(org_name,"（","(");
update hht_lawyer_henan set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_henan where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_henan_match as
select a.* from hht_lawyer_henan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_henan_match where pra_number in 
(select pra_number from hht_lawyer_henan_match group by pra_number having(count(*) > 1)) order by pra_number

delete from hht_lawyer_henan_match where id = 68012;

过滤新增数据：
create table hht_lawyer_henan_add as 
select * from hht_lawyer_henan where pra_number not in (
select a.pra_number from hht_lawyer_henan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_henan_add where pra_number in 
(select pra_number from hht_lawyer_henan_add group by pra_number having(count(*) > 1)) order by pra_number
无结果；

-- delete from hht_lawyer_guizhou_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_guizhou_add group by pra_number having(count(*) > 1)) as a
-- )
=========================
辽宁数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_liaoning where pra_number = "" or pra_number is null;
delete from hht_lawyer_liaoning where name = "" or name is null;
delete from hht_lawyer_liaoning where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_liaoning where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_liaoning set pra_number = replace(pra_number,' ','');
-- delete from hht_lawyer_henan where pra_number = "1"
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,' ','');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"'",'');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"‘",'');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"’",'');
-- update hht_lawyer_guizhou set pra_number = replace(pra_number,"	",'');

2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_liaoning where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

delete from hht_lawyer_liaoning where name like "律师%" or name like "律师%" 
update hht_lawyer_liaoning set name = replace(name,"（","(");
update hht_lawyer_liaoning set name = replace(name,"）",")");
update hht_lawyer_liaoning set name = replace(name,"(小)","");
update hht_lawyer_liaoning set name = replace(name,"(大)","");

-- delete from hht_lawyer_henan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
-- or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

3）org_name：

update hht_lawyer_liaoning set org_name = replace(org_name,"（","(");
update hht_lawyer_liaoning set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_liaoning where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_liaoning_match as
select a.* from hht_lawyer_liaoning a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_liaoning_match where pra_number in 
(select pra_number from hht_lawyer_liaoning_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；

过滤新增数据：
create table hht_lawyer_liaoning_add as 
select * from hht_lawyer_liaoning where pra_number not in (
select a.pra_number from hht_lawyer_liaoning a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_liaoning_add where pra_number in 
(select pra_number from hht_lawyer_liaoning_add group by pra_number having(count(*) > 1)) order by pra_number
无结果；

-- delete from hht_lawyer_guizhou_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_guizhou_add group by pra_number having(count(*) > 1)) as a
-- )
=========================
青海数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_qinghai where pra_number = "" or pra_number is null;
delete from hht_lawyer_qinghai where name = "" or name is null;
delete from hht_lawyer_qinghai where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_qinghai where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_qinghai set pra_number = replace(pra_number,' ','');
update hht_lawyer_qinghai set pra_number = replace(pra_number,'？','');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_qinghai where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- delete from hht_lawyer_liaoning where name like "律师%" or name like "律师%" 
-- update hht_lawyer_liaoning set name = replace(name,"（","(");
-- update hht_lawyer_liaoning set name = replace(name,"）",")");
-- update hht_lawyer_liaoning set name = replace(name,"(小)","");
-- update hht_lawyer_liaoning set name = replace(name,"(大)","");

-- delete from hht_lawyer_henan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
-- or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

3）org_name：

update hht_lawyer_qinghai set org_name = replace(org_name,"（","(");
update hht_lawyer_qinghai set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_qinghai where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_qinghai set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_qinghai_match as
select a.* from hht_lawyer_qinghai a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_qinghai_match where pra_number in 
(select pra_number from hht_lawyer_qinghai_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；

过滤新增数据：
create table hht_lawyer_qinghai_add as 
select * from hht_lawyer_qinghai where pra_number not in (
select a.pra_number from hht_lawyer_qinghai a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_qinghai_add where pra_number in 
(select pra_number from hht_lawyer_qinghai_add group by pra_number having(count(*) > 1)) order by pra_number

执业证号一样，名字不一样，无法取舍，直接删除；

delete from hht_lawyer_qinghai_add where pra_number in (
select a.pra_number from 
(select pra_number from hht_lawyer_qinghai_add group by pra_number having(count(*) > 1)) as a
)
===================
陕西数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_shanxi where pra_number = "" or pra_number is null;
delete from hht_lawyer_shanxi where name = "" or name is null;
delete from hht_lawyer_shanxi where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_shanxi where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_shanxi set pra_number = replace(pra_number,' ','');
update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_shanxi where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

delete from hht_lawyer_shanxi where name = "何？"
update hht_lawyer_shanxi set name = replace(name," ","");
update hht_lawyer_shanxi set name = replace(name,"l","");
update hht_lawyer_shanxi set name = replace(name,"周涛C","周涛");


3）org_name：

update hht_lawyer_shanxi set org_name = replace(org_name,"（","(");
update hht_lawyer_shanxi set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_shanxi where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_shanxi set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_shanxi_match as
select a.* from hht_lawyer_shanxi a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_shanxi_match where pra_number in 
(select pra_number from hht_lawyer_shanxi_match group by pra_number having(count(*) > 1)) order by pra_number

经统计，有重复的，说明三字段一样时有重复，查看数据发现，max(id)不完整，因此去重删除max(id)：
delete from hht_lawyer_shanxi_match where id in (
select a.id from (
select max(id) as id from hht_lawyer_shanxi_match a group by pra_number having(count(*) > 1)
) as a
)

过滤新增数据：
create table hht_lawyer_shanxi_add as 
select * from hht_lawyer_shanxi where pra_number not in (
select a.pra_number from hht_lawyer_shanxi a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


delete  from hht_lawyer_shanxi_add where id in 
(select a.id from 
(select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
) 

delete from hht_lawyer_shanxi_add where CHAR_LENGTH(pra_number) < 4

=========================================================================
四川数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_sichuan where pra_number = "" or pra_number is null;
delete from hht_lawyer_sichuan where name = "" or name is null;
delete from hht_lawyer_sichuan where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_sichuan where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_shanxi set pra_number = replace(pra_number,' ','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_sichuan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_sichuan set name = replace(name," ","");
update hht_lawyer_sichuan set name = replace(name,"邓永刚（绵阳分所）","邓永刚");


3）org_name：

update hht_lawyer_sichuan set org_name = replace(org_name,"（","(");
update hht_lawyer_sichuan set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_sichuan where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_sichuan_match as
select a.* from hht_lawyer_sichuan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_sichuan_match where pra_number in 
(select pra_number from hht_lawyer_sichuan_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，说明三字段一样时有重复，查看数据发现，max(id)不完整，因此去重删除max(id)：
-- delete from hht_lawyer_shanxi_match where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_shanxi_match a group by pra_number having(count(*) > 1)
-- ) as a
-- )

过滤新增数据：
create table hht_lawyer_sichuan_add as 
select * from hht_lawyer_sichuan where pra_number not in (
select a.pra_number from hht_lawyer_sichuan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_sichuan_add where pra_number in 
(select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) order by pra_number
执业证号一样，名字不一样，无法取舍，直接删除；


delete from hht_lawyer_sichuan_add where pra_number in (
select a.pra_number from 
(select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
)
delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================
天津数据处理：


设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_tianjin where pra_number = "" or pra_number is null;
delete from hht_lawyer_tianjin where name = "" or name is null;
delete from hht_lawyer_tianjin where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_tianjin where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_shanxi set pra_number = replace(pra_number,' ','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_tianjin where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_sichuan set name = replace(name," ","");
-- update hht_lawyer_sichuan set name = replace(name,"邓永刚（绵阳分所）","邓永刚");


3）org_name：

update hht_lawyer_tianjin set org_name = replace(org_name,"（","(");
update hht_lawyer_tianjin set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_tianjin where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_tianjin_match as
select a.* from hht_lawyer_tianjin a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_tianjin_match where pra_number in 
(select pra_number from hht_lawyer_tianjin_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，说明三字段一样时有重复，查看数据发现，max(id)不完整，因此去重删除max(id)：
-- delete from hht_lawyer_shanxi_match where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_shanxi_match a group by pra_number having(count(*) > 1)
-- ) as a
-- )

过滤新增数据：
create table hht_lawyer_tianjin_add as 
select * from hht_lawyer_tianjin where pra_number not in (
select a.pra_number from hht_lawyer_tianjin a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_tianjin_add where pra_number in 
(select pra_number from hht_lawyer_tianjin_add group by pra_number having(count(*) > 1)) order by pra_number
无结果；


-- delete from hht_lawyer_sichuan_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
-- )
-- delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================
新疆数据处理：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_xinjiang where pra_number = "" or pra_number is null;
delete from hht_lawyer_xinjiang where name = "" or name is null;
delete from hht_lawyer_xinjiang where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_xinjiang where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_xinjiang set pra_number = replace(pra_number,'I','1');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_xinjiang where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_xinjiang set name = replace(name,"。",".");
update hht_lawyer_xinjiang set name = replace(name,"，",".");
update hht_lawyer_xinjiang set name = replace(name,"?",".");
-- update hht_lawyer_sichuan set name = replace(name," ","");
-- update hht_lawyer_sichuan set name = replace(name,"邓永刚（绵阳分所）","邓永刚");


3）org_name：

update hht_lawyer_xinjiang set org_name = replace(org_name,"（","(");
update hht_lawyer_xinjiang set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_xinjiang where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_xinjiang_match as
select a.* from hht_lawyer_xinjiang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_xinjiang_match where pra_number in 
(select pra_number from hht_lawyer_xinjiang_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，说明三字段一样时有重复，查看数据发现，max(id)不完整，因此去重删除max(id)：
-- delete from hht_lawyer_shanxi_match where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_shanxi_match a group by pra_number having(count(*) > 1)
-- ) as a
-- )

过滤新增数据：
create table hht_lawyer_xinjiang_add as 
select * from hht_lawyer_xinjiang where pra_number not in (
select a.pra_number from hht_lawyer_xinjiang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_xinjiang_add where pra_number in 
(select pra_number from hht_lawyer_xinjiang_add group by pra_number having(count(*) > 1)) order by pra_number
无结果；


-- delete from hht_lawyer_sichuan_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
-- )
-- delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================
西藏数据处理：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_xizang where pra_number = "" or pra_number is null;
delete from hht_lawyer_xizang where name = "" or name is null;
delete from hht_lawyer_xizang where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_xizang where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- update hht_lawyer_xinjiang set pra_number = replace(pra_number,'I','1');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_xizang where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- update hht_lawyer_xinjiang set name = replace(name,"。",".");
-- update hht_lawyer_xinjiang set name = replace(name,"，",".");
-- update hht_lawyer_xinjiang set name = replace(name,"?",".");
-- update hht_lawyer_sichuan set name = replace(name," ","");
-- update hht_lawyer_sichuan set name = replace(name,"邓永刚（绵阳分所）","邓永刚");


3）org_name：

update hht_lawyer_xizang set org_name = replace(org_name,"（","(");
update hht_lawyer_xizang set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_xizang where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_xizang_match as
select a.* from hht_lawyer_xizang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_xizang_match where pra_number in 
(select pra_number from hht_lawyer_xizang_match group by pra_number having(count(*) > 1)) order by pra_number

经统计，有重复的，只有三个字段且三字段一样，因此去重删除max(id)：
执行多次以下语句：
delete from hht_lawyer_xizang_match where id in (
select a.id from (
select max(id) as id from hht_lawyer_xizang_match a group by pra_number having(count(*) > 1)
) as a
)

过滤新增数据：
create table hht_lawyer_xizang_add as 
select * from hht_lawyer_xizang where pra_number not in (
select a.pra_number from hht_lawyer_xizang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_xizang_add where pra_number in 
(select pra_number from hht_lawyer_xizang_add group by pra_number having(count(*) > 1)) order by pra_number

经统计，有重复的，只有三个字段且三字段一样，因此去重删除max(id)：
执行多次以下语句：
delete from hht_lawyer_xizang_add where id in (
select a.id from (
select max(id) as id from hht_lawyer_xizang_add a group by pra_number having(count(*) > 1)
) as a
)


-- delete from hht_lawyer_sichuan_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
-- )
-- delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================
云南数据处理：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_yunnan where pra_number = "" or pra_number is null;
delete from hht_lawyer_yunnan where name = "" or name is null;
delete from hht_lawyer_yunnan where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_yunnan where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_xinjiang set pra_number = replace(pra_number,'I','1');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_yunnan where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- update hht_lawyer_xinjiang set name = replace(name,"。",".");
-- update hht_lawyer_xinjiang set name = replace(name,"，",".");
-- update hht_lawyer_xinjiang set name = replace(name,"?",".");
-- update hht_lawyer_sichuan set name = replace(name," ","");
-- update hht_lawyer_sichuan set name = replace(name,"邓永刚（绵阳分所）","邓永刚");


3）org_name：

update hht_lawyer_yunnan set org_name = replace(org_name,"（","(");
update hht_lawyer_yunnan set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_yunnan where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_yunnan_match as
select a.* from hht_lawyer_yunnan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_yunnan_match where pra_number in 
(select pra_number from hht_lawyer_yunnan_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，只有三个字段且三字段一样，因此去重删除max(id)：
-- 执行多次以下语句：
-- delete from hht_lawyer_xizang_match where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_xizang_match a group by pra_number having(count(*) > 1)
-- ) as a
-- )

过滤新增数据：
create table hht_lawyer_yunnan_add as 
select * from hht_lawyer_yunnan where pra_number not in (
select a.pra_number from hht_lawyer_yunnan a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_yunnan_add where pra_number in 
(select pra_number from hht_lawyer_yunnan_add group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，只有三个字段且三字段一样，因此去重删除max(id)：
-- 执行多次以下语句：
-- delete from hht_lawyer_xizang_add where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_xizang_add a group by pra_number having(count(*) > 1)
-- ) as a
-- )


-- delete from hht_lawyer_sichuan_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
-- )
-- delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================
广东省数据处理：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_gds_gdlawyer where pra_number = "" or pra_number is null;
delete from hht_lawyer_gds_gdlawyer where name = "" or name is null;
delete from hht_lawyer_gds_gdlawyer where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_gds_gdlawyer where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_xinjiang set pra_number = replace(pra_number,'I','1');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'	','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,'？','');
-- update hht_lawyer_shanxi set pra_number = replace(pra_number,"'",'');


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_gds_gdlawyer where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

经百度搜索，律师名字更正如下：
update hht_lawyer_gds_gdlawyer set name = replace(name,"潘新?","潘新翀");
update hht_lawyer_gds_gdlawyer set name = replace(name,"熊wei","熊韡");
update hht_lawyer_gds_gdlawyer set name = replace(name,"施小?","施小珺");
update hht_lawyer_gds_gdlawyer set name = replace(name,"雷旌wei","雷旌韡");
update hht_lawyer_gds_gdlawyer set name = replace(name,"黄惠?","黄惠堎");
delete from hht_lawyer_gds_gdlawyer where name in ("杨雯?","李国?")

-- update hht_lawyer_xinjiang set name = replace(name,"。",".");
-- update hht_lawyer_xinjiang set name = replace(name,"，",".");
-- update hht_lawyer_xinjiang set name = replace(name,"?",".");
-- update hht_lawyer_sichuan set name = replace(name," ","");


3）org_name：

update hht_lawyer_gds_gdlawyer set org_name = replace(org_name,"（","(");
update hht_lawyer_gds_gdlawyer set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_gds_gdlawyer where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

-- update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_gds_gdlawyer_match as
select a.* from hht_lawyer_gds_gdlawyer a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_gds_gdlawyer_match where pra_number in 
(select pra_number from hht_lawyer_gds_gdlawyer_match group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，只有三个字段且三字段一样，因此去重删除max(id)：
-- 执行多次以下语句：
-- delete from hht_lawyer_xizang_match where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_xizang_match a group by pra_number having(count(*) > 1)
-- ) as a
-- )

过滤新增数据：
create table hht_lawyer_gds_gdlawyer_add as 
select * from hht_lawyer_gds_gdlawyer where pra_number not in (
select a.pra_number from hht_lawyer_gds_gdlawyer a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_gds_gdlawyer_add where pra_number in 
(select pra_number from hht_lawyer_gds_gdlawyer_add group by pra_number having(count(*) > 1)) order by pra_number
无结果；
-- 经统计，有重复的，只有三个字段且三字段一样，因此去重删除max(id)：
-- 执行多次以下语句：
-- delete from hht_lawyer_xizang_add where id in (
-- select a.id from (
-- select max(id) as id from hht_lawyer_xizang_add a group by pra_number having(count(*) > 1)
-- ) as a
-- )


-- delete from hht_lawyer_sichuan_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
-- )
-- delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================

黑龙江数据处理：

设计表中，先删除无用字段；

1、先统计、删除空执业证、去重；pra_number、name、org_name三个字段；

delete from hht_lawyer_heilongjiang where pra_number = "" or pra_number is null;
delete from hht_lawyer_heilongjiang where name = "" or name is null;
delete from hht_lawyer_heilongjiang where org_name = "" or org_name is null;


1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_heilongjiang where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_heilongjiang set pra_number = replace(pra_number,'	','');
update hht_lawyer_heilongjiang set pra_number = replace(pra_number,' ','');
update hht_lawyer_heilongjiang set pra_number = replace(pra_number,"'",'');
update hht_lawyer_heilongjiang set pra_number = replace(pra_number,"12308198610565786yj",'12308198610565786');
update hht_lawyer_heilongjiang set pra_number = replace(pra_number,"hlj12302200211460287",'12302200211460287');
update hht_lawyer_heilongjiang set pra_number = replace(pra_number,"12310199710621446+",'12310199710621446');
delete from hht_lawyer_heilongjiang where 
pra_number like "%xx%" or pra_number like "%号" or pra_number like "%服务%"



2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_heilongjiang where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


update hht_lawyer_heilongjiang set name = replace(name," ","");
update hht_lawyer_heilongjiang set name = replace(name,"	","");

-- update hht_lawyer_xinjiang set name = replace(name,"。",".");
-- update hht_lawyer_xinjiang set name = replace(name,"，",".");
-- update hht_lawyer_xinjiang set name = replace(name,"?",".");
-- update hht_lawyer_sichuan set name = replace(name," ","");


3）org_name：

update hht_lawyer_heilongjiang set org_name = replace(org_name,"（","(");
update hht_lawyer_heilongjiang set org_name = replace(org_name,"）",")");

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_heilongjiang where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
无结果；
-- update hht_lawyer_sichuan set org_name = replace(org_name," ","")

2、必须先进行关联；关联之后才能确定重复的数据中，哪条数据名字是正确的；
create table hht_lawyer_heilongjiang_match as
select a.* from hht_lawyer_heilongjiang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

select * from hht_lawyer_heilongjiang_match where pra_number in 
(select pra_number from hht_lawyer_heilongjiang_match group by pra_number having(count(*) > 1)) order by pra_number

经统计，有重复的，三字段一样，其他主要字段也一样，因此去重删除max(id)：
执行多次以下语句：
delete from hht_lawyer_heilongjiang_match where id in (
select a.id from (
select max(id) as id from hht_lawyer_heilongjiang_match a group by pra_number having(count(*) > 1)
) as a
)

过滤新增数据：
create table hht_lawyer_heilongjiang_add as 
select * from hht_lawyer_heilongjiang where pra_number not in (
select a.pra_number from hht_lawyer_heilongjiang a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select * from hht_lawyer_heilongjiang_add where pra_number in 
(select pra_number from hht_lawyer_heilongjiang_add group by pra_number having(count(*) > 1)) 
 order by pra_number

经统计，有重复的，有三字段一样的，也有执业证号一样但三字段不一样的，
因此去重三字段一样的，删除执业证号一样但三字段不一样的（无法取舍）；

1）去重三字段一样的：
delete from hht_lawyer_heilongjiang_add where id in (
select a.id from (
select max(id) as id from hht_lawyer_heilongjiang_add a group by pra_number,name,org_name having(count(*) > 1)
) as a
)
2）删除执业证号一样但三字段不一样的（因为无法取舍）：
delete from hht_lawyer_heilongjiang_add where id in (
select a.id from (
select max(id) as id from hht_lawyer_heilongjiang_add a group by pra_number having(count(*) > 1)
) as a
)

-- delete from hht_lawyer_sichuan_add where pra_number in (
-- select a.pra_number from 
-- (select pra_number from hht_lawyer_sichuan_add group by pra_number having(count(*) > 1)) as a
-- )
-- delete from hht_lawyer_sichuan_add where CHAR_LENGTH(pra_number) < 4

-- delete  from hht_lawyer_shanxi_add where id in 
-- (select a.id from 
-- (select max(id) as id from hht_lawyer_shanxi_add group by pra_number having(count(*) > 1)) a
-- ) 
==============================================
