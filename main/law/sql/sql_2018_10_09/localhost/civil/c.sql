SELECT id FROM `tb_doc` WHERE (`caseid`, `title`,`casedate`) IN (SELECT `caseid`, `title`,`casedate` FROM `tb_doc` GROUP BY `caseid`, `title`,`casedate` HAVING COUNT(1) > 1) AND `id` NOT IN (SELECT MIN(`id`) FROM `tb_doc` GROUP BY `caseid`, `title`,`casedate` HAVING COUNT(1) > 1);

CREATE table content_test LIKE tb_content

update tb_doc t1 ,tb_content t2 set t1.doc_content = t2.doc_content where t1.id <= 5


-- tb_doc t1, tb_content t2 SET 
--    set t1. = t2.`name`
--  where t1.id = t2.id;
-- update test123 t1, test456 t2
--    set t1.address2 = t2.`name`
--  where t1.id = t2.id;

ALTER TABLE table_name ADD func varchar(50), ADD gene varchar(50), ADD genedetail varchar(50);
ALTER TABLE  table_name ADD INDEX idx1 ( `func`), ADD INDEX idx2 ( `func`,`gene`), ADD INDEX idx3( `genedetail`); 
CREATE TABLE `tb_doc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` varchar(100) NOT NULL COMMENT '文书ID',
  `doc_title` varchar(200) NOT NULL COMMENT '案件名称',
  `doc_date` varchar(50) NOT NULL COMMENT '判决日期',
  `doc_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `doc_court` varchar(100) NOT NULL COMMENT '判决法院',
  `doc_num` varchar(100) NOT NULL COMMENT '文书编号',
  `is_crawled` tinyint(2) NOT NULL DEFAULT '0',
  `is_format` tinyint(2) NOT NULL DEFAULT '0' COMMENT '是否清洗',
  PRIMARY KEY (`id`),
  UNIQUE KEY `doc_id` (`doc_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=5949853 DEFAULT CHARSET=utf8;


CREATE TABLE `judgment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) CHARACTER SET utf8 NOT NULL,
  `caseid` varchar(80) CHARACTER SET utf8 NOT NULL,
  `title` varchar(220) CHARACTER SET utf8 NOT NULL,
  `doc_reason` text CHARACTER SET utf8,
  `doc_oriligigation` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `fact_finder` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `court` varchar(255) CHARACTER SET utf8 NOT NULL,
  `lawlist` text CHARACTER SET utf8,
  `record_time` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `casedate` varchar(30) CHARACTER SET utf8 DEFAULT '',
  `timeline` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `party_info` text CHARACTER SET utf8,
  `defendant` text,
  `plaintiff` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `third` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `trial_process` mediumtext,
  `trial_request` mediumtext,
  `trial_reply` mediumtext,
  `court_find` mediumtext,
  `court_idea` mediumtext,
  `judge_result` mediumtext,
  `judge_chief` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `judge_member` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `history` text CHARACTER SET utf8,
  `type` varchar(255) CHARACTER SET utf8 DEFAULT '0',
  `reason_type` varchar(255) CHARACTER SET utf8 DEFAULT '刑事',
  `judge_type` varchar(255) CHARACTER SET utf8 DEFAULT '判决书',
  `result_type` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `doc_content` mediumtext CHARACTER SET utf8,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `doc_from` varchar(255) CHARACTER SET utf8 DEFAULT 'wenshu-gov',
  `reason` varchar(255) CHARACTER SET utf8 DEFAULT '',
  `is_crawl` tinyint(2) DEFAULT '0',
  `is_format` tinyint(2) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`) USING BTREE,
  UNIQUE KEY `union_index` (`casedate`,`title`,`caseid`),
  KEY `is_crawl` (`is_crawl`),
  KEY `is_format` (`is_format`),
  KEY `doc_from` (`doc_from`)
) ENGINE=MyISAM AUTO_INCREMENT=2824917 DEFAULT CHARSET=utf8mb4;
