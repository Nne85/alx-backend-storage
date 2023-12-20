#!/usr/bin/env python3
"""
This module returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """
    This function returns returns the list of school having a specific topic
    """
    topic_filter = {
            "topic": {
                "elemmatch": {
                    "$eq": topic,
                    },
                },
            }
    return mongo_collection.find(topic_filter)
