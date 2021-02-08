#!/usr/bin/env python
# coding: utf-8

# In[5]:


import xml.etree.cElementTree as ET
import codecs
import pprint
import json
import re
from collections import defaultdict

db_name = "vegas"

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    return db


def top_users():
    # Top 10 contributing users
    group = {"$group" : {'_id' : '$created.user', 'count' : {'$sum' : 1}}}
    sort = {"$sort" : {'count' : -1}}
    limit = {"$limit" : 10}
    pipeline = [group, sort, limit]
    return pipeline

def top_cities():
    # Top 10 mentioned cities
    match = {"$match":{"address.city":{"$exists":1}}}
    group = {"$group":{"_id":"$address.city", "count":{"$sum":1}}}
    sort = {"$sort":{"count":-1}}
    limit = {"$limit":10}
    pipeline = [match, group, sort, limit]
    return pipeline

def top_amenities():
    # Top 10 appearing amenities
    match = {"$match":{"brand":{"$exists":1}}}
    group = {"$group":{"_id":"$brand", "count":{"$sum":1}}}
    sort = {"$sort":{"count":-1}}
    limit = {"$limit":10}
    pipeline = [match, group, sort, limit]
    return pipeline

def top_leisure_facilities():
    # Top 10 mentioned leisure facilities 
    match = {"$match":{"leisure":{"$exists":1}}}
    group = {"$group":{"_id":"$leisure", "count":{"$sum":1}}}
    sort = {"$sort":{"count":-1}}
    limit = {"$limit":10}
    pipeline = [match, group, sort, limit]
    return pipeline

def top_golf_labels():
    # Top 10 mentioned golf course labels
    match = {"$match":{"golf":{"$exists":1}}}
    group = {"$group":{"_id":"$golf", "count":{"$sum":1}}}
    sort = {"$sort":{"count":-1}}
    limit = {"$limit":10}
    pipeline = [match, group, sort, limit]
    return pipeline

def top_healthcare_facilities():
    # Top 10 types of healthcare facilities 
    match = {"$match":{"healthcare":{"$exists":1}}}
    group = {"$group":{"_id":"$healthcare", "count":{"$sum":1}}}
    sort = {"$sort":{"count":-1}}
    limit = {"$limit":10}
    pipeline = [match, group, sort, limit]
    return pipeline

def aggregate(db, pipeline):
    result = db.vegas.aggregate(pipeline)
    return result

def test(pipeline_function):
    db = get_db(db_name)
    pipeline = pipeline_function
    cursor = aggregate(db, pipeline)
    import pprint
    for document in cursor:
        pprint.pprint(document)
        

if __name__ == "__main__":
    print("Top 10 contributing users:\n")
    test(top_users())
    print("\nTop listed cities:\n")
    test(top_cities())
    print("\nTop 10 brands in the area:\n")
    test(top_amenities())
    print("\nTop 10 leisure facilities:\n")
    test(top_leisure_facilities())
    print("\nTop 10 golf course labels:\n")
    test(top_golf_labels())
    print("\nTop categories of healthcare facilities:\n")
    test(top_healthcare_facilities())


# ## Notes and thoughts on pipeline queries:
# 
# * Top listed cities presents an accurate and interesting finding.  While this area is mostly located outside the official city limits of Las Vegas and in the township of Spring Valley, almost all of the city labels reflect 'Las Vegas'.  This corresponds with official addresses in the area.
# 
# * Top listed brands represent an accurate finding based on personal knowledge of the area.
# 
# * Leisure facility labels seem to be accurate based on personal knowledge of the area.  Findings indicate there are plenty of outdoor options available to residents.
# 
# * Golf course labels are accurate and seem to represent the number of golf courses in the area.  
# 
# * Healthcare facility labels seem to be accurate.  However, my knowledge of the area raises a potential red flag, as there are many more dentists and optometrists in this neighborhood.

# In[10]:


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["vegas"]


# In[14]:


print("Total number of documents in source file: ", db.vegas.find().count())
print("Total number of node tags: ", db.vegas.find({'type':'node'}).count())
print("Total number of way tags: ", db.vegas.find({'type':'way'}).count())


# **Node count value corresponds with initial query of node label above.**

# **Way count value corresponds with initial query of way label above.**
