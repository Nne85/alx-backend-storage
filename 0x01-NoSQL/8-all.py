#!/usr/bin/env python3
"""This module  lists all documents in a collection:"""


def list_all(mongo_collection):
    """
    Lists all documents in a pymongo collection.

    Args:
       mongo_collection: A pymongo collection object.

    Returns:
       A list of documents in the collection.A list of documents in the collection.
    """
    return mongo_collection.find()
