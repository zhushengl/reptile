# -*- coding:utf-8 -*-
import redis
import pymongo
import json


def main():
    redis_connect = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    mongo_connect = pymongo.MongoClient(host='127.0.0.1', port=27017)

    db = mongo_connect['sina']
    collection = db['sina_articles']

    while True:
        source, data = redis_connect.blpop(['sina:items'])
        item = json.loads(data)
        collection.insert(item)


if __name__ == '__main__':
    main()





