已处理：行政
执行
其他执行（除了通知书）
adjudication表


处理新增合同以外600万：



select doc_from,count(*) from administration group by doc_from; 
wenshu-gov	550541

select * from administration where id = 312840
select * from administration where uuid = "04c49178-6a0a-4019-8f20-a85600d7103a"
select doc_content from administration where id in (select id from administration_pri_reason_id)
select count(*) from administration where is_crawl = 1
550541
select * from administration where judge_result is null limit 100;

select reason_type,judge_type,type,count(*) from administration group by reason_type,judge_type,type
行政	判决		247986
行政	裁定		302555

select reason_type,judge_type,type,count(*) from implement group by reason_type,judge_type,type

其他执行案件	裁定		145
刑事执行	裁定		1221510
民事执行	裁定		218970
行政执行	裁定		678985

select count(*) from implement where is_crawl = 1
2076031
select doc_content,count(*) from implement where is_crawl != 1 group by doc_content
NULL	43579
select reason_type,judge_type,type,count(*) from imp_other group by reason_type,judge_type,type
其他执行	裁定		218071
其他执行案件	决定		53085
其他执行案件	裁定		4302716
其他执行案件	通知		159976
select count(*) from imp_other where is_crawl = 1
4532200
select * from imp_other where is_crawl != 1 and doc_content is not null limit 100;
NULL

select * from imp_other where judge_type = "通知" or judge_type = "决定" limit 200;
select * from imp_other where id in (1578586,1578587,1578588)


select reason_type,judge_type,type,count(*) from adjudication group by reason_type,judge_type,type
刑事	裁定		309492
民事	裁定		3569577
select count(*) from adjudication where id < 500 and doc_from = "wenshu"

select count(*) from adjudication where is_crawl = 1 ;
3878998
3569487
select * from adjudication where is_crawl != 1 and doc_content is not null limit 100;
NULL
select * from adjudication where is_format = 3  #分段不成功，涉及到文书内容不宜公开的。
NULL
select reason_type,judge_type,type,count(*) from judgment group by reason_type,judge_type,type
22上，除合同以外：
民事	判决		795763
民事	判决	一审	3923348
民事	判决	二审	897437
民事	判决	其他	1900
民事	判决	再审	17971

select * from judgment where is_crawl = 1 and doc_content is null limit 100;
select * from judgment where is_format = 3



select type,reason_type,judge_type,count(*) from adjudication_xingshi_etl group by type,reason_type,judge_type
	刑事	裁定	309492
	民事	裁定	309492

select reason_type,judge_type,type,count(*) from mediate group by reason_type,judge_type,type
民事	调解		131606

=====================================================
74.102上刑事，judgment：
select reason_type,judge_type,type,doc_from,count(*) as t from judgment 
group by reason_type,judge_type,type,doc_from order by count(*) desc 

刑事	判决书	0	wenshu-gov	2059998
刑事	判决	0	limai	1036779
盗窃罪||侵犯财产罪	判决书	0	legalminer_com	133026
危险驾驶罪||危害公共安全罪	判决书	0	legalminer_com	88513
刑事	判决书	0	legalminer_com	88099
故意伤害罪||侵犯人身权利、民主权利罪	判决书	0	legalminer_com	50051
走私、贩卖、运输、制造毒品罪||走私、贩卖、运输、制造毒品罪||妨害社会管理秩序罪	判决书	0	legalminer_com	45708
危害公共安全罪||交通肇事罪	判决书	0	legalminer_com	38609
容留他人吸毒罪||走私、贩卖、运输、制造毒品罪||妨害社会管理秩序罪	判决书	0	legalminer_com	19095
诈骗罪||侵犯财产罪	判决书	0	legalminer_com	18297
寻衅滋事罪||扰乱公共秩序罪||妨害社会管理秩序罪	判决书	0	legalminer_com	16442
故意伤害罪||侵犯人身权利、民主权利罪||刑事附带民事案件	判决书	0	legalminer_com	11914
扰乱公共秩序罪||开设赌场罪||妨害社会管理秩序罪	判决书	0	legalminer_com	10492
侵犯财产罪||抢劫罪	判决书	0	legalminer_com	9863
金融诈骗罪||破坏市场经济秩序罪||信用卡诈骗罪	判决书	0	legalminer_com	9319
扰乱公共秩序罪||民事案件||危害公共安全罪||交通肇事罪	判决书	0	legalminer_com	5102
非法持有、私藏妨害公务罪||妨害社会管理秩序罪	判决书	0	legalminer_com	6535
非法持有毒品罪||走私、贩卖、运输、制造毒品罪||妨害社会管理秩序罪	判决书	0	legalminer_com	5786
刑事附带枪支、弹药罪||危害公共安全罪	判决书	0	legalminer_com	4976
侵犯人身权利、民主权利罪||非法拘禁罪	判决书	0	legalminer_com	4898

这里省略部分查询结果，共有5162条，查询耗时1分钟。

经过查看具体数据，以下SQL执行结果，来源于文书网，可用DSRXX,WBSB等标签分割：
select * from judgment where reason_type = "刑事" and 
judge_type = "判决书" and doc_from = "wenshu-gov" limit 100

经过查看具体数据，以下三个SQL执行结果，来源于理脉，结构一样，可用litigantpart，fact,result等标签分割：
select * from judgment where reason_type = "刑事" and 
judge_type = "判决" and doc_from = "limai" limit 100


select * from judgment where reason_type = "刑事" and 
judge_type = "判决书" and doc_from = "legalminer_com" limit 100

select * from judgment where reason_type = "盗窃罪||侵犯财产罪" and 
judge_type = "判决书" and doc_from = "legalminer_com" limit 100

74.103上民事，judgment：
select reason_type,judge_type,type,doc_from,count(*) as t from judgment 
group by reason_type,judge_type,type,doc_from order by count(*) desc 
============================================================



线上统计：
民事：
mysql> select count(*) from judgment_civil_all;
+----------+
| count(*) |
+----------+
|  6717770 |

judgment_new: 5559381

mysql> select count(*) from adjudication_civil_etl;
+----------+
| count(*) |
+----------+
|  3569487 |

============================
mysql> select count(*) from judgment_add560wan_all;
+----------+
| count(*) |
+----------+
|  5584094 |

总计：15846638 + 5584094 = 21430732


刑事：
mysql> select count(*) from judgment_main_etl;
+----------+
| count(*) |
+----------+
|  2630629 |
mysql> select count(*) from judgment2_main_etl;
+----------+
| count(*) |
+----------+
|    40434 |
mysql> select count(*) from adjudication_xingshi_etl;
+----------+
| count(*) |
+----------+
|   309492 |

============================
mysql> select count(*) from judgment_add100wan_etl;
+----------+
| count(*) |
+----------+
|  1036775 |


总计：2980555 + 1036775 = 4017330

行政：
mysql> select count(*) from administration_etl;
+----------+
| count(*) |
+----------+
|   550479 |


总计：550479

执行：
mysql> select count(*) from implement_civil_etl;
+----------+
| count(*) |
+----------+
|  2076007 |
+----------+
mysql> select count(*) from imp_other_etl;
+----------+
| count(*) |
+----------+
|  4532184 |


总计：6608191


全部类型总计：25985863 + 5584094 + 1036775 = 32606732 + 4711424 = 37318156





