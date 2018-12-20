# -*- coding:utf-8 -*-
import redis
import json
from openpyxl import Workbook


def main():
    redis_connect = redis.StrictRedis(host='localhost', port=6379, db=0)

    while redis_connect.exists('sina:items'):
        source, data = redis_connect.blpop('sina:items')
        item = json.loads(data, encoding='utf-8')
        ws.append([item['id'],
                   item['classification'],
                   item['shopName'],
                   item['address'],
                   item['foodInformation'][0]['rating'],
                   item['foodInformation'][0]['price'],
                   item['foodInformation'][0]['Evaluation'],
                   item['foodInformation'][0]['foodName'],
                   item['foodInformation'][0]['sale']])
    wb.save('nba.xlsx')  # 保存文件


if __name__ == "__main__":
    wb = Workbook()  # class实例化
    ws = wb.active  # 激活工作表
    ws.title = "New Shit"
    title_list = ['id', 'classification', 'shopName', 'address', 'rating', 'price', 'Evaluation', 'foodName', 'sale']
    ws['A1'] = '饿了么'
    ws.append(title_list)  # 添加一行数据

    main()
