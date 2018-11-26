sqoop import -D sqoop.hbase.add.row.key=true --connect jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new  --username weiwc --password HHly2017. \
 --query 'select * from hht_lawyer_all_collect_match_result where $CONDITIONS' \
-m 30 --target-dir /user/weiwc/tb_doc --split-by id --hbase-table laws_doc:lawyers_v4 --hbase-row-key lawyer_id  --column-family d --hbase-create-table --hbase-bulkload
