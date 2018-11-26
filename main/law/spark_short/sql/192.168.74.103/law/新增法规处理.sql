create table law_id_tmp as select law_id from law_rule_result2_add group by law_id ;
update law_id_tmp set id = id + 609665;

-- select * from law_id_tmp where law_id is null or law_id = "";
update law_rule_result2_add a join law_id_tmp b on a.law_id = b.law_id set a.law_id = b.id;

update law_rule_result2_add set lawlist_id = CONCAT_WS("",law_id,LPAD(art_digit,4,0));

update law_rule_result2_add a join law_rule_result2_add2 b on 
a.id = b.id set 
a.art_num = b.art_num,
a.title_long = b.title_long,
a.error = b.error,
a.insert_time = b.insert_time,
a.doc_num = b.doc_num;

update law_rule_result2_add_article set id = id + 609663;


update law_rule_result2_add_article a,law_area_uid_add b 
set a.city = b.city,
a.area_uid = b.area_uid where a.law_id = b.law_id;

update law_rule_result2_add_article set area_uid = "00" where  area = "全国";

update law_rule_result2_add a,law_rule_result2_add_article b 
set a.city = b.city,
a.area_uid = b.area_uid,
a.law_grade = b.law_grade where a.law_id = b.law_id;


insert into law_rule_result_article select * from law_rule_result2_add_article;

create table law_rule_result2_add2 as 
select * from law_rule_result2 where id > 2880886 ;

delete from law_rule_result2 where id > 2880886 ;
insert into law_rule_result2 select * from law_rule_result2_add;


select * from law_rule_result_article where 
article like "%关联法规%" and article not like "%关联法规：%" limit 100;

select * from law_rule_result_article where article like "%关联法规%" limit 100;
select * from law_rule_result_article where article is null or article = "";
update law_rule_result2 set art = replace(art,"关联法规......","") where id in (197729,215409,2772700)
select *  from law_rule_result2  where id in (197729,215409,2772700)

1、除去art字段的：关联法规；
update law_rule_result_article set art = replace(art,substr(art,locate('关联法规',art)),"") where art like "%关联法规%" ;
2、程序除掉article字段的关联法规；
update law_rule_result_article set 
article = replace(article,"关联法规......","") 
where id in (191754,580355)

update law_rule_result_article a join law_rule_result2_article_article_fields b
on a.id = b.id set a.article = b.article;


===============
更新等级字段：
10: 中华人民共和国**法；
-- select * from law_rule_result2_add_article where cate_a = "全国人大法律库"  and department != "国务院" and title_short like "中华人民共和国%法%" and title_short not like "%办法";
update  law_rule_result2_add_article  set law_grade = "10" where cate_a = "全国人大法律库"  and 
department != "国务院" and title_short like "中华人民共和国%法%" and title_short not like "%办法";


11:条例;
update  law_rule_result2_add_article  set law_grade = "11" where cate_a = "全国人大法律库"  and 
department != "国务院" and right(title_short,2) = "条例";

12:规定;
update  law_rule_result2_add_article  set law_grade = "12" where cate_a = "全国人大法律库"  and 
department != "国务院" and right(title_short,2) = "规定";

13:办法;
update  law_rule_result2_add_article  set law_grade = "13" where cate_a = "全国人大法律库"  and 
department != "国务院" and right(title_short,2) = "办法";

14:通知、意见、命令、批复、**决定，决议，公告，意见等；
update  law_rule_result2_add_article  set law_grade = "14" where cate_a = "全国人大法律库"  and 
department != "国务院" and law_grade is null;

2、行政法规：
-- select * from law_rule_result2_add_article where cate_a = "国务院行政法规库" ;
20:条例;
update  law_rule_result2_add_article set law_grade = "20" where cate_a = "国务院行政法规库" and right(title_short,2) = "条例" ;
update  law_rule_result2_add_article  set law_grade = "20" where 
cate_a = "全国人大法律库"  and department = "国务院" and right(title_short,2) = "条例" ;

-- select * from law_rule_result2_add_article where cate_a = "全国人大法律库"  and department= "国务院";

21:规定;
update  law_rule_result2_add_article set law_grade = "21" where cate_a = "国务院行政法规库" and right(title_short,2) = "规定" ;
update  law_rule_result2_add_article  set law_grade = "21" where 
cate_a = "全国人大法律库"  and department = "国务院" and right(title_short,2) = "规定" ;

22:办法;
update  law_rule_result2_add_article set law_grade = "22" where cate_a = "国务院行政法规库" and right(title_short,2) = "办法" ;
update  law_rule_result2_add_article  set law_grade = "22" where 
cate_a = "全国人大法律库"  and department = "国务院" and right(title_short,2) = "办法" ;
23:通知、意见、命令、批复等；
update  law_rule_result2_add_article set law_grade = "23" where cate_a = "国务院行政法规库" and law_grade is null; ;
update  law_rule_result2_add_article  set law_grade = "23" where 
cate_a = "全国人大法律库"  and department = "国务院" and law_grade is null;


3、部门规章：select * from law_rule_result2_add_article where 
cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库"
 limit 100;


-- select * from law_rule_result2_add_article where (cate_a = "国务院部委规章库" or cate_a = "国家规范性文件库" or cate_a = "团体、行业规范库" ) and title_short like "%条例" limit 100;
-- select * from law_rule_result2_add_article where (cate_a = "国务院部委规章库" or cate_a = "国家规范性文件库" or cate_a = "团体、行业规范库" ) and title_short like "%规定" limit 100;
-- select * from law_rule_result2_add_article where (cate_a = "国务院部委规章库" or cate_a = "国家规范性文件库" or cate_a = "团体、行业规范库" ) and title_short like "%办法" limit 100;
30:条例;
update law_rule_result2_add_article set law_grade = "30" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and right(title_short,2) = "条例" ;
31:规定;
update law_rule_result2_add_article set law_grade = "31" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and right(title_short,2) = "规定" ;
32:办法;
update law_rule_result2_add_article set law_grade = "32" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and right(title_short,2) = "办法" ;
33:通知、意见、命令、批复等；
update law_rule_result2_add_article set law_grade = "33" where 
(cate_a = "国务院部委规章库" 
or cate_a = "国家规范性文件库" 
or cate_a = "团体、行业规范库" 
or cate_a = "立法、司法解释库"
or cate_a = "军事法规库"
or cate_a = "国际法、国际条约与惯例库"
or cate_a = "地方人大法规库") and law_grade is null ;


4、地方政府规章：

select * from law_rule_result2_add_article where 
cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" 
limit 200;
40:条例;
update law_rule_result2_add_article set law_grade = "40" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and right(title_short,2) = "条例" ;

41:规定;
update law_rule_result2_add_article set law_grade = "41" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and right(title_short,2) = "规定" ;

42:办法;
update law_rule_result2_add_article set law_grade = "42" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and right(title_short,2) = "办法" ;

43:通知、意见、命令、批复等；
update law_rule_result2_add_article set law_grade = "43" where 
(cate_a = "地方规范性文件库" 
or cate_a = "地方政府规章库" 
or cate_a = "地方司法规范库" ) and law_grade is null ;


select * from law_rule_result_article where title_short like "%中华人民共和国宪法%"

create table law_rule_result_article_1w as 
SELECT * from law_rule_result_article order by law_grade limit 10000

SELECT * from law_rule_result_article where law_grade = "10"


SELECT * from law_rule_result_article where law_id = "615895"
SELECT * from law_rule_result_article where law_id = "615895"
SELECT * from law_rule_result2 where law_id = "615895"
SELECT count(*) from law_rule_result2 where error = "";
2727729
2636861




