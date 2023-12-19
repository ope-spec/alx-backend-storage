#!/usr/bin/env python3
"""
Utility module for listing all documents in a MongoDB collection
"""


def list_all(mongo_collection):
    """List all documents in a collection"""
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
