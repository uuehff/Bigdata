create table lawyer_picture as select uuid,party_info from judgment2

update lawyer_picture set plaintiff_judge_result = '1' ,defendant_judge_result = '0' 

update lawyer_picture set defendant_company = "" where defendant_company like "%×%"
update lawyer_picture set defendant_company = "" where defendant_company like "%某%"

update lawyer_picture set plaintiff_company = "" where plaintiff_company like "%×%"
update lawyer_picture set plaintiff_company = "" where plaintiff_company like "%某%"

update lawyer_picture set plaintiff_company = REPLACE(plaintiff_company,'）','')
update lawyer_picture set plaintiff_company = REPLACE(plaintiff_company,'（','')

update lawyer_picture set defendant_company = REPLACE(defendant_company,'）','')
update lawyer_picture set defendant_company = REPLACE(defendant_company,'（','')

DELETE from lawyer_picture where uuid in (select uuid from judgment2 where is_format != 1);


select * from judgment2 where uuid = "009bac57-ecea-49c7-a836-e6cf2b95b523"


update laws_doc.lawyers set id_name = CONCAT(id,"||",lawyer)

select * from lawyer_picture where party_info like "%人侯安到周口市公安局交警支队投案自首%"

