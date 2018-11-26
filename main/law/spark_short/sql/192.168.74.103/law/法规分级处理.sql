统计分析：
select * from law_rule_result_article where cate_a like "%全国人大%" or cate_a like "%全国人民代表大会%" 
select department,count(*) from law_rule_result_article where 
cate_a like "%全国人大%" or cate_a like "%全国人民代表大会%" group by department order by count(*) desc 



select * from law_rule_result_article where cate_a like "%全国人大%" and department not like "%全国人大常委会%" 
and department not like "%全国人民代表大会%" and department not like "%全国人民代表大会常务委员会%" ;
-- select * from law_rule_result_article where title_short like "%法" and title_short not like "%办法" and cate_a like "全国人大法律库" limit 1000

统计分析：
select cate_a,count(*) from law_rule_result_article group by cate_a order by count(*) desc 
地方规范性文件库	404246
国家规范性文件库	112341
团体、行业规范库	23341
地方政府规章库	18827
国务院部委规章库	18397
地方人大法规库	17156
国务院行政法规库	5289
立法、司法解释库	5007
地方司法规范库	3602
全国人大法律库	1439
军事法规库	12
国际法、国际条约与惯例库	5
-- select  * from law_rule_result_article where cate_a is null

1、人民代表大会及其委员会制定的法律：

select right(title_short,2),count(*) from law_rule_result_article where 
cate_a = "全国人大法律库"  and department != "国务院" 
and not (title_short like "中华人民共和国%法%" and title_short not like "%办法") 
group by right(title_short,2) order by count(*) desc ;
决定	536
决议	306
报告	39
年）	39
条例	26
答复	25
意见	21
办法	19
规定	10
通知	8
计划	6
纲要	5
公告	4
方案	4
通则	4
号）	3
要点	3
批复	3
正）	2
规则	2
订）	2
守则	2
解释	2
件）	2
复函	2
01	1
99	1
程序	1
处理	1
章程	1
答五	1
答六	1
权利	1
草案	1
答三	1
法）	1
90	1
93	1
答一	1
者问	1
赦令	1
司法	1

-- select * from law_rule_result_article where 
-- cate_a = "全国人大法律库"  and department != "国务院" and not 
-- (title_short like "中华人民共和国%法%" and title_short not like "%办法") and title_short like "%条例" limit 100;
select  * from law_rule_result_article where 
cate_a = "全国人大法律库" and right(title_short,2) in ("通知","批复","条例") limit 100

更新等级字段：
10: 中华人民共和国**法；
-- select * from law_rule_result_article where cate_a = "全国人大法律库"  and department != "国务院" and title_short like "中华人民共和国%法%" and title_short not like "%办法";
update  law_rule_result_article  set law_grade = "10" where cate_a = "全国人大法律库"  and 
department != "国务院" and title_short like "中华人民共和国%法%" and title_short not like "%办法";
338

11:条例;
update  law_rule_result_article  set law_grade = "11" where cate_a = "全国人大法律库"  and 
department != "国务院" and right(title_short,2) = "条例";

12:规定;
update  law_rule_result_article  set law_grade = "12" where cate_a = "全国人大法律库"  and 
department != "国务院" and right(title_short,2) = "规定";

13:办法;
update  law_rule_result_article  set law_grade = "13" where cate_a = "全国人大法律库"  and 
department != "国务院" and right(title_short,2) = "办法";

14:通知、意见、命令、批复、**决定，决议，公告，意见等；
update  law_rule_result_article  set law_grade = "14" where cate_a = "全国人大法律库"  and 
department != "国务院" and law_grade is null;


2、行政法规：
-- select * from law_rule_result_article where cate_a = "国务院行政法规库" ;
20:条例;
update  law_rule_result_article set law_grade = "20" where cate_a = "国务院行政法规库" and right(title_short,2) = "条例" ;
update  law_rule_result_article  set law_grade = "20" where 
cate_a = "全国人大法律库"  and department = "国务院" and right(title_short,2) = "条例" ;

-- select * from law_rule_result_article where cate_a = "全国人大法律库"  and department= "国务院";

21:规定;
update  law_rule_result_article set law_grade = "21" where cate_a = "国务院行政法规库" and right(title_short,2) = "规定" ;
update  law_rule_result_article  set law_grade = "21" where 
cate_a = "全国人大法律库"  and department = "国务院" and right(title_short,2) = "规定" ;

22:办法;
update  law_rule_result_article set law_grade = "22" where cate_a = "国务院行政法规库" and right(title_short,2) = "办法" ;
update  law_rule_result_article  set law_grade = "22" where 
cate_a = "全国人大法律库"  and department = "国务院" and right(title_short,2) = "办法" ;
23:通知、意见、命令、批复等；
update  law_rule_result_article set law_grade = "23" where cate_a = "国务院行政法规库" and law_grade is null; ;
update  law_rule_result_article  set law_grade = "23" where 
cate_a = "全国人大法律库"  and department = "国务院" and law_grade is null;

select right(title_short,2),count(*) from law_rule_result_article where cate_a = "国务院行政法规库" 
group by right(title_short,2) order by count(*) desc ;
通知	2361
批复	734
条例	547
意见	350
规定	273
决定	208
复函	134
办法	132
报告	109
方案	48
的函	32
通报	24
指示	22

select  * from law_rule_result_article where 
cate_a = "国务院行政法规库" and right(title_short,2) in ("通知","批复","条例") limit 100


3、部门规章：select * from law_rule_result_article where 
cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库"
 limit 100;


-- select * from law_rule_result_article where (cate_a = "国务院部委规章库" or cate_a = "国家规范性文件库" or cate_a = "团体、行业规范库" ) and title_short like "%条例" limit 100;
-- select * from law_rule_result_article where (cate_a = "国务院部委规章库" or cate_a = "国家规范性文件库" or cate_a = "团体、行业规范库" ) and title_short like "%规定" limit 100;
-- select * from law_rule_result_article where (cate_a = "国务院部委规章库" or cate_a = "国家规范性文件库" or cate_a = "团体、行业规范库" ) and title_short like "%办法" limit 100;
30:条例;
update law_rule_result_article set law_grade = "30" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and right(title_short,2) = "条例" ;
31:规定;
update law_rule_result_article set law_grade = "31" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and right(title_short,2) = "规定" ;
32:办法;
update law_rule_result_article set law_grade = "32" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and right(title_short,2) = "办法" ;
33:通知、意见、命令、批复等；
update law_rule_result_article set law_grade = "33" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and law_grade is null ;


-- 5、地方行政法规：
-- select * from law_rule_result_article where cate_a = "地方人大法规库" limit 200;
-- 30:条例;
-- 31:规定;
-- 32:办法;
-- 33:通知、意见、命令、批复等；


select right(title_short,2),count(*) from law_rule_result_article where 
cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库"
 group by right(title_short,2) order by count(*) desc ;
通知	76762
批复	19376
公告	18055
办法	7940
条例	7191
规定	5228
决定	4948
意见	4589
复函	4045
的函	3764
答复	1657
通报	1582
修订	870
效]	837
行）	677
细则	641
通告	621
规则	490
13	474
决议	431
票据	399
14	397
04	381
国债	362
报告	358
11	299
标准	296
号）	293
97	288
12	286
解释	281
目录	280
方案	233
规范	225
规程	214
制度	209
试行	195
02	195
提示	193
年）	189
0）	158
公示	157
05	155

select  * from law_rule_result_article where 
(cate_a = "国务院部委规章库" or cate_a = "地方人大法规库")  and right(title_short,2) in ("通知","批复","条例") limit 100



4、地方政府规章：

select * from law_rule_result_article where 
cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" 
limit 200;
40:条例;
update law_rule_result_article set law_grade = "40" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and right(title_short,2) = "条例" ;

41:规定;
update law_rule_result_article set law_grade = "41" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and right(title_short,2) = "规定" ;

42:办法;
update law_rule_result_article set law_grade = "42" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and right(title_short,2) = "办法" ;

43:通知、意见、命令、批复等；
update law_rule_result_article set law_grade = "43" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and law_grade is null ;


select right(title_short,2),count(*) from law_rule_result_article where 
cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" 
 group by right(title_short,2) order by count(*) desc ;

通知	261406
批复	54763
意见	24408
办法	18313
规定	9269
决定	7499
通告	7105
通报	5864
复函	5423
效]	5079
公告	3582
的函	3324
号）	1874
细则	1574
方案	900
条例	814
试行	788
修订	763
行）	665
知》	566
2)	511
报告	460
决议	452
公报	419
认证	409
号)	313
规则	294
订)	250
5)	221
制度	214
答复	209
标准	198
4)	187

select count(*) from law_rule_result_article where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库") and title_short like "%条例" limit 100;


select * from law_rule_result_article where cate_a = "国务院行政法规库" and title_short like "%条例" limit 100;
select * from law_rule_result_article where cate_a = "国务院行政法规库" and title_short like "%规定" limit 100;
select * from law_rule_result_article where cate_a = "国务院行政法规库" and title_short like "%办法" limit 100;

select * from law_rule_result_article where cate_a = "国务院行政法规库" and title_short not like "%规定"  
and title_short not like "%条例" and title_short not like "%办法" limit 100;


select * from law_rule_result_article where cate_a = "全国人大法律库"  and department != "国务院" 
select * from law_rule_result_article where article like "%关联法规%" limit 100;
select * from law_rule_result2 where art like "%关联法规：%" limit 100;

update mt2 set name = replace(name,
substring(name, locate('<contact>', name),locate('</contact>', name)-locate('<contact>'+10, name)),
''); 

1、去掉"关联法规"字样：

-- select art,replace(art,substr(art,locate('关联法规：',art)),"") from law_rule_result2 where art like "%关联法规%" limit 100;
-- select count(*) from  law_rule_result2 where art like "%关联法规%" ;
-- 69370

update law_rule_result2 set art = replace(art,substr(art,locate('关联法规：',art)),"") where art like "%关联法规%" ;

2、处理更新law_rule_article中的law_grade字段到law_rule_result2表中：

update law_rule_result2 a  
join 
law_rule_result_article b 
on 
a.law_id = b.law_id set a.law_grade= b.law_grade;

update law_rule_result2 a  
join 
law_rule_result_article b 
on 
a.law_id = b.law_id set a.law_grade= b.law_grade where b.cate_a = "全国人大法律库"  and b.department = "国务院" ;


update law_rule_result2 a  
join 
law_rule_result_article b 
on 
a.law_id = b.law_id set a.law_grade= b.law_grade where b.law_id in ("374465","114077")



select * from law_rule_result2 where law_grade is null or law_grade = "";

select * from law_rule_result2 where art_digit is null;
select * from law_rule_result2 where id > 2881120 and  id < 2881180;
select * from law_rule_result2 where id > 2880850 and  id < 2880900;  #2880886以该id为准，后面的都是新爬取的数据。

create table law_rule_result2_add2 as 
select * from law_rule_result2 where id > 2880886 ;


select * from law_rule_result2 where law_id = "139" ;


select * from law_rule_result2 where CHAR_LENGTH(law_id) > 6 or (CHAR_LENGTH(law_id) = 6 and law_id > "609664");


select * from law_rule_result_article where law_grade is null or law_grade = "";
select * from law_rule_result_article where law_id = 374465;
update law_rule_result_article set law_grade = "10" where law_id = "374465";
update law_rule_result_article set law_grade = "14" where law_id = "114077";
