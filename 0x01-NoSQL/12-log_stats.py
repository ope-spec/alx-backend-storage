#!/usr/bin/env python3
"""
Provide statistics about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """
    Provide statistics about Nginx logs stored in MongoDB
    """
    items = {}
    if option:
        value = mongo_collection.count_documents({"method": option})
        print(f"\tmethod {option}: {value}")
        return

    total_logs = mongo_collection.count_documents(items)
    print(f"{total_logs} logs")
    print("Methods:")
    for method in METHODS:
        log_stats(mongo_collection, method)
    status = mongo_collection.count_documents({"method":
                                               "GET", "path": "/status"})
    print(f"{status} status check")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_stats(nginx_collection)
