#!/usr/bin/env python3
"""
Nginx logs stats
"""
from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    col = client.logs.nginx
    print(f'{col.count_documents({})} logs')
    print("Methods:")
    print(f'\tmethod GET: {col.count_documents({"method": "GET"})}')
    print(f'\tmethod POST: {col.count_documents({"method": "POST"})}')
    print(f'\tmethod PUT: {col.count_documents({"method": "PUT"})}')
    print(f'\tmethod PATCH: {col.count_documents({"method": "PATCH"})}')
    print(f'\tmethod DELETE: {col.count_documents({"method": "DELETE"})}')
    print(f'{col.count_documents({"method": "GET", "path": "/status"})} status check')
    match_ip = {"$group": {"_id": "$ip", "count": {"$sum": 1}}}
    sort_by_count = {"$sort": {"count": -1}}
    pipeline = [match_ip, sort_by_count]
    ips_by_log = list(col.aggregate(pipeline))
    print("IPs:")
    for i in range(10):
        print(f'\t{ips_by_log[i].get("_id")}: {ips_by_log[i].get("count")}')