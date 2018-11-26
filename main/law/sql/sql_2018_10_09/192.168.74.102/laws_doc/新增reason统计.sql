DELIMITER $$  
  
CREATE DEFINER=`root`@`%` FUNCTION `split_count`(  
f_string varchar(1000),f_delimiter varchar(100)  
) RETURNS int(11)  
BEGIN  
  return 1+(length(f_string) - length(replace(f_string,f_delimiter,''))) / length(f_delimiter);  
END$$  
  
DELIMITER ;  


SELECT new_reason,reason_uid,split_count(new_reason,'||'),split_count(reason_uid,'||') from judgment_etl where id = 367

create table reason_add as 
SELECT uuid,new_reason,reason_uid from judgment_etl where new_reason is not null and new_reason != '' and 
(reason_uid is null or reason_uid = '' or split_count(new_reason,'||') != split_count(reason_uid,'||'))

SELECT * from reason where uid = '1006007'
SELECT * from reason where uid = '1006007003'


SELECT * from reason where uid = '1006'
SELECT * from reason where parent = '1006007'

SELECT * from reason where new_name = '非法买卖、运输、携带、持有毒品原植物种子、幼苗罪'



SELECT * from reason where new_name = '%侵犯人身权利%'

create table laws_doc2.reason_new_add as 
SELECT * from laws_doc2.reason_c where new_reason not in (SELECT new_name from reason)

SELECT * from laws_doc2.judgment2_etl where uuid = '08314a7a-5401-497b-b594-e3245d2b52a0'

create table judgment_etl_uuid_new_reason as 
select uuid,new_reason from judgment_etl 

select * from judgment_etl_uuid_new_reason where new_reason is null or new_reason = ''



