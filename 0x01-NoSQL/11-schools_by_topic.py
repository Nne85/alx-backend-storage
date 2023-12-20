#!/usr/bin/env python3
"""
function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    list of schools having a specific topic
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return mongo_collection.find(topic_filter)
