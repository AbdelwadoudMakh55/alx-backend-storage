#!/usr/bin/env python3
"""
Listing all documents inside MongoDB collection
"""
import pymongo


def list_all(mongo_collection):
    """ return all documents """
    return list(mongo_collection.find({}))