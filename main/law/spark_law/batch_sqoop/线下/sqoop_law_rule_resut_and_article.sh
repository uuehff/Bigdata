sqoop import --connect jdbc:mysql://cdh5-slave3:3306/law --username weiwc --password HHly2017. \
 --query 'select * from law_rule_result2 where $CONDITIONS  ' \
 -m 60 --target-dir /user/weiwc/tb_doc_result --split-by id --hbase-table laws_doc:law_rule_result2 \
 --hbase-row-key lawlist_id  --column-family d --hbase-create-table --hbase-bulkload


 sqoop import --connect jdbc:mysql://cdh5-slave3:3306/law --username weiwc --password HHly2017. \
 --query 'select * from law_rule_result_article where $CONDITIONS  ' \
 -m 60 --target-dir /user/weiwc/tb_doc_article --split-by id --hbase-table laws_doc:law_rule_result_article \
 --hbase-row-key id  --column-family d --hbase-create-table --hbase-bulkload
