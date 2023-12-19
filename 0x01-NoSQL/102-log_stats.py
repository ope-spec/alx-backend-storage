#!/usr/bin/env python3
"""
top 10 of the most present IPs in the collection
nginx of the database logs
"""
from pymongo import MongoClient


def nginx_stats_check():
    """ Provides some statistics about Nginx logs stored"""
    client = MongoClient()
    collection = client.logs.nginx

    logs_count = collection.count_documents({})
    print(f"{logs_count} logs")
    print("Methods:")

    http_mtd = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_mtd:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status} status check")

    print("IPs:")

    latest_ips = collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for latst_ip in latest_ips:
        count = latst_ip.get("count")
        ip_address = latst_ip.get("ip")
        print(f"\t{ip_address}: {count}")


if __name__ == "__main__":
    nginx_stats_check()
