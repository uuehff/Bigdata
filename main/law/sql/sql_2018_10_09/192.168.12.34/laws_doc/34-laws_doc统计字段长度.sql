-- length:返回字符串所占的字节数，是计算字段的长度一个汉字是算三个字符,一个数字或字母算一个字符
-- char_length:返回字符串所占的字符数，不管汉字还是数字或者是字母都算是一个字符

SELECT casedate,court_new, LENGTH(casedate),CHAR_LENGTH(casedate),LENGTH(court_new),CHAR_LENGTH(court_new), (LENGTH(casedate)+LENGTH(court_new)) as sums  from judgment_etl where id < 100 order by (LENGTH(casedate)+LENGTH(court_new)) desc 