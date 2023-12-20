#!/usr/bin/env python3

"""This module prints log stats"""

from pymongo import MongoClient


def main():
    # Connect to MongoDB
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
    status_checks = collection.count_documents({"method": "GET", "path": "/status"})

    # Aggregate top 10 most frequent IPs
    top_ips = collection.aggregate(
        [
            {
                "$group": {
                    "_id": "$client_ip",
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": { "count": -1 }
            },
            { "$limit": 10 }  # Limit to top 10 IPs
        ]
    )

    # Print output
    print(f"{document_count} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")
    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip['_id']
        ip_count = top_ip['count']
        print('\t{}: {}'.format(ip, ip_count))


if __name__ == "__main__":
    main()
