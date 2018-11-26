INSERT into lawyers3(lawyer,law_office) SELECT lawyer,office from judgment2_lawyer

select count(*) from (
SELECT count(*)  from lawyers GROUP BY lawyer,office 
HAVING(count(*) > 1) ) a;

SELECT lawyer,office  from lawyers GROUP BY lawyer,office 
HAVING(count(*) > 1)

select * from lawyers where id = 158528
-- 丁伟	江苏衡鼎（苏州）律师事务所
-- 丁伟	河南卓衡律师事务所
-- 丁伟	湖南碧灏律师事务所
-- 丁伟	陕西兴振业律师事务所


create table lawyers4 as select lawyer,law_office from lawyers3 GROUP BY lawyer,law_office;

select id,lawyer,office from lawyers2 where id >=70 and id <= 85;

select * from judgment2_lawyer where lawyer like '一%'

