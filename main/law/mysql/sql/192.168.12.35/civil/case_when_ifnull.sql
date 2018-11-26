select lawyer from id_lawyer group by lawyer ORDER BY count(lawyer) desc;


select lawyer,office from id_lawyer group BY lawyer,office HAVING(count(*) > 1)

select id,lawyer,office from id_lawyer where lawyer = '丁一元'

create table id_lawyer2 as select lawyer,office from id_lawyer group BY lawyer,office

update tmp_lawyers a, party_info_result_ids b set a.plaintiff_id = b.plaintiff_id, 
a.defendant_id = b.defendant_id where a.uuid = b.uuid;

update tmp_lawyers a, party_info_result_ids b set a.lawyer_id = b.lawyer_id where a.uuid = b.uuid;

#使用IFNULL函数进行判断时，结果的前后会多添加一个||。
select plaintiff_id,defendant_id,CONCAT(IFNULL(plaintiff_id,''),"||",IFNULL(defendant_id,'')) from tmp_lawyers where id <300


update party_info_result_ids set lawyer_id = (case 
when plaintiff_id is null then defendant_id
when defendant_id is null then plaintiff_id
else  CONCAT(plaintiff_id,"||",defendant_id) end);


注意：concat函数连接时，有一个字段为NULL时，则连接结果就为NULL！

select plaintiff_id,defendant_id,
(case 
when plaintiff_id is null then defendant_id     #该条件也包含了两个都为NULL的情况！
when defendant_id is null then plaintiff_id
else  CONCAT(plaintiff_id,"||",defendant_id) end) as lawyer_id from tmp_lawyers where id <300;

select max(CHAR_LENGTH(uuid)) from party_info_result_ids where uuid is null;

alter table judgment_main_etl 
add plaintiff_id varchar(255),
add defendant_id varchar(255),
add lawyer_id varchar(255);



alter table judgment_main_etl 
add plaintiff_id varchar(255),
add defendant_id varchar(255),
add lawyer_id varchar(255);


alter table judgment_visualization 
drop new_lawyer,
drop new_office;
