SELECT new_reason from judgment2_etl where reason_uid is null and CHAR_LENGTH(new_reason) > 8 group by new_reason
侵犯人身权利、民主权利罪||强制猥亵、侮辱妇女罪(已删除罪名)
结果类型||：驳回攻方部分请求
非法获取公民个人信息罪（已删除罪名）||侵犯人身权利、民主权利罪



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
SELECT uuid,new_reason,reason_uid from judgment2_etl where new_reason is not null and new_reason != '' and 
(reason_uid is null or reason_uid = '' or split_count(new_reason,'||') != split_count(reason_uid,'||'))



select * from reason_add where new_reason in ('刑事特别程序案件')
