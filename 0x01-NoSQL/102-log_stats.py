#!/usr/bin/env python3
"""This module provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def main():
    """ This function connects to MongoDB and prints stats"""
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs
    collection = db.nginx

    # Count total documents
    document_count = collection.count_documents({})

    # Count documents by HTTP method
    method_counts = {
            "GET": collection.count_documents({"method": "GET"}),
            "POST": collection.count_documents({"method": "POST"}),
            "PUT": collection.count_documents({"method": "PUT"}),
            "PATCH": collection.count_documents({"method": "PATCH"}),
            "DELETE": collection.count_documents({"method": "DELETE"}),
    }
    # Count GET requests for "/status" path
    status_checks = collection.count_documents({"method": "GET",
                                               "path": "/status"})

    # Prints Results
    print(f"{document_count} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")

    print('IPs:')
    request_logs = collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))


if __name__ == "__main__":
    main()
