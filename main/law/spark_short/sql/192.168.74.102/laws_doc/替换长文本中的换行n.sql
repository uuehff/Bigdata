UPDATE zzzz set doc = replace(doc,'\\n','\n')

update judgment set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea_origin = replace(court_idea_origin,'\\n','\n'),
judge_result_origin = replace(judge_result_origin,'\\n','\n') ;


update judgment_etl set 
prvs =  replace(prvs,'\\n','\n'),
doc_footer = replace(doc_footer,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');

update judgment_etl set 
judge_result = replace(judge_result,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n');
prvs =  replace(prvs,'\\n','\n'),
doc_footer = replace(doc_footer,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');


update judgment_main_etl set 
judge_result = replace(judge_result,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
doc_footer = replace(doc_footer,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');


update judgment_part set 
party_info = replace(party_info,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n') ;


update tmp_footer set 
doc_footer = replace(doc_footer,'\\n','\n');

update tmp_hzj set 
prvs = replace(prvs,'\\n','\n');

update tmp_hzj_pltdft set 
trial_request = replace(trial_request,'\\n','\n'),
trial_reply = replace(trial_reply,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n');


update tmp_wxy set 
court_idea = replace(court_idea,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n');


