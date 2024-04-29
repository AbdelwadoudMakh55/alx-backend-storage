#!/usr/bin/env python3
"""
Insert document inside MongoDB collection
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ insert document and return id """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id