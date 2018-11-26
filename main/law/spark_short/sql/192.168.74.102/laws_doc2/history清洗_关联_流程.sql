1、去掉与自己相同的uuid，去掉引号，中括号等。
2、筛选部分uuid，根据匹配原则：case?id=，只选取以cased开头的uuid，（uuid前两位：01~ff），经统计
		uuid后27位唯一！可用来作为(uuid_27,uuid)，使用spark进行补全。
先确保history中的uuid都是能匹配到的，因为之前judgment_etl中又删了一些uuid，is_format不为1的。

3、筛选history长度为：36的。
	判断其：province,age_year,if_surrender,if_nosuccess,if_accumulate是否一致，一致的话基本OK，有
  案号加上这几个字段基本可以确定正确。
	如果province,age_year,if_surrender,if_nosuccess,if_accumulate这几个中只要有一个不一致，可打印出
  该uuid(judgment)和history中一审的uuid（judgment2）进行对比对应的title，再进行取舍。（可先将不一致的放到另一表，顺序一致，
   对比的同时进行删除uuid，之后在更新到judgment2_etl）

筛选history长度大于：36的。

先使用province,age_year,if_surrender,if_nosuccess,if_accumulate过滤掉，这几个字段不一致的uuid。
之后只有一个uuid的话，可根据上面history长度为36的来。
若还有多个则只能打印出title。肉眼观察，取舍。

