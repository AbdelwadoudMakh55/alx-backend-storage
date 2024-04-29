#!/usr/bin/env python3
"""
sort students by avg score
"""


def top_students(mongo_collection):
    """ Return students sorted by avg score """
    students = list(mongo_collection.find({}))
    for student in students:
        if len(student.get('topics')) > 0:
            avg = sum([topic.get('score') for topic in student.get('topics')]) \
                  / len(student.get('topics'))
            value = {'$set': {'averageScore': avg}}
            mongo_collection.update_many({"name": student.get('name')}, value)
    return list(mongo_collection.find().sort("averageScore", -1))
