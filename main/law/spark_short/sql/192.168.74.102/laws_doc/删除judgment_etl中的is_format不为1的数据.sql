select id from judgment_etl where uuid in (SELECT uuid from is_format_not_1)

update laws_doc2.judgment2_etl set type = '2' where type != '2'
