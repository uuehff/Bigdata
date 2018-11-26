SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';

create table judgment_add300wan_etl01 like laws_doc_judgment_add560wan.judgment_add560wan_etl01;
create table judgment_add300wan_etl02 like judgment_add300wan_etl01;
create table judgment_add300wan_etl03 like judgment_add300wan_etl01;
create table judgment_add300wan_etl04 like judgment_add300wan_etl01;
create table judgment_add300wan_etl05 like judgment_add300wan_etl01;

create table judgment_add300wan_etl01 like laws_doc_judgment_add560wan.judgment_add560wan_etl01;
