create table judgment_visualization as select 
id,uuid,court_cate,province,casedate,duration,age_year,
edu,nation,if_accumulate,gender,if_adult,if_nosuccess,
if_surrender,if_team,punish_money,punish_date,delay_date,
if_delay,punish_cate,reason,new_lawyer,new_office,fact_finder,court ;