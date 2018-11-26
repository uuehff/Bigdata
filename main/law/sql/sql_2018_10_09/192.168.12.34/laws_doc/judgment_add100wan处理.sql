select * from judgment where id > 2824880 and id < 2824940; 新增起始id:2824917

create table judgment_add100wan_part as select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where 1=2;
INSERT into judgment_add100wan_part(id,uuid,caseid,title,court,lawlist,reason_type,type,judge_type) select id,uuid,caseid,title,court_origin,lawlist,reason_type,type,judge_type from judgment where id > 2824916;

select reason_type,judge_type,type,count(*) from judgment where id > 2824916  group by reason_type,judge_type,type

刑事	判决	0	1036779