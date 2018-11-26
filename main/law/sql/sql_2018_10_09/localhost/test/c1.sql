DELETE from tb_doc where id in (
select tt3.idd from 
(select tt.id as idd from (select id as id from tb_doc as t,
	(SELECT CONCAT(caseid,title,casedate) as c from tb_doc as a GROUP BY CONCAT(caseid,title,casedate) HAVING(COUNT(*)>1)) as tmp 
	where CONCAT(t.caseid,t.title,t.casedate) = tmp.c ) as tt WHERE tt.id not in 
(SELECT min(id) as id2 from tb_doc GROUP BY CONCAT(caseid,title,casedate) HAVING COUNT(*) > 1)) as tt3
)
-- -- -- alter table tb_doc add unique index union_index(caseid,title,casedate);

SELECT id FROM `tb_doc` WHERE (`caseid`, `title`,`casedate`) IN (SELECT `caseid`, `title`,`casedate` FROM `tb_doc` GROUP BY `caseid`, `title`,`casedate` HAVING COUNT(1) > 1) AND `id` NOT IN (SELECT MIN(`id`) FROM `tb_doc` GROUP BY `caseid`, `title`,`casedate` HAVING COUNT(1) > 1);

