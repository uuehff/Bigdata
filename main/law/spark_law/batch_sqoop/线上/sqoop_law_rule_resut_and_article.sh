sqoop import --connect jdbc:mysql://slave2:3306/law_v2 --username weiwc --password HHly2017. \
 --query 'select * from law_rule_result2 where $CONDITIONS and error = "" ' \
 -m 30 --target-dir /user/weiwc/tb_doc_result --split-by id --hbase-table laws_doc:law_rule_result2 \
 --hbase-row-key lawlist_id  --column-family d --hbase-create-table --hbase-bulkload


sqoop import --connect jdbc:mysql://slave2:3306/law_v2 --username weiwc --password HHly2017. \
--query 'select id,effective_status from law_rule_result_article where $CONDITIONS ' \
-m 30 --target-dir /user/weiwc/tb_doc_article --split-by id \
--hbase-table laws_doc:law_rule_result_article --hbase-row-key id  \
--column-family d --hbase-create-table --hbase-bulkload