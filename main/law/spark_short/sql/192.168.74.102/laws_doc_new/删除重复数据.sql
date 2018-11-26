删除judgment_new_v2表重复数据：

DELETE a from judgment_new_v2 a,judgment_new_uuid_del_02 b where a.uuid = b.uuid;

DELETE a from judgment_new_v2_court_cate_judge_footer a,judgment_new_uuid_del_02 b where a.uuid = b.uuid;

DELETE a from judgment_new_uuid_law_id_v2 a,judgment_new_uuid_del_02 b where a.uuid = b.uuid;

DELETE a from judgment_new_other_fields_v2_result a,judgment_new_uuid_del_02 b where a.uuid = b.uuid;