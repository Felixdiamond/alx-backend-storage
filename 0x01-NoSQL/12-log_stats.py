#!/usr/bin/env python3
"""Provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    num_docs = logs_collection.count_documents({})
    print(f"{num_docs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        num_method = logs_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {num_method}")

    num_status = logs_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{num_status} status check")
