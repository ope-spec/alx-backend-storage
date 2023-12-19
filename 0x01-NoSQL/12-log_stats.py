#!/usr/bin/env python3
"""
Provide statistics about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_nginx_stats(mongo_collection):
    """Provides statistics about Nginx logs"""
    num_logs = mongo_collection.estimated_document_count()
    print(f"{num_logs} logs")

    print("Methods:")
    for method in METHODS:
        method_count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_count} status check")


if __name__ == "__main__":
    mongo_client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = mongo_client.logs.nginx
    log_nginx_stats(nginx_collection)
