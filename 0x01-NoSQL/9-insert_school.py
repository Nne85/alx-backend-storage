#!/usr/bin/env python3
"""
This module inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    This inserts a new document in a collection based on kwargs

    Args:
        mongo_collection
        kwargs

    Returns:
        new _id
    """
    return mongo_collection.insert_one(kwargs).inserted_id
