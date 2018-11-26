===================================================
============Mysql中使用正则，注意的问题：==========
===================================================
英文,!:()+/@空格等都不是特殊符号，可以直接用，空格不区分中英文；
英文特殊字符.|?][\-
.| 直接放在[]之内不转义，或放在[]之外加\\转义，如[a-z0-9A-Z_.|]等价于[a-z0-9A-Z_]|\\.|\\|
?][- 必须放在[]之外加\\转义，如[a-z0-9A-Z_.|()]|\\?|\\]|\\[|\\-|\\-
\字符匹配，必须放在[]之内加\转义，使用[\\]进行匹配，不能放在[]之外匹配，如[a-z0-9A-Z_|\\]


""双引号匹配,引号放在[]的最后,如'[a-z0-9A-Z()"]'
或者放[]之外使用\\转义：如'[a-z0-9A-Z()]|\\"'

''单引号匹配，放在[]之内，使用\转义，如'[a-z0-9A-Z()\\|"\']'
或放[]之外使用\\\转义：如'[a-z0-9A-Z()\\|"]|\\\''

单引号、双引号的匹配，取决于正则表达式字符串使用单还是双引号，如果使用双引号，
则上面单双引号的匹配规则相反。

注意：\\在[]中不能放在.|?字符之前以及[]中的最前或最后（紧挨着[]号）,否则会报错（可能\\会转义后面的字符，然后报错），
最好放在[]中的()之前，

匹配英文字符a-z0-9A-Z ,:-\()+!/.|"'@?[]等的正则为：
REGEXP '[a-z0-9A-Z ,:;\\()+!/.|"\'@]|\\?|\\]|\\[|\\-';
-- SELECT org_name from hht_lawyer_anhui where org_name REGEXP '[a-z0-9A-Z ,:;\\().|"\']|\\?|\\]|\\[|\\-';

注意：^只有在[]中才是取反，取反[]内的任意一个字符，就是除了[]中的字符，否则都是以字符开头的意思；

汉字、中文字符，。、：；？（）！‘’等不能直接使用[]匹配，需使用hex()函数将原中文字段转为16进制，
也就是python中的str类型，再进行比较:比如冒号：16进制为'\xef\xbc\x9a'，需要使用'efbc9a'进行匹配！
，。、：；？（）！对应16进制为：
\xef\xbc\x8c\xe3\x80\x82\xe3\x80\x81\xef\xbc\x9a\xef\xbc\x9b\xef\xbc\x9f\xef\xbc\x88\xef\xbc\x89\xef\xbc\x81\xe2\x80\x98\xe2\x80\x99
去掉\x,匹配规则为：
hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc88|efbc89|efbc81|e28098|e28099';
utf8编码汉字匹配：hex(pra_number) REGEXP 'e[4-9][0-9a-f]{4}';

=================================================================================================
=================================================================================================
=================================================================================================
法网hht_lawyer_12348gov_v4表pra_number、name、org_name三个字段统一处理：

SELECT id,pra_number from hht_lawyer_12348gov_v4 where pra_number REGEXP '[a-zA-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
满足要求；

SELECT * from hht_lawyer_12348gov_v4 where name REGEXP '[a-z0-9A-Z ,:;\\()!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
满足要求；

update hht_lawyer_12348gov_v4 set org_name = replace(org_name,"（","(");
update hht_lawyer_12348gov_v4 set org_name = replace(org_name,"）",")");

SELECT id,org_name from hht_lawyer_12348gov_v4 where org_name REGEXP '[a-z0-9A-Z ,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099';


-- 处理思路：
-- 1执业证号
-- 2姓名
-- 3律所
-- 4执业状态
-- 5执业历程
-- 
-- 1一样：
-- 	123一样：直接根据4取舍。
-- 	1一样，2或3或23不一样：12一样，3不一样，根据执业历程，
-- 		1）法网律所在执业历程中的话：更新执业律所等字段，根据执业状态来取舍。
-- 		2）法网律所不在执业历程中的话：直接扔掉；
-- 1不一样：直接新增数据。


安徽处理流程：
1、先统计、删除空执业证、去重；：pra_number、name、org_name三个字段；
delete from hht_lawyer_anhui where pra_number = "" or pra_number is null;
delete from hht_lawyer_anhui where name = "" or name is null;
delete from hht_lawyer_anhui where org_name = "" or org_name is null;

select min(id) from hht_lawyer_anhui group by pra_number having(count(*) > 1) 
1）pra_number:
SELECT id,pra_number from hht_lawyer_anhui where pra_number REGEXP '[a-zA-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2）name：
SELECT * from hht_lawyer_anhui where name REGEXP '[a-z0-9A-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

3）org_name：
SELECT id,org_name from hht_lawyer_anhui where org_name REGEXP '[a-z0-9A-Z ,:;\\()+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099';

update hht_lawyer_anhui set org_name = replace(org_name,"（","(");
update hht_lawyer_anhui set org_name = replace(org_name,"）",")");

2、针对统计的结果规律进行pra_number、name、org_name字段的处理
update hht_lawyer_anhui set org_name = replace(org_name,"1","") where id = 24297

3、然后进行关联；
create table hht_lawyer_anhui_match as
select a.* from hht_lawyer_anhui a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name

create table hht_lawyer_anhui_add as 
select * from hht_lawyer_anhui where pra_number not in (
select a.pra_number from hht_lawyer_anhui a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


北上广深处理流程：
1、先统计、删除空执业证、去重；：pra_number、name、org_name三个字段；
delete from hht_lawyer_bsgs where pra_number = "" or pra_number is null;
delete from hht_lawyer_bsgs where name = "" or name is null;
delete from hht_lawyer_bsgs where org_name = "" or org_name is null;

select min(id) from hht_lawyer_bsgs group by pra_number having(count(*) > 1) 
1）pra_number:
SELECT id,pra_number from hht_lawyer_bsgs where pra_number REGEXP '[a-zA-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2）name：
SELECT * from hht_lawyer_bsgs where name REGEXP '[a-z0-9A-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

执业证号、律所一样,补充名字；
select * from hht_lawyer_bsgs a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number where a.name REGEXP '[a-z0-9A-Z ,:;\\()+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(a.name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


3）org_name：
SELECT id,org_name from hht_lawyer_bsgs where org_name REGEXP '[a-z0-9A-Z ,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099';

update hht_lawyer_bsgs set org_name = replace(org_name,"（","(");
update hht_lawyer_bsgs set org_name = replace(org_name,"）",")");
2、针对统计的结果规律进行pra_number、name、org_name字段的处理
delete from hht_lawyer_bsgs where name REGEXP '[a-z0-9A-Z ,:;\\()!+@|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


3、然后进行关联；
create table hht_lawyer_bsgs_match as
select a.* from hht_lawyer_bsgs a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name where a.practicestatus = "注销"

create table hht_lawyer_bsgs_add as 
select * from hht_lawyer_bsgs where pra_number not in (
select a.pra_number from hht_lawyer_bsgs a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 

select * from hht_lawyer_12348gov_v4 where pra_number in (
select pra_number from hht_lawyer_bsgs where practicestatus = "注销"
)

-- select practicestatus,count(*) from hht_lawyer_bsgs group by practicestatus ;
-- NULL  12141
-- 其他	2
-- 吊销	7
-- 执业	42771
-- 未经年度考核	693
-- 正常	23117
-- 注销	6464
-- 律师执业证注销申请条件：
-- 一、法律依据
-- 《律师执业管理办法》（2016年9月18日司法部令第134号修订）
-- 第二十三条　律师有下列情形之一的，由其执业地的原审核颁证机关收回、注销其律师执业证书：
-- （一）受到吊销律师执业证书处罚的；
-- （二）原准予执业的决定被依法撤销的；
-- （三）因本人不再从事律师职业申请注销的；
-- （四）因与所在律师事务所解除聘用合同或者所在的律师事务所被注销，在六个月内未被其他律师事务所聘用的；
-- （五）因其他原因终止律师执业的。
-- 律师正在接受司法机关、司法行政机关、律师协会立案调查期间，不得申请注销执业证书。



重庆处理流程：
1、先统计、删除空执业证、去重；：pra_number、name、org_name三个字段；
delete from hht_lawyer_chongqing where pra_number = "" or pra_number is null;
delete from hht_lawyer_chongqing where name = "" or name is null;
delete from hht_lawyer_chongqing where org_name = "" or org_name is null;


select min(id) from hht_lawyer_chongqing group by pra_number having(count(*) > 1) 
删除重复数据：执行多次，因为一次只能删除重复中的一条，有的可能重复多次；一直删除到结果为0为止；
delete from hht_lawyer_chongqing where id in (
select a.id from (
select min(id) as id from hht_lawyer_chongqing a group by pra_number having(count(*) > 1)
) as a
)

1）pra_number:
SELECT id,pra_number from hht_lawyer_chongqing where pra_number REGEXP '[a-zA-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

2）name：
SELECT * from hht_lawyer_chongqing where name REGEXP '[a-z0-9A-Z ,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

3）org_name：
SELECT id,org_name from hht_lawyer_chongqing where org_name REGEXP '[a-z0-9A-Z ,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

update hht_lawyer_chongqing set org_name = replace(org_name,"（","(");
update hht_lawyer_chongqing set org_name = replace(org_name,"）",")");

2、针对统计的结果规律进行pra_number、name、org_name字段的处理
无需处理；
3、然后进行关联；
create table hht_lawyer_chongqing_match as
select a.* from hht_lawyer_chongqing a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name 

create table hht_lawyer_chongqing_add as 
select * from hht_lawyer_chongqing where pra_number not in (
select a.pra_number from hht_lawyer_chongqing a join hht_lawyer_12348gov_v4 b on 
a.pra_number = b.pra_number) 


select practicestatus,count(*) from hht_lawyer_chongqing group by practicestatus ;
正常执业	10428