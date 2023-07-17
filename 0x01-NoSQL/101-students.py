#!/usr/bin/env python3
"""Return all students sorted by average score"""


def top_students(mongo_collection):
    """Return all students sorted by average score"""
    students = mongo_collection.find()
    students = [student for student in students]
    for student in students:
        topics = student["topics"]
        score = 0
        for topic in topics:
            score += topic["score"]
        score /= len(topics)
        student["averageScore"] = score
    students = sorted(students, key=lambda x: x["averageScore"], reverse=True)
    return students
