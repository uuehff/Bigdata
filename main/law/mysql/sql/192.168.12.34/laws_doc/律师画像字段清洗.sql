select id from laws_doc2.judgment2_visualization_v2  where degree is null limit 100;

create table lawyer_picture as select uuid,party_info from judgment_part_v2

update lawyer_picture set plaintiff_judge_result = '1' ,defendant_judge_result = '0' 

select id,name,uid from reason where level = "一级案由"

select count(*) from lawyer_picture where party_info like "%被告%公司%"  or party_info like "%原告%公司%"  # 93703

select * from lawyer_picture where party_info like "%被告%公司%"  or party_info like "%原告%公司%" 

select uuid,party_info from lawyer_picture where party_info like "%被告：%公司%" limit 1000
select uuid,party_info from lawyer_picture where party_info like "%原告%公司%" limit 1000
select uuid,party_info from lawyer_picture where party_info like "%原告：%公司%" limit 1000

select * from lawyer_picture where (plaintiff_company is not null or defendant_company is not null) and 
plaintiff_company != "" or defendant_company != ""   #18924


select count(*) from lawyer_picture where plaintiff_company like "%公司%" or defendant_company like "%公司%"

select * from lawyer_picture where plaintiff_company is not null and plaintiff_company != "" and  plaintiff_company like "单位%" #436

select * from lawyer_picture where defendant_company is not null and defendant_company != "" and defendant_company like "%单位%" #436

update lawyer_picture set plaintiff_company = TRIM(LEADING '单位' FROM plaintiff_company) where plaintiff_company is not null and plaintiff_company != "" and  plaintiff_company like "单位%"
update lawyer_picture set plaintiff_company = "" where plaintiff_company like "%×%"

update lawyer_picture set defendant_company = TRIM(LEADING '单位' FROM defendant_company) where defendant_company is not null and defendant_company != "" and  defendant_company like "单位%"
update lawyer_picture set defendant_company = "" where defendant_company like "%某%"


#就差被告多个公司前面“单位“关键字
update lawyer_picture set defendant_company =  where defendant_company like "%||%"


select * from lawyer_picture where id < 10 and reason_one like "%公[共民]%"

select * from lawyer_picture where party_info like "%人侯安到周口市公安局交警支队投案自首%"
select * from lawyer_picture where party_info like "%人左法建到郸城县公安局汲水派出所投案%"
select * from lawyer_picture where party_info like "%李凯乐因涉嫌故意伤害在深圳市宝安国际机场被深圳市公安局机场分局刑警大队抓获%"

select uuid,party_info from lawyer_picture where (party_info like "%被告%公司%"  or party_info like "%原告%公司%") and id = 1689378 

select * from lawyer_picture where id = 1689378 



附带民事诉讼被告：新疆新建旅客运输（集团）公司。
委托代理人：朱某
代理权限：特别代理
附带民事诉讼被告：新疆新建旅客运输（集团）公司额敏县分公司
委托代理人：梁某，律师
附带民事诉讼被告：中国大地财产保险股份有限公司阜新中心支公司，地址阜新市细河区迎宾大街中段宝典大厦。
==========
附带民事诉讼被告人天安财产保险股份有限公司江西省分公司。
附带民事诉讼被告中国人寿财产保险股份有限公司岳阳市中心支公司。
===========
附带民事诉讼被告：中国大地财产保险股份有限公司通城营销部（以下简称大地保险公司）。地址：湖北省咸宁市通城县隽水镇五里大道36号。
========
被告：华安财产保险股份有限公司吉林分公司，住所地：长春市朝阳区西安大路1688号。
=============
辩护人黄祖宝，广西桂中律师事务所律师。
刑事附带民事被告：广西来宾中兴汽车运输有限责任公司。
地址：来宾市兴宾区翠屏路西182号。
法定代表人覃国钧，该公司经理。
委托代理人樊恒德，忻城县中心法律服务所法律工作者。
刑事附带民事被告：广西来宾中兴汽车运输有限责任公司来宾汽车总站。
地址：来宾市兴宾区翠屏路西182号。
法定代表人莫文洪，经理。
委托代理人罗祖红。该公司员工。
刑事附带民事被告：中国人民财产保险股份有限公司来宾市分公司。
地址：来宾市中南路353号。
法定负责人龚振，该公司经理。
委托代理人谢雄躯，广西鹏程律师事务所律师。
刑事附带民事被告罗某，农民。
===============
附带民事诉讼被告人：赵西松。肇事冀B×××××号重型自卸车所有人。
============
自诉人暨附带民事诉讼原告：昆明某某某有限公司。
=附带民事诉讼原告人胡某甲，男，1945年1月7日出生，，汉族，农民，住招远市。系被害人胡某乙之父。
附带民事诉讼原告人胡某丙，男，2011年12月30日出生，，汉族，儿童，住址同上。系被害人胡某乙之子。
附带民事诉讼原告人暨原告人胡某丙的法定代理人杜某某，女，1986年5月10日出生，汉族，农民，住址同上。系被害人胡某乙之妻。
上述原告人的诉讼代理人梁前、刘彩菊，招远市开发法律服务所法律工作者。
======
原告：裕达建工集团有限公司，住所地广州市天河区。
法定代表人：宁永杰，董事长。
============
附带民事诉讼原告人××有限责任公司，住所××。
法定代表人王××，男，××年6月14日出生，汉族，系该公司经理，住××。
