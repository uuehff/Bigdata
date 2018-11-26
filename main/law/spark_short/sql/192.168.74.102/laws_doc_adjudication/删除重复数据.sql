删除adjudication_civil_etl_v2表重复数据：

DELETE a from adjudication_civil_etl_v2 a,adju_uuid_del03_distinct b where a.uuid = b.uuid;
DELETE a from adjudication_civil_etl_v2_court_cate_judge_footer a,adju_uuid_del03_distinct b where a.uuid = b.uuid;