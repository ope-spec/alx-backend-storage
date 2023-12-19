#!/usr/bin/env python3
"""Module for finding schools by topic"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """Find schools with the specified topic"""
    return mongo_collection.find({"topics": topic})
