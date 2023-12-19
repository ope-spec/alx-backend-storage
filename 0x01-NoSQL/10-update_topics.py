#!/usr/bin/env python3
"""Module for updating school topics"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """Update topics for multiple documents"""
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
