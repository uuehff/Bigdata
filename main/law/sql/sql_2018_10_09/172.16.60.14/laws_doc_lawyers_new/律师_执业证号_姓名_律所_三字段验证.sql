1）pra_number: 查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_12348gov_v3 where pra_number REGEXP '[a-zA-Z 	,:;-\\()!+@.|"\'/]|\\?|\\]|\\[' 
or hex(pra_number) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


2）name：查询*，可以直接在查询结果中修改
SELECT * from hht_lawyer_12348gov_v3 where name REGEXP '[a-z0-9A-Z 	,:;-\\()!+@|"\'/]|\\?|\\]|\\[' 
or hex(name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';


3）org_name：

update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"（","(");
update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"）",")");

带中文（）和()的正则来匹配
SELECT * from hht_lawyer_12348gov_v3 where org_name REGEXP '[a-z0-9A-Z ,:;-\\()+!@.|"\'/]|\\?|\\]|\\[' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

带中文（）不带()的正则来匹配
SELECT * from hht_lawyer_12348gov_v3 where org_name REGEXP '[a-z0-9A-Z ,:;-\\+!@.|"\'/]|\\?|\\]|\\[' 
or hex(org_name) REGEXP 'efbc8c|e38082|e38081|efbc9a|efbc9b|efbc9f|efbc81|e28098|e28099|efbc88|efbc89';

省市县区：e79c81|e5b882|e58ebf|e58cba


-- select * from hht_lawyer_12348gov_v3 where name like "%	%"
update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"（","(");
update hht_lawyer_12348gov_v3 set org_name = replace(org_name,"）",")");