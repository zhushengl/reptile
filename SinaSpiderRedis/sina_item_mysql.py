# -*- coding:utf-8 -*-
# import MySQLdb
import mysql.connector
import redis
import json


def main():
    redis_connect = redis.StrictRedis(host='localhost', port=6379, db=0)
    mysql_connect = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', passwd='root', database='sina',
                                            use_unicode=True)

    while redis_connect.exists('sina:items'):
        source, data = redis_connect.blpop('sina:items')
        item = json.loads(data, encoding='utf-8')
        cur = mysql_connect.cursor()
        cur.execute(
            'insert into sina_articles(parent_title, parent_url, sub_title, sub_url, sub_path, file_url, '
            'file_title, file_content, crawled, spider) '
            'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (item['parent_title'], item['parent_url'], item['sub_title'], item['sub_url'], item['sub_path'],
             item['file_url'], item['file_title'], item['file_content'], item['crawled'], item['spider']))
        mysql_connect.commit()
        cur.close()
    mysql_connect.close()


if __name__ == "__main__":
    main()
