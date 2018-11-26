update mediate_uuid set uuid = id ;

insert ignore into hbase_uuid(uuid,uuid_old) select uuid,uuid_old from  administration;
insert ignore into hbase_uuid(uuid,uuid_old) select uuid,uuid_old from implement;
insert ignore into hbase_uuid(uuid,uuid_old) select uuid,uuid_old from  judgment;
insert ignore into hbase_uuid(uuid,uuid_old) select uuid,uuid_old from  mediate_uuid;
insert ignore into hbase_uuid(uuid,uuid_old) select uuid,uuid_old from  civil;


统计重复：


create table administration_implement as select a.uuid,a.uuid_old from 
implement a join administration b on a.uuid = b.uuid;
1条；
create table administration_civil as select a.uuid,a.uuid_old from 
civil a join administration b on a.uuid = b.uuid ;
6条;

create table judgment_civil as select a.uuid,a.uuid_old from 
judgment a join civil b on a.uuid = b.uuid ;
56条；

create table implement_civil as select a.uuid,a.uuid_old from 
implement a join civil b on a.uuid = b.uuid ;
1779条；

共：1842条；

