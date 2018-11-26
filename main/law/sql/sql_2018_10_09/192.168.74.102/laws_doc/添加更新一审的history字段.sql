UPDATE judgment_etl_uuid_history_title_result a , judgment_etl b set 
b.history = a.history ,
b.history_title = a.title  where a.uuid = b.uuid;


UPDATE judgment_etl_uuid_history_title_result a , judgment_main_etl b set 
b.history = a.history ,
b.history_title = a.title  where a.uuid = b.uuid;
