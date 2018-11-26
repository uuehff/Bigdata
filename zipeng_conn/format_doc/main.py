#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
对抓取的文书内容进行数据提取
"""
from multiprocessing import Pool

import pymysql
from store_data import select_data, update_data
from common import format_content


def doc_items(items):
    item_id = items.get('id')
    doc_content = items.get('doc_content')
    conditions = {'id': item_id}

    if not doc_content:
        conditions = {'id': item_id}
        value_dict = {'is_crawl': 0, 'is_format': 5}
        update_data(conditions=conditions, value=value_dict)
        return False

    if not doc_content.endswith('/div&gt;'):
        conditions = {'id': item_id}
        value_dict = {'is_crawl': 0, 'is_format': 2}
        update_data(conditions=conditions, value=value_dict)
        return False

    # print(item_id)
    content_text = format_content(doc_content)

    # 格式化后的内容
    content = content_text.get('content')
    if len(content) < 120:
        value_dict = {'is_format': 3}
        update_data(conditions=conditions, value=value_dict)
        return False

    party_info = content_text.get('member', '')
    trial_process = content_text.get('process', '')
    trial_request = content_text.get('request', '')
    court_find = content_text.get('fact', '')
    court_idea = content_text.get('idea', '')
    judge_result = content_text.get('result', '')

    court_find = pymysql.escape_string(court_find)
    trial_process = pymysql.escape_string(trial_process)
    trial_request = pymysql.escape_string(trial_request)
    court_idea = pymysql.escape_string(court_idea)
    judge_result = pymysql.escape_string(judge_result)

    items_dict = dict(party_info=party_info, trial_process=trial_process, trial_request=trial_request,
                      court_find=court_find, court_idea=court_idea, judge_result=judge_result, is_format=1)

    return item_id, items_dict


def worker(items):
    try:
        items_dict = doc_items(items)
    except Exception as error:
        print(error)
    else:
        if isinstance(items_dict, tuple):
            item_id = items_dict[0]
            conditions = {'id': item_id}
            update_data(conditions=conditions, value=items_dict[1])


def format_main():
    while 1:
        pool = Pool(24)
        rows = select_data()
        if not rows:
            break
        pool.map(worker, rows)
        pool.close()
        pool.join()



if __name__ == "__main__":
    format_main()

