1、新闻            属性：url，time，source，web_name，web_from，title,coment_list[content,area,name,time]
3、网站流量统计    属性：domain、data{pv{"week", "trimester", "day", "month"}、uv{"week", "trimester", "day", "month"}, sub_domain{子网站名{"per_reach", "per_user", "domain", "per_views"}}
4、微信            属性：公众号名称、公众号简介、发布时间、文章内容、文章标题、文章简介；
				   新增加 主要字段属性：index_scores（小宝指数）、history_rank（综合排名）、history_category_rank（分类排名）、fans_num_estimate（预估粉丝量）、avg_read_num_idx1（头条平均阅读数）
5、微博            属性：主页、信息{昵称、关注数、标签、认证、粉丝数、性别、地区、生日、简介、微博数}、全部评论、内容、发布时间、昵称、点赞数、评论数、转发数
6、贴吧            属性：tie_title，tieba_name，user_name，tie_time，tie_content

（二）数据清洗
1. 面向所有表格：
去重，如果所有属性数据都一致，去掉该条数据，即（去掉同一个用户的同一个评论）

2. 新闻表
Title: 保留题目，去掉’-’、’_’之后的媒体来源
如：“名人战惊现圣诞树安全果柯洁降级古力唐韦星出局_众鑫娱乐”等
问题：有没有可能title中有多个-，_，那怎么知道谁是title或媒体来源？删除最后一个_。


3、所有的文件title?：四强-->?4强；八强-->8强；第二十九届-->第29届
4、评论中：去掉单个字符（例如；，），去掉为空的评论，去掉的是评论字段，而非整行。

