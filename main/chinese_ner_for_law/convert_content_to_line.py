# -*- coding: utf-8 -*-
import HTMLParser
html_parser = HTMLParser.HTMLParser()
import mysql.connector
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def conn_database():
    """connect database"""
    config={'host':'192.168.10.24',#默认192.168.32.2
            'user':'xwx',
            'password':'123456',
            'port':3306 ,#默认即为3306
            'database':'laws_doc',
            'charset':'utf8'#默认即为utf8
            }
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = conn.cursor()
    cursor.execute('select id, uuid, doc_content from judgment  where 1=1 limit 2 ;')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    """暂时先存成txt文档"""
    data_from_database = open("D:\\short_text_information_retrieval\\doc_content.txt", 'w')
    for i in range(len(values)):
        data_from_database.write(values[i][2].decode("utf8"))
        data_from_database.write("\n")
    data_from_database.close()

def format_html(content):
   """filter html tag"""
   content_text = HTMLParser.HTMLParser().unescape(content)
   from lxml import etree
   selector = etree.HTML(content_text)
   source_data = selector.xpath('string(*)').encode("utf8")
   return source_data


def convert_content_to_line(frpath,fwpath):
    """convert content to line"""
    fr = open(frpath, "r")
    fw = open(fwpath, "w")
    for line in fr.readlines():
        line = format_html(line)
        line = line.replace(' ', '')
        print line
        if line == "":
            continue
        line = unicode(line, "utf-8")
        for li in line:
            fw.write(li.encode("utf8"))
            if li == "\n":
                continue
            fw.write("\n")
    fr.close()
    fw.close()


if __name__ == "__main__":
    conn_database()
    convert_content_to_line("D:\\short_text_information_retrieval\\doc_content.txt", "D:\\short_text_information_retrieval\\original_doc_content.txt")
