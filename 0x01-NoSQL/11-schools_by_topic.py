#!/usr/bin/env python3
"""
find specific documents
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """ find and return documents matching query """
    schools = list(mongo_collection.find({}))
    return [school for school in schools if topic in school.get("topics")]