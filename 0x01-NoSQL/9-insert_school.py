#!/usr/bin/env python3
"""
Utility module for inserting documents into a MongoDB collection
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """Insert a document into collection"""
    return mongo_collection.insert_one(kwargs).inserted_id
