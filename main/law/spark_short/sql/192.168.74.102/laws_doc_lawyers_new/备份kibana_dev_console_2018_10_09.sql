DELETE /cdh-doc
GET /_cat/indices/cdh-doc
GET cdh-doc/_settings
GET /_cat/health?v
GET /_cat/nodes?v
GET /_cat/indices/
GET _cat/shards
GET /_cat/shards/cdh-doc

GET /cdh-doc/_mapping

PUT cdh-doc
{
  "settings": {
      "index": {
        "number_of_shards": "5",
        "number_of_replicas": "1"
      }
    },
    
  "mappings": {
      "civil": {
        "properties": {
          "casedate": {
            "type": "date"
          },
          "caseid": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "court": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "court_find": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "court_idea": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "court_uid": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "doc_footer": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "id": {
            "type": "long"
          },
          "judge_result": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "judge_type": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "law_id": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "lawlist": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "party_info": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "province": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "reason": {
            "type": "text",
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
          },
          "reason_uid": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "title": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "trial_process": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "trial_request": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "type": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "uuid": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "uuid_old": {
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


GET /cdh-doc/civil/2
GET /cdh-doc/_mapping/civil

GET /cdh-doc/civil/_search
{
  "bool": {
      "must": { "match":   { "email": "business opportunity" }},
      "should": [
          { "match":       { "starred": true }},
          { "bool": {
              "must":      { "match": { "folder": "inbox" }},
              "must_not":  { "match": { "spam": true }}
          }}
      ],
      "minimum_should_match": 1
  }
}

GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
        "must":     { "match": { "court": "江苏省高级人民法院" }},
        "must_not": { "match": { "reason":  "劳动" }},
        "should":   { "match": { "casedate": "2017-04-11" }},
        "filter":   { "range": { "id" : { "gt" :  10}} }
    }
  }
}

GET /cdh-doc/_mapping/civil

GET cdh-doc/civil/_search
{
  "query": {
    
     "match_all": {}
  }
}

GET cdh-doc/civil/_search
{
  "query": {
     "match": {
       "casedate": "2017-03-30"
     }
  }
}

GET cdh-doc/civil/_search
{
  "query": {
     "match": {
       "doc_footer": "章芳芳"
     }
  }
}


GET cdh-doc/civil/_search
{
  "query": {
     "match": {
       "doc_footer.keyword": "章芳芳"
     }
  }
}


GET cdh-doc/civil/_search
{
  "query": {
     "multi_match": {
       "query": "章芳芳", 
       "fields": ["doc_footer.keyword","trial_request"]
     }
  }, 
  
  "_source": ["id","doc_footer","trial_request"]  

}

GET cdh-doc/civil/_search
{
  "query": {
     "term": {
       "id": 20
     }
  }  ,
  "_source": ["id","casedate"]
}

GET cdh-doc/civil/_search
{
  "query": {
     "term": {
       "casedate": "2017-06-02"
     }
  }  , 
  "_source": ["id","casedate"]
}

GET cdh-doc/civil/_search
{
  "query": {
     "terms": {
       "casedate": ["2017-05-08","2017-09-22"]
     }
  }  , 
  "_source": ["id","casedate"]
}

GET cdh-doc/civil/_search
{
  "query": {
     "term": {
       "lawlist.keyword": " "
     }
  }  , 
  "_source": ["id","casedate","lawlist","caseid"]
}

GET cdh-doc/civil/_search
{
  "query": {
    "bool": {
      "must": {
        "term": {"caseid": "2401"}
      }, 
      "must": {
        "term": {"caseid": "苏"}
      }
    }
  }  , 
  "_source": ["id","casedate","lawlist","caseid"]
}

GET /_analyze
{
  "analyzer": "standard",
  "text": "（2016） 苏民申2401号"
}


GET cdh-doc/civil/_search
{
  "query": {
     "match": {
       "caseid.keyword": "（2016） 苏民申2401号"
     }
  }  , 
  "_source": ["id","casedate","lawlist"]
}

GET cdh-doc/civil/_search
{
  "query": {
     "range": {
       "casedate": {
         "gt": "2018",
         "lt": "2021"
       }
     }
  }
  
  , "_source": ["id","casedate"]
}

GET cdh-doc/civil/_search
{
  "query": {
     "range": {
       "id": {
         "gte": "1",
         "lt": "10"
       }
     }
  }
  
  , "_source": ["id","casedate"]
}

GET /cdh-doc/civil/_search
{
  "query": {
    "exists":{
      "field":"lawlist"
    }
  }
  , "_source": ["id","casedate","lawlist"]
}



# = missing
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
    "casedate",
    "lawlist"
  ]
}


GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
      "must": [
        {"": {
          "casedate": {
            "value": "2017-05-27"
          }
        }},
        {"exists": {
          "field":"lawlist"
        }}
        ]
    }
     }
  , "_source": ["id","casedate","lawlist"]
}



# query explain and validate

GET /cdh-doc/civil/_validate/query?explain 
{
   "query": {
      "match" : {
         "caseid" : "刑事案号 "
      }
   }
}


# bool query
GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
          "must":{ "match": { "reason_type": "民事" }},
          "must_not": { "match": { "judge_type":   "判决" }},
          "should": [
              { "match": { "party_info": "判决" }},
              { "range": { "casedate": { "gte": "2017-04-01" }}}
          ]
          
    }
  },
  "_source": ["id","reason_type","judge_type","party_info", "casedate"]
}


GET /cdh-doc/civil/_search
{
  "query": {
    "bool": {
          "must":{ "match": { "reason_type": "民事" }},
          "must_not": { "match": { "judge_type":   "判决" }},
          "should": 
              { "match": { "party_info": "判决" }},
          "filter": {
               "range": {"casedate": {"gte": "2017-04-01"}}}
    }
  }

}

#GET /cdh-doc/civil/_validate/query?explain 

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

GET /cdh-doc/civil/_search
{
  "range" : {
    "title" : {
        "gte" : "a",
        "lt" :  "b"
    }
}
}


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

"must":{"range": { "id": { "gte": 2 }}},
          "must_not": { "term": { "reason": "劳动争议" }},
          "must_not": { "term": { "reason.keyword": "劳动争议" }},

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

GET /cdh-doc/civil/_search
{
  "query": {
    "match_all": {}
  }
}

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


GET /cdh-doc/civil/_search
{
    "query": {
        "match": {
            "caseid": {      
                "query":    "苏1145",
                "operator": "and"
            }
        }
    }
}

GET /_analyze
{
  "analyzer": "standard",
  "text": "故意劳工"
}

GET /cdh-doc/civil/_search
{
  "query": {
    "match": {
      "reason": {
        "query": "工纠纷",
        "minimum_should_match": "2"
      }
    }
  }
}


#"minimum_should_match"
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

#must and must_not deep understand !
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
  },
  "_source": ["id","reason"]
}


GET /_analyze
{
  "analyzer": "standard",
  "text": "1234||3639"
}



GET /_analyze
{
  "analyzer": "standard",
  "text": "人力资源经理"
}

# term vs  match_phrase：
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


#match_phrase:
GET /_analyze
{
  "analyzer": "standard",
  "text": "劳动争议||装饰装修合同纠纷||合同纠纷"
}

GET /cdh-doc/civil/_search
{
    "query": {
        "match_phrase": {
            "reason": {
                "query": "同纠合",
                "slop":  1
            }
        }
    }
}


# aggregations

GET /cdh-doc/civil/_search
{
   "size" : 0,
   "aggs": {
      "reason_type_aggs": {
         "terms": {
            "field": "reason_type.keyword"
         },
         "aggs": {
            "avg_id": { "avg": { "field": "id" }
            },
            "judge_type_aggs" : {
                "terms" : {
                    "field" : "judge_type.keyword"
                },
                "aggs" : { 
                    "min_id" : { "min": { "field": "id"} }, 
                    "max_id" : { "max": { "field": "id"} } 
                }
            }
         }
      }
   }
}

GET /cdh-doc/civil/_search
{
   "aggs": {
      "reason_type_aggs": {
         "terms": {
            "field": "reason_type.keyword"
         },
         "aggs": {
            "avg_id": { "avg": { "field": "id" }
            },
            "judge_type_aggs" : {
                "terms" : {
                    "field" : "judge_type.keyword"
                },
                "aggs" : { 
                    "min_id" : { "min": { "field": "id"} }, 
                    "max_id" : { "max": { "field": "id"} } 
                }
            }
         }
      }
   },
   "_source": ["reason_type","judge_type"]
  
}

# range query and all_buckets！
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
        "all_doc_aggs": {
            "global" : {}, 
            "aggs" : {
                "all_avg_id": {
                    "avg" : { "field" : "id" } 
                }

            }
        }
    }
}


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

# filter buckets:
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
   }
}

#post filter:
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
            "reason.keyword": "劳动争议"
        }
    },
    "aggs" : {
        "all_reason": {
            "terms" : { "field" : "reason.keyword" }
        }
    }
}

#filter buckets and post filter:
GET /cdh-doc/civil/_search
{ 
  "query": {
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

#使用含有值为NULL和""的lawlist排序：
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
#========================================================================
#ES索引
#legislation_0330/single,book/
#lawyer_0330
#lawyer_v2
#implement_0504
#criminal_0504_v2
#completion_0330/court,reason/
#civil_0504_v2
#administration

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

#aggs demo
GET /cdh-doc/civil/_search
{
   "aggs": {
      "reason_type_aggs": {
         "terms": {
            "field": "reason_type.keyword"
         },
         "aggs": {
            "avg_id": { "avg": { "field": "id" }
            },
            "judge_type_aggs" : {
                "terms" : {
                    "field" : "judge_type.keyword"
                },
                "aggs" : { 
                    "min_id" : { "min": { "field": "id"} }, 
                    "max_id" : { "max": { "field": "id"} } 
                }
            }
         }
      }
   },
   "_source": ["reason_type","judge_type"]
}

GET /criminal_0504_v2,civil_0504_v2,implement_0504,administration/_search


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


#著作权
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

#商标合同纠纷
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

#专利权
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

#============================
#_all字段：
GET /cdh-doc/civil/_search
{ 
  "query": {
    "match": {
      "_all":"曹继明"
    }
  },
  "_source": "id"
}


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

DELETE cdh-doc2
GET /cdh-doc2/_mapping

GET /cdh-doc2/test_all_alias/_search
{
  "query": {
    "match_all": {}
  }
}


GET /cdh-doc2/test_all_alias/_search
{
  "query": {
    "match": {
      "my_all": "辖"
    }
  },
  "_source": ["caseid","judge_type"]
}

#===alias===========================================
GET _cat/aliases

#创建一个别名，包含多个索引
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "cdh-doc",
        "alias": "my_cdh_alias"
      }
    },
    {
      "add": {
        "index": "cdh-doc2",
        "alias": "my_cdh_alias"
      }
    }
  ]
}

#移除别名下关联的索引（可以使用通配符），当最后一个关
#联索引被移除时，别名也就被删除了：
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "cdh-doc", 
        "alias": "my_cdh_alias"
      }
    }
  ]
}

POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "cdh-doc*", 
        "alias": "my_cdh_alias*"
      }
    }
  ]
}

#别名没有修改的语法，要修改别名，需要先删别名,然后在添加别名。：
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "cdh-doc",
        "alias": "my_cdh_alias"
      }
    },
    {
      "add": {
        "index": "cdh-doc",
        "alias": "my_cdh_alias2"
      }
    }
  ]
}


#使用别名查询
GET /my_cdh_alias/_search
{
  "query": {
    "term": {
      "_type": {
        "value": "civil"
      }
    }
  }
}


#对于同一个index，我们给不同人看到不同的数据：
#创建带过滤器的别名
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "my_index",
        "alias": "my_index__teamA_alias",
        "filter":{
            "term":{
                "team":"teamA"
            }
        }
      }
    },
    {
      "add": {
        "index": "my_index",
        "alias": "my_index__teamB_alias",
        "filter":{
            "term":{
                "team":"teamB"
            }
        }
      }
    },
    {
      "add": {
        "index": "my_index",
        "alias": "my_index__team_alias"
      }
    }
  ]
}
#============原始律师数据创建别名==================
DELETE lawyers-origin

GET /lawyers-origin/_search
GET /lawyers-origin/_mapping

GET _cat/aliases

#索引：lawyers-origin，别名：hht_lawyer(新律协数据),12348gov（法网）,lawyer_info（旧律协）

POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "lawyers-origin", 
        "alias": "lawyers-origin*"
      }
    }
  ]
}

#前缀查询：https://blog.csdn.net/dm_vincent/article/details/42001851
#正则查询：https://blog.csdn.net/shiyaru1314/article/details/46895939
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "lawyers-origin",
        "alias": "lawyers-origin-hht_lawyer",
        "filter":{
            "prefix":{
                "table_name.keyword":"hht_lawyer"
            }
        }
      }
    },
    {
      "add": {
        "index": "lawyers-origin",
        "alias": "lawyers-origin-12348gov",
        "filter":{
            "prefix":{
                "table_name.keyword":"zy_lawyer"
            }
        }
      }
    },
    {
      "add": {
        "index": "lawyers-origin",
        "alias": "lawyers-origin-lawyer_info",
        "filter":{
            "prefix":{
                "table_name.keyword":"lawyer_info"
            }
        }
      }
    }
  ]
}

#lawyers-origin-hht_lawyer
#lawyers-origin-lawyer_info
#lawyers-origin-12348gov
#lawyers-origin
GET /lawyers-origin-hht_lawyer/_search
{
  "query": {
    "match_all": {}
  }
}

GET /lawyers-origin-lawyer_info/_search
{
  "query": {
    "match_all": {}
  }
}

GET /laws_0504/_search

GET /criminal_0504_v2,civil_0504_v2,implement_0504,administration/_search
{
  "query": {
    "term": {
      "uuid.keyword": {
        "value": "1afb60f7cbc3374ca4fab1bcb02801d1"
      }
    }
  }
}
