======================================================
=======律师版本一处理流程：===========================
======================================================
1、原始数据来源于：
	1）爬取各地的律协、司法局律师数据（不完整）。
	2）文书（当时的280万文书）中提取，律师姓名，律所。
2、合并两部分原始数据，并去重（律师名称、律所一样的认为重复）。
3、得到70万律师数据，质量不高。

======================================================
=======律师版本二处理流程：===========================
======================================================
1、原始数据来源于：
	1）爬取法网数据。
	2）新爬取各省的律协、司法局律师数据。
2、合并处理两部分原始数据：流程如下：
1）删除律协数据中，律师名称、执业证号、律所任意一个为NULL或""的数据；如下：
	delete from hht_lawyer_gansu where pra_number = "" or pra_number is null;
	delete from hht_lawyer_gansu where name = "" or name is null;
	delete from hht_lawyer_gansu where org_name = "" or org_name is null;

2）使用正则统计、清洗律师名称、执业证号、律所三个字段,因为需要去重、合并，去重、合并都是围绕这三个字段，必须先处理，如下：
	1.清洗pra_number字段: 查询*，可以直接在查询结果中修改；
	SELECT * from hht_lawyer_12348gov_v3 where pra_number REGEXP '[a-zA-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
	or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
	2.清洗name字段：查询*，可以直接在查询结果中修改；
	SELECT * from hht_lawyer_12348gov_v3 where name REGEXP '[a-z0-9A-Z 	,:;\\()!+@.|"\'/]|\\?|\\]|\\[|\\-' 
	or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
	3.清洗org_name字段：先将（）字符统一为()；
	update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"（","(");
	update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"）",")");

	带中文（）的正则来匹配；
	SELECT * from hht_lawyer_12348gov_v4 where org_name REGEXP '[a-z0-9A-Z 	,:;\\+!@.|"\'/]|\\?|\\]|\\[|\\-' 
	or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';
3）法网数据新增一个source字段表示来源,便于和律协数据区分，保证所有表中同一字段的字段名称一致前提下，将所有表的数据导入到HBase,读取HBase，筛选需要的字段，
	将数据写出到一个新表中，字段名称与HBase保持一致；
	1.导入脚本：batch_sqoop_match.sh、tables_name_lawyers_origin；
	2.读取HBase写入Mysql：happybase_cdh_lawyers_match_to_mysql.py

4）去重，去重有几种情况：
	1.律师名称、执业证号、律所都一样；（主要是法网与律协之间的重复：代码lawyers_2018_09_07_hht_lawyer_all_collect_add_and_match_gov_v3_distinct.py）

	2.名称、执业证号一样，律所不一样；（可能是换律所，可参考代码：lawyers_2018_09_07_hht_lawyer_all_collect_add_and_match_result_pra_number_right_6_distinct.py）


	其中：2、3、4三个步骤中重复数据较少，可使用正则、sql，甚至手动合并，来处理。
	3.名称、律所一样的，执业证号不一样；（可能是录入错误或无效证号，可找出几个进行百查证等方式找出规律，
	具体根据真实数据进行取舍，如无法取舍，以法网为准，如果不包含法网数据，以17位且符合规则的为准）

	4.律所、执业证号一样，名称不一样的；（可能是录入错误或有大小名（包含个大字或小字等情况），可找出几个进行百查证或在文书网
	高级搜索中搜索律所和名字等方式找出规律，进行合并或删除，否则以法网为准，否则以统一的规则取舍）

	5.姓名一样、执业证号是标准的11位，且除了行政代码4位、执业类型1位不一样外，其他都一样，律所不一样；
	（这种是跨省或跨市执业或转执业类型，执业证号做了更改；代码：lawyers_2018_09_07_hht_lawyer_all_collect_add_and_match_result_pra_number_part_group.py）

	6.姓名一样、执业证号是标准的11位，且后6位一样的、律所不一样；
	（一般执业证号后6位是不变的，可能有其他原因造成的执业证号的前几位有变化，但可与姓名绑定进行去重；
	代码：lawyers_2018_09_07_hht_lawyer_all_collect_add_and_match_result_pra_number_right_6_distinct.py）


