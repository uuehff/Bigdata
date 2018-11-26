0、线上执行：SELECT max(id) from law_news，找出最大id,下面使用。
1、在22上：create table 11_21 as SELECT * from law_news where id > 14553
2、数据传输到localhost：news中，修改引擎为Myisam。
3、关闭本地mysqld(这里的mysqld好像不关闭也可以上传三个对应的文件)，上传D:\ProgramData\MySQL\MySQL Server 5.6\data\news下的文件到cdh-master的：/home/cdh/bak
	然后执行：scp -P 2222 ./12_18* cdh@cdh-slave1:/data/bak
ssh cdh-slave1 -p 2222
4、在cdh-slave1:/data/bak下:
	1）关闭mysqld服务.（这里经测试好像也可以不关闭直接放入三个文件，但允许关闭的时候最好先关闭）
	2）chown mysql:mysql ./11_17*
	3) mv ./11_17* /data/mysql/laws
	4)开启Mysqld.
5、登录mysql：mysql -h 10.33.51.2 -uroot -pHHly2017.
	use laws;	
	INSERT into law_news SELECT * from 12_18;