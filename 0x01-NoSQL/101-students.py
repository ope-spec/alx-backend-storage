#!/usr/bin/env python3
"""For retrieving top students by average score"""


def top_students(mongo_collection):
    """Retrieve students sorted by average score"""
    pipeline = [
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    return mongo_collection.aggregate(pipeline)
