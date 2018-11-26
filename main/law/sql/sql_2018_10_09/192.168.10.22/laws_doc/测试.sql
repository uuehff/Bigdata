select * from administration where judge_type = "裁定" limit 50;

select * from implement where judge_type = "裁定" limit 50;

select * from imp_other where judge_type = "裁定" limit 50;

select * from imp_other where judge_type = "决定" limit 10;
select * from imp_other where judge_type = "通知" limit 10;



select * from imp_other where uuid = "00003735-1168-426b-ae8c-a84800c76678";
select * from adjudication where uuid = "dfb93648-73b4-4e14-b39d-a7a20111f939"


select * from judgment where uuid = "08e5ed58-7b80-4db5-889b-8aa9e3ba11e9"


select * from implement where uuid = "b90efbcb-7235-4452-a9ef-828b9a1cdc4e"


select * from imp_other where uuid = "b90efbcb-7235-4452-a9ef-828b9a1cdc4e"
select * from imp_other where uuid = "775ef50c-d8cd-4dbe-af14-d5307988cdcd"
select * from implement where uuid = "cdd9f1d1-64ed-41c2-ba07-3058fec18cfc"


select * from imp_other where title like "%李培金与张德海等机动车交通事故责任纠纷无执行裁定书%";


