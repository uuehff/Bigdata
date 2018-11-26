UPDATE zzzz set doc = replace(doc,'\\n','\n')
UPDATE zzzz set doc = CONCAT(replace(doc,'\\n','\n'),'。')

update judgment2 set 
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea_origin = replace(court_idea_origin,'\\n','\n'),
judge_result_origin = replace(judge_result_origin,'\\n','\n') ;



update judgment2_etl set 
doc_footer = replace(doc_footer,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n'),
party_info = replace(party_info,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');


update judgment2_main_etl set 
doc_footer = replace(doc_footer,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');


update tmp_hzj set 
party_info = replace(party_info,'\\n','\n');

update tmp_hzj_pltdft set 
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');


update tmp_wxy set 
doc_footer = replace(doc_footer,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n');




