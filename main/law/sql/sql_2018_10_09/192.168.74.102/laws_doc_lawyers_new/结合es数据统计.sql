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

_source：返回哪些字段，= select
multi_match：一个值去匹配多个字段。
"multi_match": {
       "query": "章芳芳", 
       "fields": ["doc_footer","trial_request"]
等价于：
doc_footer like "%章芳芳%" or trial_request like "%章芳芳%"

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
注意：一个must或must_not或should只能对应一个查询语句，就类似：
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

ctrl+i 自动缩进
ctrl+enter 提交请求
ctrl + 上下键，跳到一个代码块的开头或结尾；

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
一般的match匹配：匹配"苏"或"1145"
GET /cdh-doc/civil/_search
{
    "query": {
        "match": {
            "caseid": "苏1145"
        }
    }
}

多词同时匹配：匹配"苏"和"1145"，同时查询结构有些改变；
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


多词同时匹配：匹配至少两个词，同时查询结构有些改变；
{
  "query": {
    "match": {
      "reason": {
        "query": "苏1145",
        "minimum_should_match": "2"
      }
    }
  }
}

match 查询支持 minimum_should_match 最小匹配参数，可以指定必须匹配的词项数（分词后的词项）
或者在bool组合查询中should语句匹配的个数。
minimum_should_match可以设置为某个具体数字，更常用的做法是将其设置为一个百分数，
因为我们无法控制用户搜索时输入的单词数量：

组合查询及多次匹配：
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
bool查询与match查询的等价转换：
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
如果使用 and 操作符，所有的 term 查询都被当作 must 语句，所以 所有（all） 语句都必须匹配。
以下两个查询是等价的：

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
深入搜索：全文检索
1、查询语句提升权重：https://www.elastic.co/guide/cn/elasticsearch/guide/current/_boosting_query_clauses.html
增加boost参数！

2、控制分析：https://www.elastic.co/guide/cn/elasticsearch/guide/current/_controlling_analysis.html
设置分词器，不同字段也可以设置不同的分词器，检索使用分词器的顺序！

深入搜索：多字段搜索；
multi_match:多字段查询
{
    "multi_match": {
        "query":    "判决",
        "fields":   [ "caseid", "judge_type" ]
    }
}
terms: 多词查询
"query": {
     "terms": {
       "casedate": ["2017-05-08","2017-09-22"]
     }
  }


最佳字段：best_fields
{
    "multi_match": {
        "query":                "Quick brown fox",
        "type":                 "best_fields", 
        "fields":               [ "title", "body" ],
        "tie_breaker":          0.3,
        "minimum_should_match": "30%" 
    }
}
多字段查询：将 type 设置成 most_fields， 告诉 Elasticsearch 合并所有匹配字段的评分：
{
  "query": {
    "multi_match": {
      "query":       "Poland Street W1V",
      "type":        "most_fields",
      "fields":      [ "street", "city", "country", "postcode" ]
    }
  }
} 


_all字段：https://www.elastic.co/guide/cn/elasticsearch/guide/current/root-object.html#all-field
自定义_all字段：https://www.elastic.co/guide/cn/elasticsearch/guide/current/custom-all.html
例子：first_name 和 last_name 字段中的值会被复制到 full_name 字段。
copy_to 设置对multi-field无效（类似默认keyword类型的字段），如果尝试这样配置映射，Elasticsearch 会抛异常。
为什么呢？多字段只是以不同方式简单索引“主”字段；它们没有自己的数据源。也就是说没有可供 copy_to 到另一字段的数据源。
PUT /my_index
{
    "mappings": {
        "person": {
            "properties": {
                "first_name": {
                    "type":     "string",
                    "copy_to":  "full_name" 
                },
                "last_name": {
                    "type":     "string",
                    "copy_to":  "full_name" 
                },
                "full_name": {
                    "type":     "string"
                }
            }
        }
    }
}

GET /_validate/query?explain
{
    "query": {
        "multi_match": {
            "query":       "peter smith",
            "type":        "most_fields",
            "operator":    "and", 
            "fields":      [ "first_name", "last_name" ]
        }
    }
}
逻辑如下：
(+first_name:peter +first_name:smith)
(+last_name:peter  +last_name:smith)

GET /_validate/query?explain
{
    "query": {
        "multi_match": {
            "query":       "peter smith",
            "type":        "cross_fields",
            "operator":    "and", 
            "fields":      [ "first_name", "last_name" ]
        }
    }
}
逻辑如下：
+(first_name:peter last_name:peter)
+(first_name:smith last_name:smith)
换句话说，词 peter 和 smith 都必须出现，但是可以出现在任意字段中。

使用自定义_all字段和cross_fields（跨字段搜索）都能达到多字段搜索效果，跨字段搜索还能指定某个字段的权重！

短语匹配：https://www.elastic.co/guide/cn/elasticsearch/guide/current/phrase-matching.html



=================================================================
select * from es_adjudication_civil_etl_v2_100 where lawlist is not null and lawlist != "";
select * from es_adjudication_civil_etl_v2_100 where caseid = "（2017）苏民申2367号"
select * from es_adjudication_civil_etl_v2_100 where CHAR_LENGTH(lawlist) < 3 and lawlist != ""


