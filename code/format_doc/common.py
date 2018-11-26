#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
文书内容清洗主要函数文件
"""
import html
import re

from lxml import etree

__author__ = "风轻清淡"

reg_link = re.compile(r"<a[^>]+>|</a>", flags=re.S)
reg_blank = re.compile(r'((?!\n)\s)*', flags=re.S)
reg_part = re.compile(r'<span litigantpart></span>')
reg_process = re.compile(r'<span proceeding></span>')
reg_argued = re.compile(r'<span argued></span>')
reg_fact = re.compile(r'<span fact></span>')
reg_court = re.compile(r'<span courtconsider></span>')
reg_result = re.compile(r'<span result></span>')


def format_content(content):
    """
    理脉网内容分段
    :param content:
    :return:
    """

    content_dict = dict()
    content_text = html.unescape(content)
    content_text = re.sub(reg_link, "", content_text)

    part_list = re.split(reg_part, content_text)
    if len(part_list) == 2:
        content_dict['head'] = remove_html(part_list[0])

    content_dict['content'] = remove_html(part_list[-1])
    process_list = re.split(reg_process, part_list[-1])
    if len(process_list) == 2:
        content_dict['member'] = remove_html(process_list[0])

    argued_list = re.split(reg_argued, process_list[-1])
    if len(argued_list) == 2:
        content_dict['process'] = remove_html(argued_list[0])

    fact_list = re.split(reg_fact, argued_list[-1])
    if len(fact_list) == 2:
        content_dict['request'] = remove_html(fact_list[0])

    court_list = re.split(reg_court, fact_list[-1])
    if len(court_list) == 2:
        content_dict['fact'] = remove_html(court_list[0])

    result_list = re.split(reg_result, court_list[-1])
    if len(result_list) == 2:
        content_dict['idea'] = remove_html(result_list[0])

    content_dict['result'] = remove_html(result_list[-1])

    return content_dict


def remove_html(html_data):
    """
    移除HTML标签
    :param html_data:
    :return:
    """
    html_item = re.sub(reg_blank, "", html_data)
    if html_item:
        item_list = etree.HTML(html_item).xpath('//text()')
        html_text = "\n".join(item_list).strip()
    else:
        html_text = ''
    return html_text


if __name__ == "__main__":
    pass
