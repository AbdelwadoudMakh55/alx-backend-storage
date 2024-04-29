#!/usr/bin/env python3
"""
Update document inside MongoDB collection
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """ update document """
    mongo_collection.update_one({"name": name}, { "$set": {"topics": topics}})