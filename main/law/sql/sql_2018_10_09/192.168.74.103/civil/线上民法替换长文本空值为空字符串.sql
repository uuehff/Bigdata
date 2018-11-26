judgment_all: plt_claim,court_idea,dft_rep,crs_exm,judge_result,doc_footer,title,party_info,trial_process,court_find

#使用IFNULL函数进行判断时，结果的前后会多添加一个||。
#select plaintiff_id,defendant_id,CONCAT(IFNULL(plaintiff_id,''),"||",IFNULL(defendant_id,'')) from tmp_lawyers where id <300


update judgment2_main_etl set plt_claim = IFNULL(plt_claim,''),
court_idea = IFNULL(court_idea,''),
dft_rep = IFNULL(dft_rep,''),
crs_exm = IFNULL(crs_exm,''),
judge_result = IFNULL(judge_result,''),
doc_footer = IFNULL(doc_footer,''),
title = IFNULL(title,''),
party_info = IFNULL(party_info,''),
trial_process = IFNULL(trial_process,''),
court_find = IFNULL(court_find,'') where (plt_claim is null or court_idea is null or judge_result is null or doc_footer is null or title is null or party_info is null or trial_process is null or court_find is null) and id < 200000;

