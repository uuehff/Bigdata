reg_part = re.compile(r'<span litigantpart></span>')  # <a type='dir' name='DSRXX'></a>, 当事人信息
reg_process = re.compile(r'<span proceeding></span>')  # <a type='dir' name='SSJL'></a>，审理过程
reg_argued = re.compile(r'<span argued></span>')  # <a type='dir' name='AJJBQK'></a> ，诉讼请求,案件基本情况
reg_fact = re.compile(r'<span fact></span>')                                         #法院查明
reg_court = re.compile(r'<span courtconsider></span>')  # <a type='dir' name='CPYZ'></a> #法院认为
reg_result = re.compile(r'<span result></span>')     #<a type='dir' name='PJJG'></a>    #判决结果
# doc_footer                                       #<a type='dir' name='WBWB'></a>

select doc_content from t4 where case_type = "执行案件" and doc_content like "%DSRXX%" and doc_content like "%PJJG%"

分类统计：

select reason_type,judge_type,type,count(*) from judgment_zhangye_join_all group by reason_type,judge_type,type;
+--------------+------------+-----------------------------------------------+----------+
| reason_type  | judge_type | type                                          | count(*) |
+--------------+------------+-----------------------------------------------+----------+
| 刑事案件     |            | 一审                                          |    22206 |
| 刑事案件     |            | 二审                                          |     4764 |
| 刑事案件     |            | 其他                                          |     2045 |
| 刑事案件     |            | 再审                                          |       77 |
| 刑事案件     |            | 再审审查与审判监督                            |      383 |
| 刑事案件     |            | 减刑                                          |        1 |
| 刑事案件     |            | 刑罚变更                                      |     1755 |
| 刑事案件     |            | 司法赔偿                                      |        1 |
| 刑事案件     |            | 复核                                          |      354 |
| 刑事案件     |            | 审查监督                                      |        2 |
| 刑事案件     |            | 强制医疗                                      |       56 |
| 刑事案件     |            | 执行实施类                                    |        5 |
| 刑事案件     |            | 申诉                                          |        1 |
| 刑事案件     |            | 申请没收违法所得                              |        1 |
| 刑事案件     |            | 管辖                                          |     1486 |
| 刑事案件     |            | 非诉执行审查                                  |        3 |
| 刑事案件     | 决定       | 一审                                          |     1959 |
| 刑事案件     | 决定       | 二审                                          |       26 |
| 刑事案件     | 决定       | 其他                                          |     4931 |
| 刑事案件     | 决定       | 再审                                          |      153 |
| 刑事案件     | 决定       | 再审审查与审判监督                            |      664 |
| 刑事案件     | 决定       | 刑罚变更                                      |     2968 |
| 刑事案件     | 决定       | 复核                                          |        5 |
| 刑事案件     | 决定       | 强制医疗                                      |       75 |
| 刑事案件     | 决定       | 特别程序                                      |        1 |
| 刑事案件     | 决定       | 管辖                                          |      474 |
| 刑事案件     | 决定       | 非诉执行审查                                  |        1 |
| 刑事案件     | 判决       | 一审                                          |   151936 |
| 刑事案件     | 判决       | 二审                                          |    10506 |
| 刑事案件     | 判决       | 其他                                          |      322 |
| 刑事案件     | 判决       | 再审                                          |     1628 |
| 刑事案件     | 判决       | 再审审查与审判监督                            |       86 |
| 刑事案件     | 判决       | 刑罚变更                                      |       34 |
| 刑事案件     | 判决       | 复核                                          |        9 |
| 刑事案件     | 判决       | 强制医疗                                      |        8 |
| 刑事案件     | 判决       | 管辖                                          |        2 |
| 刑事案件     | 裁定       | 一审                                          |    11755 |
| 刑事案件     | 裁定       | 二审                                          |    37883 |
| 刑事案件     | 裁定       | 其他                                          |     3297 |
| 刑事案件     | 裁定       | 再审                                          |      220 |
| 刑事案件     | 裁定       | 再审审查与审判监督                            |      163 |
| 刑事案件     | 裁定       | 刑法变更                                      |       12 |
| 刑事案件     | 裁定       | 刑罚变更                                      |   243734 |
| 刑事案件     | 裁定       | 复核                                          |      370 |
| 刑事案件     | 裁定       | 强制医疗                                      |        5 |
| 刑事案件     | 裁定       | 管辖                                          |       25 |
| 刑事案件     | 调解       | 一审                                          |     1043 |
| 刑事案件     | 调解       | 二审                                          |      156 |
| 刑事案件     | 调解       | 其他                                          |        1 |
| 刑事案件     | 调解       | 再审                                          |        3 |
| 刑事案件     | 调解       | 再审审查与审判监督                            |        1 |
| 刑事案件     | 通知       | 一审                                          |      208 |
| 刑事案件     | 通知       | 二审                                          |       40 |
| 刑事案件     | 通知       | 其他                                          |     6584 |
| 刑事案件     | 通知       | 再审                                          |     1017 |
| 刑事案件     | 通知       | 再审审查与审判监督                            |     3560 |
| 刑事案件     | 通知       | 刑罚变更                                      |       97 |
| 刑事案件     | 通知       | 复核                                          |        1 |
| 刑事案件     | 通知       | 申诉、申请再审                                |       29 |
| 刑事案件     | 通知       | 管辖                                          |       16 |
| 执行案件     |            |                                               |   175533 |
| 执行案件     | 决定       |                                               |    34887 |
| 执行案件     | 判决       |                                               |     1507 |
| 执行案件     | 裁定       |                                               |  1182814 |
| 执行案件     | 调解       |                                               |      250 |
| 执行案件     | 通知       |                                               |   132166 |
| 民事案件     |            | 1                                             |        5 |
| 民事案件     |            | 14                                            |        9 |
| 民事案件     |            | 一审                                          |   685873 |
| 民事案件     |            | 二审                                          |    30917 |
| 民事案件     |            | 催告                                          |       28 |
| 民事案件     |            | 其他                                          |    32835 |
| 民事案件     |            | 再审                                          |      676 |
| 民事案件     |            | 再审审查与审判监督                            |      917 |
| 民事案件     |            | 再审审查和审判监督                            |        1 |
| 民事案件     |            | 司法赔偿                                      |        9 |
| 民事案件     |            | 审判监督                                      |        1 |
| 民事案件     |            | 强制清算                                      |        1 |
| 民事案件     |            | 执行实施类                                    |       16 |
| 民事案件     |            | 无                                            |       19 |
| 民事案件     |            | 特别程序                                      |    13315 |
| 民事案件     |            | 特别程序：确认调解                            |        3 |
| 民事案件     |            | 特殊程序：其他民事特殊程序                    |       37 |
| 民事案件     |            | 督促                                          |      703 |
| 民事案件     |            | 督促程序(支付令)                              |       18 |
| 民事案件     |            | 破产                                          |       16 |
| 民事案件     |            | 第三人撤销之诉                                |        5 |
| 民事案件     |            | 管辖                                          |      579 |
| 民事案件     | 决定       | 一审                                          |      492 |
| 民事案件     | 决定       | 二审                                          |       21 |
| 民事案件     | 决定       | 其他                                          |     1724 |
| 民事案件     | 决定       | 再审                                          |       15 |
| 民事案件     | 决定       | 再审审查与审判监督                            |      253 |
| 民事案件     | 决定       | 再审审查和审判监督                            |        1 |
| 民事案件     | 决定       | 司法赔偿                                      |        4 |
| 民事案件     | 决定       | 执行实施类                                    |       13 |
| 民事案件     | 决定       | 特别程序                                      |      146 |
| 民事案件     | 决定       | 督促                                          |        1 |
| 民事案件     | 决定       | 管辖                                          |       87 |
| 民事案件     | 判决       |                                               |        1 |
| 民事案件     | 判决       | 一审                                          |   432907 |
| 民事案件     | 判决       | 二审                                          |    88413 |
| 民事案件     | 判决       | 催告                                          |        5 |
| 民事案件     | 判决       | 其他                                          |     5233 |
| 民事案件     | 判决       | 再审                                          |     1924 |
| 民事案件     | 判决       | 再审审查与审判监督                            |       51 |
| 民事案件     | 判决       | 特别程序                                      |      459 |
| 民事案件     | 判决       | 特殊程序：其他民事特殊程序                    |        2 |
| 民事案件     | 判决       | 第三人撤销之诉                                |        6 |
| 民事案件     | 判决       | 管辖                                          |        6 |
| 民事案件     | 裁定       |                                               |        1 |
| 民事案件     | 裁定       | 一审                                          |   324250 |
| 民事案件     | 裁定       | 二审                                          |    47123 |
| 民事案件     | 裁定       | 催告                                          |       10 |
| 民事案件     | 裁定       | 其他                                          |    67193 |
| 民事案件     | 裁定       | 再审                                          |     1188 |
| 民事案件     | 裁定       | 再审审查与审判监督                            |    16538 |
| 民事案件     | 裁定       | 再审审查和审判监督                            |        1 |
| 民事案件     | 裁定       | 执行                                          |        2 |
| 民事案件     | 裁定       | 执行实施类                                    |       10 |
| 民事案件     | 裁定       | 特别                                          |        1 |
| 民事案件     | 裁定       | 特别程序                                      |    32131 |
| 民事案件     | 裁定       | 特殊程序：其他民事案件特殊程序                |        5 |
| 民事案件     | 裁定       | 特殊程序：其他民事特殊程序                    |       57 |
| 民事案件     | 裁定       | 申诉、申请再审                                |        4 |
| 民事案件     | 裁定       | 督促                                          |      221 |
| 民事案件     | 裁定       | 破产                                          |       18 |
| 民事案件     | 裁定       | 第三人撤销之诉                                |        5 |
| 民事案件     | 裁定       | 管辖                                          |      260 |
| 民事案件     | 调解       | 一审                                          |   574080 |
| 民事案件     | 调解       | 二审                                          |    32726 |
| 民事案件     | 调解       | 其他                                          |      574 |
| 民事案件     | 调解       | 再审                                          |      916 |
| 民事案件     | 调解       | 再审审查与审判监督                            |       46 |
| 民事案件     | 调解       | 执行实施类                                    |        1 |
| 民事案件     | 调解       | 民事特殊程序                                  |        1 |
| 民事案件     | 调解       | 特别程序                                      |     1401 |
| 民事案件     | 调解       | 第三人撤销之诉                                |        6 |
| 民事案件     | 调解       | 管辖                                          |       12 |
| 民事案件     | 通知       | 一审                                          |     1925 |
| 民事案件     | 通知       | 二审                                          |       25 |
| 民事案件     | 通知       | 催告                                          |        1 |
| 民事案件     | 通知       | 其他                                          |      628 |
| 民事案件     | 通知       | 再审                                          |       26 |
| 民事案件     | 通知       | 再审审查与审判监督                            |      371 |
| 民事案件     | 通知       | 司法赔偿                                      |       18 |
| 民事案件     | 通知       | 执行实施类                                    |        1 |
| 民事案件     | 通知       | 特别程序                                      |        9 |
| 民事案件     | 通知       | 管辖                                          |        1 |
| 行政案件     |            | 5                                             |       18 |
| 行政案件     |            | 一审                                          |     4596 |
| 行政案件     |            | 二审                                          |     1047 |
| 行政案件     |            | 其他                                          |      231 |
| 行政案件     |            | 再审                                          |       71 |
| 行政案件     |            | 再审审查与审判监督                            |       17 |
| 行政案件     |            | 执行实施类                                    |        4 |
| 行政案件     |            | 执行审查类                                    |       10 |
| 行政案件     |            | 管辖                                          |      178 |
| 行政案件     |            | 非诉执行审查                                  |     6104 |
| 行政案件     | 决定       | 一审                                          |       16 |
| 行政案件     | 决定       | 二审                                          |        7 |
| 行政案件     | 决定       | 其他                                          |      183 |
| 行政案件     | 决定       | 再审                                          |        3 |
| 行政案件     | 决定       | 司法赔偿                                      |        1 |
| 行政案件     | 决定       | 执行审查类                                    |        1 |
| 行政案件     | 决定       | 管辖                                          |        5 |
| 行政案件     | 决定       | 非诉执行审查                                  |        9 |
| 行政案件     | 判决       | 一审                                          |    35239 |
| 行政案件     | 判决       | 二审                                          |    28467 |
| 行政案件     | 判决       | 其他                                          |       34 |
| 行政案件     | 判决       | 再审                                          |      279 |
| 行政案件     | 判决       | 再审审查与审判监督                            |        6 |
| 行政案件     | 判决       | 非诉执行审查                                  |       98 |
| 行政案件     | 裁定       | 一审                                          |    51741 |
| 行政案件     | 裁定       | 二审                                          |    29145 |
| 行政案件     | 裁定       | 其他                                          |     5531 |
| 行政案件     | 裁定       | 再审                                          |     3561 |
| 行政案件     | 裁定       | 再审审查与审判监督                            |     4360 |
| 行政案件     | 裁定       | 执行                                          |       71 |
| 行政案件     | 裁定       | 执行实施类                                    |        6 |
| 行政案件     | 裁定       | 执行审查类                                    |      110 |
| 行政案件     | 裁定       | 管辖                                          |       29 |
| 行政案件     | 裁定       | 非诉执行审查                                  |    76871 |
| 行政案件     | 调解       | 一审                                          |      730 |
| 行政案件     | 调解       | 二审                                          |       51 |
| 行政案件     | 调解       | 其他                                          |        2 |
| 行政案件     | 调解       | 再审                                          |        1 |
| 行政案件     | 调解       | 非诉执行审查                                  |       13 |
| 行政案件     | 通知       | 一审                                          |      161 |
| 行政案件     | 通知       | 其他                                          |      138 |
| 行政案件     | 通知       | 再审                                          |      876 |
| 行政案件     | 通知       | 再审审查与审判监督                            |     1024 |
| 行政案件     | 通知       | 执行实施类                                    |        4 |
| 行政案件     | 通知       | 非诉执行审查                                  |       11 |
| 赔偿案件     |            |                                               |       80 |
| 赔偿案件     |            | 一审                                          |      185 |
| 赔偿案件     |            | 二审                                          |       13 |
| 赔偿案件     |            | 其他                                          |       34 |
| 赔偿案件     |            | 再审                                          |        3 |
| 赔偿案件     |            | 再审审查与审判监督                            |       46 |
| 赔偿案件     |            | 司法赔偿                                      |       80 |
| 赔偿案件     |            | 管辖                                          |       16 |
| 赔偿案件     |            | 行政赔偿                                      |        9 |
| 赔偿案件     | 决定       |                                               |     4025 |
| 赔偿案件     | 决定       | 一??                                          |        1 |
| 赔偿案件     | 决定       | 一审                                          |       12 |
| 赔偿案件     | 决定       | 其他                                          |       24 |
| 赔偿案件     | 决定       | 再审                                          |        7 |
| 赔偿案件     | 决定       | 再审审查与审判监督                            |        8 |
| 赔偿案件     | 决定       | 司法赔偿                                      |      112 |
| 赔偿案件     | 决定       | 管辖                                          |       26 |
| 赔偿案件     | 决定       | 行政赔偿                                      |        8 |
| 赔偿案件     | 决定       | 赔偿                                          |       27 |
| 赔偿案件     | 判决       |                                               |     3000 |
| 赔偿案件     | 判决       | 一审                                          |       58 |
| 赔偿案件     | 判决       | 二审                                          |       34 |
| 赔偿案件     | 判决       | 其他                                          |        1 |
| 赔偿案件     | 判决       | 再审审查与审判监督                            |        1 |
| 赔偿案件     | 裁定       |                                               |     5419 |
| 赔偿案件     | 裁定       | 一审                                          |      120 |
| 赔偿案件     | 裁定       | 二审                                          |       15 |
| 赔偿案件     | 裁定       | 其他                                          |        3 |
| 赔偿案件     | 裁定       | 再审审查与审判监督                            |        7 |
| 赔偿案件     | 裁定       | 司法赔偿                                      |       19 |
| 赔偿案件     | 调解       |                                               |       34 |
| 赔偿案件     | 调解       | 一审                                          |       79 |
| 赔偿案件     | 调解       | 二审                                          |        3 |
| 赔偿案件     | 调解       | 再审                                          |        1 |
| 赔偿案件     | 调解       | 再审审查与审判监督                            |        1 |
| 赔偿案件     | 调解       | 非诉执行审查                                  |        1 |
| 赔偿案件     | 通知       |                                               |      926 |
| 赔偿案件     | 通知       | 一审                                          |        1 |
| 赔偿案件     | 通知       | 再审审查与审判监督                            |       83 |
| 赔偿案件     | 通知       | 司法赔偿                                      |        3 |
| 赔偿案件     | 通知       | 赔偿                                          |        1 |
+--------------+------------+-----------------------------------------------+----------+
张野爬取数据处理步骤：

create table judgment_zhangye_etl01 like judgment_zhangye_etl02;
create table judgment_zhangye_etl03 like judgment_zhangye_etl01;
create table judgment_zhangye_etl07 like judgment_zhangye_etl01;
create table judgment_zhangye_etl08 like judgment_zhangye_etl01;
create table judgment_zhangye_etl09 like judgment_zhangye_etl01;

spark_part_main_zhangye_update_ip-10-41-104-5_wenshu.py 分段处理后，

结果上传线上，以及judgment_doc也上传线上：

汇总分段结果：
insert into judgment_zhangye_etl01 select * from judgment_zhangye_etl02;
insert into judgment_zhangye_etl01 select * from judgment_zhangye_etl03;
insert into judgment_zhangye_etl01 select * from judgment_zhangye_etl04;
insert into judgment_zhangye_etl01 select * from judgment_zhangye_etl05;
insert into judgment_zhangye_etl01 select * from judgment_zhangye_etl06;

join分段汇总表和judgment_doc，从judgment_doc中补全title，caseid等等一般的字段，结果为judgment_zhangye_join_all：

spark-submit --master spark://cdh-master:7077  --driver-memory 8g  --executor-memory 100g judgment_zhangye_join_2018-05-25.py

alter table judgment_zhangye_join_all 
modify party_info longtext,
modify trial_process longtext,
modify trial_request longtext,
modify court_find longtext,
modify court_idea longtext,
modify judge_result longtext,
modify doc_footer longtext,
modify court longtext,
modify title longtext,
modify reason_type longtext,
modify caseid longtext,
modify type longtext,
modify casedate longtext,
modify judge_type longtext;

字段标准化处理：
update judgment_zhangye_join_all
set type =
case
when type = "一审" then "1"
when type = "二审" then "2"
when type = "再审" then "3"
when type = "其他" then "4"
when type = "再审审查与审判监督" then "5"
else '' end,
reason_type =
case reason_type
when "刑事案件" then "刑事"
when "民事案件" then "民事"
when "行政案件" then "行政"
when "执行案件" then "执行"
when "赔偿案件" then "赔偿"
else "" end;


处理另外两个表：
casedate_lawlist_court_reason_province-judgment_zhangye.py
judgment_zhangye_other_fields

lawlist_to_lawid_2018-05-27-judgment_zhangye_etl.py
judgment_zhangye_uuid_law_id


创建other_lawid，合并judgment_zhangye_other_fields和judgment_zhangye_uuid_law_id：

alter table judgment_zhangye_other_fields 
modify uuid varchar(40),
add unique index uuid(uuid);
======
alter table judgment_zhangye_uuid_law_id 
modify uuid varchar(40),
add unique index uuid(uuid);
======
create table other_lawid as select a.*,b.law_id from judgment_zhangye_other_fields a left join judgment_zhangye_uuid_law_id b  on a.uuid = b.uuid ;
======
alter table other_lawid 
modify uuid varchar(40),
add unique index uuid(uuid);

过滤四大类数据：

create table xinghshi_join as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_join_all a,other_lawid b where a.reason_type = "刑事" and a.uuid = b.uuid ;

create table minshi_join as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_join_all a,other_lawid b where a.reason_type = "民事" and a.uuid = b.uuid ;

create table xinghzheng_join as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_join_all a,other_lawid b where a.reason_type = "行政" and a.uuid = b.uuid ;


create table zhixing_join as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_join_all a,other_lawid b where a.reason_type = "执行" and a.uuid = b.uuid ;

=================================================================
第二次更新，大概180万：id从4816521开始：  judgment表id最大为：6532764
select count(*) from judgment where id > 4816521;   # 1716242


创建laws_doc_zhangye_update2：
create table judgment_zhangye_add180wan_etl01 like laws_doc_zhangye_update1.judgment_zhangye_etl01;
create table judgment_zhangye_add180wan_etl02 like laws_doc_zhangye_update1.judgment_zhangye_etl01;
spark_part_main_zhangye_add180wan_wenshu.py 分段处理后，

结果上传线上，汇总分段结果：
insert into judgment_zhangye_etl01 select * from judgment_zhangye_etl02;


join分段汇总表和laws_doc_update1中的judgment_doc，从judgment_doc中补全title，caseid等等一般的字段，结果为judgment_zhangye_180wan_join_all：

create table judgment_zhangye_180wan_join_all like laws_doc_zhangye_update1.judgment_zhangye_join_all;
-- alter table judgment_zhangye_180wan_join_all 
-- modify party_info longtext,
-- modify trial_process longtext,
-- modify trial_request longtext,
-- modify court_find longtext,
-- modify court_idea longtext,
-- modify judge_result longtext,
-- modify doc_footer longtext,
-- modify court longtext,
-- modify title longtext,
-- modify reason_type longtext,
-- modify caseid longtext,
-- modify type longtext,
-- modify casedate longtext,
-- modify judge_type longtext;

spark-submit --master spark://cdh-master:7077  --driver-memory 8g  --executor-memory 100g judgment_zhangye_join_2018-06-04.py

字段标准化处理：
update judgment_zhangye_180wan_join_all
set type =
case
when type = "一审" then "1"
when type = "二审" then "2"
when type = "再审" then "3"
when type = "其他" then "4"
when type = "再审审查与审判监督" then "5"
else '' end,
reason_type =
case reason_type
when "刑事案件" then "刑事"
when "民事案件" then "民事"
when "行政案件" then "行政"
when "执行案件" then "执行"
when "赔偿案件" then "赔偿"
else "" end;


处理另外两个表：
casedate_lawlist_court_reason_province-judgment_add180wan_zhangye.py
judgment_zhangye_180wan_other_fields

lawlist_to_lawid_2018-05-27-judgment_add180wan_zhangye_etl.py
judgment_add180wan_zhangye_uuid_law_id


创建other_lawid，合并judgment_zhangye_180wan_other_fields和judgment_add180wan_zhangye_uuid_law_id：

alter table judgment_zhangye_180wan_other_fields 
modify uuid varchar(40),
add unique index uuid(uuid);
======
alter table judgment_add180wan_zhangye_uuid_law_id 
modify uuid varchar(40),
add unique index uuid(uuid);
======
create table other_lawid_180wan as select a.*,b.law_id from judgment_zhangye_180wan_other_fields a left join judgment_add180wan_zhangye_uuid_law_id b  on a.uuid = b.uuid ;

alter table other_lawid_180wan 
modify uuid varchar(40),
add unique index uuid(uuid);

过滤四大类数据：

create table xinghshi_join_add180wan as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_180wan_join_all a,other_lawid_180wan b where a.reason_type = "刑事" and a.uuid = b.uuid ;

create table minshi_join_add180wan as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_180wan_join_all a,other_lawid_180wan b where a.reason_type = "民事" and a.uuid = b.uuid ;

create table xinghzheng_join_add180wan as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_180wan_join_all a,other_lawid_180wan b where a.reason_type = "行政" and a.uuid = b.uuid ;

create table zhixing_join_add180wan as select a.*,b.reason,b.reason_uid,
b.plt_claim,b.dft_rep,b.crs_exm,b.lawlist,b.province,
b.court_uid,b.law_id from judgment_zhangye_180wan_join_all a,other_lawid_180wan b where a.reason_type = "执行" and a.uuid = b.uuid ;

================================================================================
update uuid_type_all
set type =
case
when jud_pro = "一审" then "1"
when jud_pro = "二审" then "2"
when jud_pro = "再审" then "3"
when jud_pro = "" then ""
when jud_pro = "再审审查与审判监督" then "5"
when jud_pro = "非诉执行审查" then "6"
when jud_pro = "复核" then "7"
when jud_pro = "刑罚变更" then "8"
else "4" end;




