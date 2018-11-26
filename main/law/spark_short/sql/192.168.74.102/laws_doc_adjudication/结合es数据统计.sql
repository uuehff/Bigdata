create table es_adjudication_civil_etl_v2_100 as 
select * from adjudication_civil_etl_v2 where id < 100;

select * from adjudication_civil_etl_v2 where id < 100;


select * from adjudication_civil_etl_v2 where id < 100 and court = "江苏省高级人民法院";
select * from adjudication_civil_etl_v2 where id < 100 and casedate = "2017-03-30";
select * from adjudication_civil_etl_v2 where id < 100 and CHAR_LENGTH(casedate) < 10;


select * from es_adjudication_civil_etl_v2_100 where lawlist = ""
update es_adjudication_civil_etl_v2_100 
set reason_type = "刑事" where id like "%0" or id like "%1"

update es_adjudication_civil_etl_v2_100 
set reason_type = "执行" where id like "%2" or id like "%3"

update es_adjudication_civil_etl_v2_100 
set lawlist = "" where id like "%2" or id like "%0" or id like "%4" or id like "%5"


update es_adjudication_civil_etl_v2_100 
set judge_type = "判决" where id like "%2" or id like "%4"


select *,fields,count(*),SUBSTR(id,1,1) from es_adjudication_civil_etl_v2_100 
where id/judge_type = like "%content%" or/and  id/judge_type > 100 
or/and id/judge_type in ("r1","r2") 
group by f1,f2 having() 
order by id
limit 10;
=========================================================
kibana使用技巧：
1、
tab 或 enter ,补全选中提示；
ctrl+i 自动缩进
ctrl+enter 提交请求
ctrl + 上下键，跳到一个代码块的开头或结尾；
ctrl + d 删除当前行，或选中行
alt + 上下键，移动

2、GET、POST等大写时才会有提示自动补全；
3、kibana中输入完整的：GET /cdh-doc/civil/_search/时，
想知道每次/下面该输入什么，可以在/之后输入_a，就会有提示弹出（这里只显示包含_a的提示），
再删除_a就会有全部的提示弹出；

4、查看所有的索引、及其下的类型：
	1）head中的"数据浏览"，左侧列出了所有的索引、类型、字段；
  2）使用_index、_type字段进行分组统计即可。


========================================================================

_source：返回哪些字段，= select
multi_match：一个值去匹配多个字段。
"multi_match": {
       "query": "章芳芳", 
       "fields": ["doc_footer","trial_request"]
等价于：
doc_footer like "%章芳芳%" or trial_request like "%章芳芳%"


head监控：索引创建时间、状态、信息、查看数据；
http://192.168.74.109:9100/?auth_user=elastic&auth_password=changeme
或者: http://192.168.74.109:9100/?auth_user=cdh&auth_password=cdh@13322.com

match_all：查询所有文档，默认的查询方式：{ "match_all": {}}

GET /cdh-doc/civil/_search
{
  "query": {
    "match_all": {}
  }
}
match_all查询与下面等价：
GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
      "filter": {
        "match_all": {}
      }
    }
  }
}

multi_match:多字段查询
{
    "multi_match": {
        "query":    "判决",
        "fields":   [ "caseid", "judge_type" ]
    }
}

terms: 多值查询
"query": {
     "terms": {
       "casedate": ["2017-05-08","2017-09-22"]
     }
  }  
等价于：
casedate = "2017-05-08" or casedate = "2017-09-22"



match与term的区别：
match查询是根据要查询的字段，是否经过分词，来确定输入的内容是否分词；
使用match查询未分词的字段时，原理跟term查询一样；

term查询，无论用在分词还是未分词的字段查询上，输入内容都不会分词，因此当使用term查询
分词的字段时，没有什么意义，字段分词后是倒排索引，是将输入内容去倒排索引里查询；
例如：
GET cdh-doc/civil/_search
{
  "query": {
     "term": {
       "caseid": "2016"
     }
  }  , 
  "_source": ["id","casedate","lawlist","caseid"]
}
使用term查询caseid，其实是使用2016字符串去caseid里的倒排索引去查找；
而caseid = "（2016） 苏民申2401号" 分词结果为：2016、苏、民、申、2401、号等几个词；
GET /_analyze
{
  "analyzer": "standard",
  "text": "（2016） 苏民申2401号"
}

因此搜索2016会有结果；
但一般要查的内容要分词（长文本），查询输入也要分词；
要查的内容不分词，一般输入也是知道的，固定的；
因此这种term去查询分词的文本没有太大意义；

bool查询：query语句下面只能有一个查询语句，但是想使用多个查询语句的话，就必须使用bool组合查询。
"bool": {
      "must": {
        "term": {"caseid": "2401"}
      }, 
      "must": {
        "term": {"caseid": "苏"}
      }
    }
注意：一个must或must_not或should可以放一个查询语句（也可以使用[]放入多个语句），就类似：
"must": {
        "term": {"caseid": "2401"}
      }
must里面可以放一个查询：
就类似SQL中的一个or 或and只能加一个条件：
a > 3 and b = 5 and c >= 10
也可放多个查询；使用[]括起来；如下：
"must": [
        {"term": {
          "casedate": {
            "value": "2017-05-27"
          }
        }},
        {"exists": {
          "field":"lawlist"
        }}
        ]
exists是区分is null 和 is not null 的；mysql中不为NULL的字段导入ES后
都有保留，即使为""也会保留，但mysql中为NULL的字段，导入ES后，
该字段在ES中就不存在。missing查询在5.0以后被移除，可通过must_not搭配exists实现该功能。


组合多查询：bool查询中的每个must_not、must、should、filter子查询之间都是and逻辑，
其中must_not、must、should作用的是其内部的查询列表之间的关系:
must_not = ！
must = AND
should = OR
具体如下：
must_not中的多个查询之间逻辑关系是: not query1 and not query2 and not query3 
must中的多个查询之间逻辑关系是: query1 and query2 and query3
should中的多个查询之间逻辑关系是: query1 or query2 or query3
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }},
            { "range": { "date": { "gte": "2014-01-01" }}}
        ]
    }
}

如果没有 must 语句，那么至少需要能够匹配其中的一条 should 语句。
但，如果存在至少一条 must 语句，则对 should 语句的匹配没有要求，should语句
只对must和must_not查询的结果进行评分影响，不参与查询。
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }}
        ],
        "filter": {
          "range": { "date": { "gte": "2014-01-01" }} 
        }
    }
}

所有查询都可以借鉴这种方式。将查询移到 bool 查询的 filter 语句中，
这样它就自动的转成一个不评分的 filter了。filter中的过滤一般都是精确值
匹配:日期、数字、固定短语。一般用range、term、exists、或针对非text类型的match查询。
GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
          "must": {"match": { "reason_type": "民事" }},
          "must_not": { "match": { "judge_type":   "判决" }},
          "should": { "match": { "party_info": "判决" }},
          
          "filter": {
            "bool": {
                "must": [
                    {"range": {"casedate": {"gte": "2017-04-01"}}},
                    {"range": { "id": { "lte": 50 }}}
                ],
                "must":{"range": { "id": { "gte": 2 }}},
                "must_not": { "term": { "reason": "劳动争议" }},
                "must_not": { "term": { "reason.keyword": "劳动争议" }},
                "must_not": { "match": { "reason": "劳动争议" }},
                "must_not": { "match": { "reason.keyword": "劳动争议" }}
            }
        }
    }
  }
}
filter过滤中也可以使用bool过滤；
"term": { "reason": "劳动争议" } : 匹配不到任何结果，因为reason分词为四个字，而term不分词查询内容；
"term": { "reason.keyword": "劳动争议" }：有意义的固定匹配，有结果
"match": { "reason": "劳动争议" }：输入内容分词后匹配，有结果
"match": { "reason.keyword": "劳动争议" } ：与"term": { "reason.keyword": "劳动争议" }原理一样；

注意：该查询filter中的
{ "term": { "reason": "劳动争议" }，匹配的数据为空，因为reason字段
被分词之后建立倒排索引，而term查询对输入是部分词的，
因此就相当于拿着："劳动争议"词去倒排索引里匹配，找不到结果，因为：
因此：
想通过精确值查找、过滤、不评分查询的字段，不评分就意味着不分词查询，
评分就意味着分词查询；
一个完整的查询，包括评分查询逻辑和不评分查询逻辑；
不评分查询全部放入bool查询的filter子查询中！

term只能查询单个精确值；
terms：查询多个精确值：相当于 in 语句；
terms中的精确值，只要有一个在字段（分词的）的倒排索引中能找到即可，这里keyword类型的
字段认为是：将整个值放入倒排索引，当做一个词来处理；
===================================
嵌套过滤器：bool过滤器嵌套在should查询中：

GET /cdh-doc/civil/_search
{
   "query" : {
      "bool" : {
         "filter" : {
            "bool" : {
              "should" : [
                { "term" : {"productID" : "KDKE-B-9947-#kL5"}}, 
                { "bool" : { 
                  "must" : [
                    { "term" : {"productID" : "JODL-X-1937-#pV7"}}, 
                    { "term" : {"price" : 30}} 
                  ]
                }}
              ]
           }
         }
      }
   }
}
============
字符串过滤：在倒排索引中的词项就是采取字典顺序（lexicographically）排列的，
这也是字符串范围可以使用这个顺序来确定的原因。

"range" : {
    "title" : {
        "gte" : "a",
        "lt" :  "b"
    }
}




GET /_analyze
{
  "analyzer": "standard",
  "text": "劳动争议"
}
返回四个词："劳"、"动"、"争"、"议"




验证查询的正确性、以及对查询进行解释、拆分；如下：
GET /cdh-doc/civil/_validate/query?explain 
{
   "query": {
      "match" : {
         "caseid" : "刑事案号"
      }
   }
}
-- ===========================
GET /cdh-doc/civil/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "reason_type.keyword": "民事"
        }
      }
    }
  }
}
等价于：
GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
      "filter": {
        "term": {
          "reason_type.keyword": "民事"
        }
      }
    }
  }
}
constant_score经常用于只需要执行一个filter而没有其它查询（例如，评分查询）的情况下。
constant_score只能使用它来取代只有filter语句的bool查询，因此constant_score语句中不能
像bool那样直接包含must、must_not、should等评分查询语句，但可以在filter内部使用bool查询，该bool
查询下面包含must、must_not、should等查询。如下：
constant_score在性能上和bool查询是完全相同的，但对于提高查询简洁性和清晰度有很大帮助。

GET /cdh-doc/civil/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "bool": {
          "must":{"term": {"reason_type.keyword": "民事"}},
          "must_not":{"term": {"reason_type.keyword": "裁定"}}
        }
      }
    }
  }
}

======================
match查询控制精度：

match 查询可以接受 operator 操作符作为输入参数，默认情况下该操作符是 or 。
我们可以将它修改成 and 让所有指定词项都必须匹配：

GET /cdh-doc/civil/_search
{
    "query": {
        "match": {
            "caseid": {      
                "query":  "苏1145",
                "operator": "and"
            }
        }
    }
}

说明："苏1145"被分词为："苏"、"1145"，"operator": "and"因此需要全部匹配这两个词项，结果只有一条；



match 查询支持 minimum_should_match 最小匹配参数，可以指定必须匹配的词项数（分词后的词项）
或者在bool组合查询中should语句匹配的个数。
minimum_should_match可以设置为某个具体数字，更常用的做法是将其设置为一个百分数，
因为我们无法控制用户搜索时输入的单词数量：

控制查询中的词项匹配个数：
GET /cdh-doc/civil/_search
{
  "query": {
    "match": {
      "reason": {
        "query": "故意劳工",
        "minimum_should_match": "75%"
      }
    }
  }
}

控制should中：查询语句的数量：
GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "reason": "劳" }},
        { "match": { "reason": "动"   }},
        { "match": { "reason": "争"   }},
        { "match": { "reason": "议"   }}
      ],
      "minimum_should_match": 3 
    }
  }
}
================================================
GET /cdh-doc/civil/_search?size=23
{
  "query": {
    "bool": {
      "must": [
        {"match": { "reason": "劳动" }}
      ], 
      "must_not": [
        {"match": { "reason": "争议" }}
      ]
      
    }
  }
}
说明：
must逻辑：reason中存在"动"或"劳"或"劳动"都会保留；
must_not逻辑：reason中存在"争"或"议"或"争议"都会丢弃；
以上两种结果的交集是最终结果；

==========================================================================
ool查询与match查询的等价转换：
多词 match 查询只是简单地将生成的 term 查询包裹 在一个 bool 查询中。如果使用默认的 or 操作符，
每个 term 查询都被当作 should 语句，这样就要求必须至少匹配一条语句。以下两个查询是等价的：

{
    "match": { "title": "brown fox"}
}
{
  "bool": {
    "should": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }}
    ]
  }
}
如果使用 and 操作符，所有的 term 查询都被当作 must 语句，所以 所有（all） 语句都必须匹配。以下两个查询是等价的：

{
    "match": {
        "title": {
            "query":    "brown fox",
            "operator": "and"
        }
    }
}
{
  "bool": {
    "must": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }}
    ]
  }
}
如果指定参数 minimum_should_match ，它可以通过 bool 查询直接传递，使以下两个查询等价：

{
    "match": {
        "title": {
            "query":                "quick brown fox",
            "minimum_should_match": "75%"
        }
    }
}
{
  "bool": {
    "should": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }},
      { "term": { "title": "quick" }}
    ],
    "minimum_should_match": 2 
  }
}
深入搜索：近似匹配：
短语查询：
本质上来讲，match_phrase 查询是利用一种低级别的 span 查询族（query family）去做词语位置敏感的匹配。
Span 查询是一种词项级别的查询，所以它们没有分词阶段；它们只对指定的词项进行精确搜索。

term与match_phrase区别：
term是输入内容不进行分词，去文档的倒排索引中去查找词项；
match_phrase是输入内容进行分词，拿着分词后的词项及词项之间的位置信息，去文书对应字段的倒排索引中匹配
这一组词项及位置信息，匹配到则认为是查找到。

GET /cdh-doc/civil/_search
{
    "query": {
        "term": {
            "party_info": "董事长"
        }
    }
}

GET /cdh-doc/civil/_search
{
    "query": {
        "match_phrase": {
            "party_info": "董事长"
        }
    }
}

短语词项间顺序、间隔控制：
GET /cdh-doc/civil/_search
{
    "query": {
        "match_phrase": {
            "reason": {
                "query": "同纠合",  #左移"合",再右移"同"，可以组合成"合同纠"进行匹配
                "slop":  1
            }
        }
    }
}
例如：待匹配的句子是："the quick brown fox jumped over the lazy dog."
如果使用"lazy jumped quick"来匹配上面的句子，要考虑3个单词，不管多少个单词，
slop表示的是间隔的最大距离；quick与lazy的距离最远，待匹配的句子中（移动待匹配句子或移动输入句子道理一样），
quick需要向右移动8次，才能与输入内容匹配；
多个词项移动，如何计算slop：https://blog.csdn.net/rick_123/article/details/6708527


多值字段（比如：数组字段）匹配：https://www.elastic.co/guide/cn/elasticsearch/guide/current/_multivalue_fields_2.html
例如："names": [ "John Abraham", "Lincoln Smith"]
Elasticsearch对数组的索引方式，与分析一个字符串一样，
忽略了数组符号[]的界限；
对["John Abraham","Lincoln Smith"]分词时和"John Abraham Lincoln Smith"一样！

分词结果信息：
Position 1: john
Position 2: abraham
Position 3: lincoln
Position 4: smith
造成搜索："Abraham Lincoln"时也能出来结果；
解决方法：建立索引时对字段设置正确的mapping：
"properties": {
        "names": {
        "type":                "text",
        "position_increment_gap": 100    #控制数组中的不同元素之间，位置按100递增
        }
    }

对[ "John Abraham", "Lincoln Smith"]分词结果为：
Position 1: john
Position 2: abraham
Position 103: lincoln
Position 104: smith

聚合：每个聚合都是一个或者多个桶和零个或者多个指标的组合。
GET /cdh-doc/civil/_search
{
   "aggs": {
      "reason_type_aggs": {
         "terms": {
            "field": "reason_type.keyword"
         },
         "aggs": {
            "avg_id": { "avg": { "field": "id" }  #统计的是reason_type.keyword分组下的值；
            },
            "judge_type_aggs" : {
                "terms" : {
                    "field" : "judge_type.keyword"
                },
                "aggs" : { 
                    "min_id" : { "min": { "field": "id"} }, #统计reason_type.keyword和judge_type.keyword分组下的值；
                    "max_id" : { "max": { "field": "id"} } 
                }
            }
         }
      }
   },
   "_source": ["reason_type","judge_type"]
  
}

# 范围查询和全局桶！
GET /cdh-doc/civil/_search
{
    "size" : 0,
    "query" : {
        "match" : {
            "reason_type.keyword" : "民事"
        }
    },
    "aggs" : {
        "civil_avg_id": {
            "avg" : { "field" : "id" } 
        },
        "all_doc_aggs": {    #全局桶
            "global" : {}, 
            "aggs" : {
                "all_avg_id": {
                    "avg" : { "field" : "id" } 
                }

            }
        }
    }
}

查询使用过滤器：
GET /cdh-doc/civil/_search
{
    "size" : 0,
    "query" : {
        "constant_score": {
            "filter": {
                "range": {
                    "id": {
                        "gte": 50
                    }
                }
            }
        }
    },
    "aggs" : {
        "single_avg_id": {
            "avg" : { "field" : "id" }
        }
    }
}
过滤桶：返回全部数据，聚合部分数据！
基于查询中的过滤器查询结果（代表返回结果数据），创建id_gte_50过滤桶（基于该桶进行统计）,
返回的结果是bool查询的结果，而聚合的结果是过滤桶的统计结果；互不影响！
GET /cdh-doc/civil/_search
{
   "size" : 0,
   "query":{
     "bool":{
       "must": [
         {"match": {"reason_type.keyword": "民事"}},
         {"match": {"judge_type.keyword": "判决"}}
         ]
       
     }
   },
   "aggs":{
      "id_gte_50": {
         "filter": { 
            "range": {
               "casedate": {
                  "gte": "2015-09-08"
               }
            }
         },
         "aggs": {
            "average_id":{
               "avg": {
                  "field": "id" 
               }
            }
         }
      }
   }
}

后过滤器：聚合全部数据，返回部分数据！
GET /cdh-doc/civil/_search
{
    "size": 0, 
    "query": {
        "match": {
            "reason_type.keyword": "民事"
        }
    },
    "post_filter": {    
        "term" : {
            "reason.keyword": "劳动争议"  #这里的字段可以不是分组的字段，分组只是给聚合来用，这里的过滤忽略分组。
        }
    },
    "aggs" : {
        "all_reason": {
            "terms" : { "field" : "reason.keyword" }
        }
    }
}
post_filter相当于having的作用！

过滤桶和后过滤器的区别：
过滤桶：不影响返回数据，聚合过滤桶内的数据！
后过滤器：只影响返回数据，返回后过滤器过滤之后的数据！
后过滤器使用任意字段针对query的结果再次过滤，过滤桶是在query的基础上，在自己的桶内聚合，过滤桶和后过滤器首先都是基于query的基础上操作，
为何使用后过滤器，而不在query中使用filter，加入后过滤其中的条件？比如query中过滤"福特"汽车，聚合是按颜色，最后使用后过滤器过滤"绿色"的
，汽车，直接在query中使用"福特","绿色"两个条件是可以的，但聚合分组后只显示"绿色"选项框，不合适，因此聚合就按所有的数据聚合，以得到
所有选项框，显示时使用后过滤器过滤绿色即可。
总结：
在filter 过滤中的 non-scoring 查询，同时影响搜索结果和聚合结果。
filter桶,影响聚合。
post_filter后过滤器，只影响搜索结果。

过滤桶和后过滤器组合：
GET /cdh-doc/civil/_search
{
   
   "query":{
     "bool":{
       "must": [
         {"match": {"reason_type.keyword": "民事"}},
         {"match": {"judge_type.keyword": "判决"}}
         ]
       
     }
   },
   "aggs":{
      "id_gte_50": {
         "filter": { 
            "range": {
               "casedate": {
                  "gte": "2015-09-08"
               }
            }
         },
         "aggs": {
            "average_id":{
               "avg": {
                  "field": "id" 
               }
            }
         }
      }
   },
    "post_filter": {    
        "term" : {
            "reason.keyword": "劳动争议"
        }
    }
}

多桶排序：默认的，桶会根据 doc_count 降序排列。
内置排序：
_count：按文档数排序。对 terms 、 histogram 、 date_histogram 有效。
_term：按词项的字符串值的字母顺序排序。只在 terms 内使用。
注意：排序输出的是聚合结果，而不是查询结果；
GET /cdh-doc/civil/_search
{   
    "aggs" : {
        "reason_aggs" : {
            "terms" : {
              "field" : "reason.keyword",
              "order": {
                "_count" : "desc" 
              }
            }
        }
    },
    "_source": ["reason","id"]
}

度量排序：
GET /cdh-doc/civil/_search
{
    "aggs" : {
        "reason_aggs" : {
            "terms" : {
              "field" : "reason.keyword",
              "order": {
                "avg_id" : "desc" 
              }
            },
            "aggs": {
                "avg_id": {
                    "avg": {"field": "id"} 
                }
            }
        }
    },
    "_source": ["id","reason"]
  
}



排序：英文官方文档参考：https://www.elastic.co/guide/en/elasticsearch/reference/6.4/search-request-sort.html

PUT /my_index/my_type/1?refresh
{
   "product": "chocolate",
   "price": [20,4,6,30]
}

POST /_search
{
   "query" : {
      "term" : { "product" : "chocolate" }
   },
   "sort" : [
      {"price" : {"order" : "asc", "mode" : "avg"}}
   ]
}
以下三种写法效果一样：
"sort": [{"id": {"order": "desc"}}]
"sort": {"id": {"order": "desc"}} 
"sort": {"id": "desc"} 
对应的升序写法如下：
"sort": "id" 
"sort": {"id":"asc"}
"sort": ["id"]


对多个字段排序：
"sort": ["reason.keyword","id"], 对两个字段依次升序；
"sort": ["reason.keyword",{"id":"desc"}], 对第一个字段升序，对第二个字段降序；

=====================
GET /cdh-doc/civil/_search
{
  "query": {
    "match": {"reason": "劳动"}
  },
  "sort": ["reason.keyword","_score"],
  "_source": ["id","reason"]
  
}

说明：
1、"_score"字段默认是降序的，其他所有字段默认都是升序的；
官方说明: The order defaults to desc when sorting on the _score, and defaults to asc when sorting on anything else.

2、对单值字段使用mode：min,max,sum,avg,median结果还是他自己，用它自己来进行排序。
order参数的值有：desc , asc
mode参数的值有：
1) min,max
2) sum,avg,median (仅用于数组或多值字段)

3、默认排序
是根据评分排序的
"sort":[{"_score":"desc"}]


4、空值及其排序：默认情况下，没有给定字段的文档，如果是升序，则会出现在第一个，如果是降序，则出现在最后一个；

mysql中的空字符串，在ES为"";
mysql中的空值（NULL），在ES为null;例如：id为3的文档lawlist字段为空：
"_source": {
          "lawlist": null,
          "id": 3
        },
es中判断lawlist是否为NULL：
#lawlist is not NULL in mysql
GET /cdh-doc/civil/_search
{
  "query": {
    "exists": {"field":"lawlist"}
  },
     "_source": ["id","lawlist"]
}
# lawlist is NULL in mysql
GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "lawlist"
        }
      }
    }
  },
  "_source": [
    "id",
    "lawlist"
  ]
}

使用含有值为NULL和""的lawlist排序：
GET /cdh-doc/civil/_search
{
  "size": 20, 
  "query": {
    "constant_score": {
      "filter": {"range": {
        "id": {
          "lte": 20
        }
      }}
    }
  },
  "sort": [{"lawlist.keyword":"desc"},"id"],
  "_source": ["id","lawlist"]  
}
当lawlist is null不存在时，lawlist不参与排序，无论升序还是降序，该文档都在最后面；
当lawlist is not null存在时，如果lawlist为"",升序时该文档在最前面，降序时该文档在最后面；
================
知识产权：
GET /criminal_0504_v2,civil_0504_v2,implement_0504,administration/_search
{ 
  "size": 20, 
  "query": {
    "terms": {
      "reason_uid": ["2005001","2005002"]
    }
  },
  "sort": [
    {
      "casedate": {
        "order": "desc"
      }
    }
  ]
  ,
  "_source": ["id","uuid","reason_uid", "reason","title"]
}


著作权：
GET /criminal_0504_v2,civil_0504_v2,implement_0504,administration/_search
{ 
  "size": 20, 
  "query": {
    "terms": {
      "reason_uid": ["2005001001","2005002001"]
    }
  },
  "sort": [
    {
      "casedate": {
        "order": "desc"
      }
    }
  ],
  "_source": ["id","uuid","reason_uid", "reason","title"]
}

商标合同纠纷：
GET /criminal_0504_v2,civil_0504_v2,implement_0504,administration/_search
{ 
  "size": 20, 
  "query": {
    "terms": {
      "reason_uid": ["2005001002","2005002002"]
    }
  },
  "sort": [
    {
      "casedate": {
        "order": "desc"
      }
    }
  ],
  "_source": ["id","uuid","reason_uid", "reason","title"]
}

专利权：
GET /criminal_0504_v2,civil_0504_v2,implement_0504,administration/_search
{ 
  "size": 20, 
  "query": {
    "terms": {
      "reason_uid": ["2005001003","2005002003"]
    }
  },
  "sort": [
    {
      "casedate": {
        "order": "desc"
      }
    }
  ],
  "_source": ["id","uuid","reason_uid", "reason","title"]
}
================
查看指定索引下的"类型"：
GET /legislation_0330/_search
{ 
  "size": 0, 
  "query": {
    "match_all": {}
  },
  "aggs": {
    "type_group": {
      "terms": {
        "field": "_type",
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
查看指定多个索引下的"类型"：
GET /a*,c*,i*,l*,r*,t*/_search
{ 
  "size": 0, 
  "query": {
    "match_all": {}
  },
  "aggs": {
    "index_type_group": {
      "terms": {
        "field": "_index",
        "order": {
          "_term": "asc"
        }
      },
      "aggs": {
        "type_group": {
          "terms": {
            "field": "_type",
            "order": {
              "_term": "asc"
            }
          }
        }
      }
    }
  }
}
=========================================
_all和自定义all字段：
1）_all和自定义all字段都只能被搜索，不能被返回；因为这两种字段不存储原始的数据
（不会拼接多个字段进行存储，也没有意义，因为一般都是看单个的原始字段，不会想看拼接的原始字段数据），
只是将其拼接的多个字段，分词后将词项存储在倒排索引中，以供搜索，但这种all字段本身不会返回。

2）_all字段默认开启，可在mapping中禁用（可以使用include_in_all属性决定是否包含在默认的_all字段中,
gai功能在6.0已经禁用，推荐使用copy_to方式自定义all字段）。
3）自定义all字段，在定义每个字段时，使用copy_to决定是否包含在自定义的all字段中。

如下：禁用_all字段，自定义my_all字段：
PUT cdh-doc2
{
  "settings": {
      "index": {
        "number_of_shards": "5",
        "number_of_replicas": "1"
      }
    },
    
  "mappings": {
      "test_all_alias": {
        "_all": {"enabled": false}, 
        
        "properties": {
          "my_all":{
            "type": "text",
            "analyzer": "standard"
          },
          
          "caseid": {
            "type": "text",
            "copy_to": "my_all", 
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "judge_type": {
            "type": "text",
            "copy_to": "my_all", 
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "reason_type": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    }
}
使用my_all字段查询：
GET /cdh-doc2/test_all_alias/_search
{
  "query": {
    "match": {
      "my_all": "辖"
    }
  },
  "_source": ["caseid","judge_type"]
}
==================================================
别名：alias



select * from es_adjudication_civil_etl_v2_100 where party_info = "" order by id;
select id,lawlist from es_adjudication_civil_etl_v2_100 where id < 20 and lawlist is null  order by id;
select * from es_adjudication_civil_etl_v2_100 where lawlist = "" or lawlist = " " order by id;
select * from es_adjudication_civil_etl_v2_100 where lawlist is null  order by id;
select lawlist,count(*) from es_adjudication_civil_etl_v2_100 where lawlist is not null group by lawlist;


select * from es_adjudication_civil_etl_v2_100 where lawlist is not null and lawlist != "";
select * from es_adjudication_civil_etl_v2_100 where caseid = "（2017）苏民申2367号"
select * from es_adjudication_civil_etl_v2_100 where CHAR_LENGTH(lawlist) < 3 and lawlist != ""


select * from es_adjudication_civil_etl_v2_100 where party_info like "%董事长%";
select * from es_adjudication_civil_etl_v2_100 where reason like "%劳__议%";


select reason_type,count(*),avg(id) from es_adjudication_civil_etl_v2_100 group by reason_type 
select avg(id) from es_adjudication_civil_etl_v2_100 group by reason_type 