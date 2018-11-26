update tmp_wxy set  
doc_footer = replace(doc_footer,'\\n','\n'), 
court_idea = replace(court_idea,'\\n','\n'), 
judge_result = replace(judge_result,'\\n','\n');

create table law_rule_result2_error_flag as 
select id,error from law.law_rule_result2 where error != '' ;


update judgment_civil_56w set  
reason = replace(reason,'罪','');


民法字段换行符替换：
doc_footer,party_info,judge_result,plt_claim,dft_rep,crs_exm,trial_process,court_find, court_idea                                                   

update judgment_civil_56w set 
reason = replace(reason,'罪',''),
doc_footer = replace(doc_footer,'\\n','\n'),
party_info = replace(party_info,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n');

update judgment_civil_50w set 
reason = replace(reason,'罪',''),
doc_footer = replace(doc_footer,'\\n','\n'),
party_info = replace(party_info,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n');

update judgment_civil_all set 
reason = replace(reason,'罪',''),
doc_footer = replace(doc_footer,'\\n','\n'),
party_info = replace(party_info,'\\n','\n'),
judge_result = replace(judge_result,'\\n','\n'),
plt_claim = replace(plt_claim,'\\n','\n'),
dft_rep = replace(dft_rep,'\\n','\n'),
crs_exm = replace(crs_exm,'\\n','\n'),
trial_process = replace(trial_process,'\\n','\n'),
court_find = replace(court_find,'\\n','\n'),
court_idea = replace(court_idea,'\\n','\n');