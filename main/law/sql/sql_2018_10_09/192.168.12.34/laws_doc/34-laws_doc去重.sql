SELECT id FROM `tb_doc` WHERE (`caseid`, `title`,`casedate`) IN (SELECT `caseid`, `title`,`casedate` FROM `tb_doc` GROUP BY `caseid`, `title`,`casedate` HAVING COUNT(1) > 1) AND `id` NOT IN (SELECT MIN(`id`) FROM `tb_doc` GROUP BY `caseid`, `title`,`casedate` HAVING COUNT(1) > 1);


SELECT COUNT(*) from tmp_weiwenchao2 where 