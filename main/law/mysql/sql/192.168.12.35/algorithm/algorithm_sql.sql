-- ==============================
-- ssq规则：(更新数据：2\4\7)
-- r1~r6: 1 ~ 33
-- b1:	1 ~ 16
-- ==============================
-- dlt规则：(更新数据：1\3\6)
-- r1~r5: 1 ~ 35
-- b1~b2: 1 ~ 12

SELECT * from  ssq LIMIT 10
CREATE TABLE factor LIKE ssq

CREATE TABLE factor as SELECT * from dlt ORDER BY id

SELECT r1+r2+r3+r4+r5+r6,r1+r2+r3+r4+r5+r6+b1,b1 from ssq 

SELECT r1%2+r2%2+r3%2+r4%2+r5%2+r6%2,6-(r1%2+r2%2+r3%2+r4%2+r5%2+r6%2) from ssq 

SELECT r1,r6 from ssq
