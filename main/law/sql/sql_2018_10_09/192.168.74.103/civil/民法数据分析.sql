select id,uuid,judge_type,is_format from judgment where judge_type != "判决" limit 1000

3	691a2baf-28e5-4144-8a2f-6b0246df438c	裁定	1
4	c21f343b-cdac-41f4-9042-c4ab828f8e40	裁定	1
6	de569d8c-d734-4347-9464-02898a9d5e6e	裁定	1
11	ba63a1c1-8638-4fb9-a9e9-52a9ddaf353a	裁定	1
16	46020274-7ead-4c70-aab7-a72b000f31cf	裁定	1
23	4b2e1d52-f80c-4e76-9b54-02da85a16303	裁定	1

select id,uuid,judge_type from judgment_civil_all where uuid = "691a2baf-28e5-4144-8a2f-6b0246df438c"
