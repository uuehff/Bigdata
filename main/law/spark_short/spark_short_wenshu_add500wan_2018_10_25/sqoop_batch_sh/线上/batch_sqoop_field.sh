#!/bin/bash
s1=""
s2=""
s3=""
cat /home/cdh/add500wan/table_name_field | while read line
do
 
 #echo "$line"   #输出整行内容
 #echo "$line" |  awk '{for(i=1;i<=NF;i++) print $i}'  #输出每行的各个字段
 
 s1=`echo "$line" | awk '{print $1}'` #输出每行第一个字段
 s2=`echo "$line" | awk '{print $2}'` #输出每行第一个字段
 s3=`echo "$line" | awk '{print $3}'` #输出每行第一个字段
 
 echo $s1,$s2,$s3
 
 sqoop import -D sqoop.hbase.add.row.key=true  --connect jdbc:mysql://slave2:3306/${s1} \
 --username weiwc --password HHly2017. --query "select id,uuid,field from ${s2} where \$CONDITIONS " \
 -m 100 --target-dir /user/weiwc/tb_doc_${s1}_${s2} --split-by id --hbase-table ${s3}  \
 --hbase-row-key uuid  --column-family d --hbase-create-table --hbase-bulkload

done


