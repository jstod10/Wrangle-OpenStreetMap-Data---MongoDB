#!/usr/bin/env python
# coding: utf-8

# **Also wanted to find the values of k tags to further evaluate data and identify specific areas to explore in the data:**

# In[1]:


import xml.etree.ElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
lower_colon_vals = {}

def key_type(element, keys):
    if element.tag == "tag":
        kval = element.attrib['k']
        if re.search(lower, kval):
            keys['lower'] += 1
        elif re.search(lower_colon, kval):
            keys['lower_colon'] += 1
            colvals = kval.split(':')
            if colvals[0] not in lower_colon_vals.keys():
                lower_colon_vals[colvals[0]] = set()
            lower_colon_vals[colvals[0]].add(colvals[1])
        elif re.search(problemchars, kval):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
        
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

with open('vegas', 'rb') as mapfile:
    keys = process_map(mapfile)
    print("Types of k-values and their counts:\n")
    pprint.pprint(keys)
    print("\nTypes of colon-separated k-values:\n")
    pprint.pprint(lower_colon_vals)


# **Further audit of 'k' values in map data selection.  Upon review, there does not seem to be any invalid 'k' values.  All tags appear to be legitimate based on knowledge of area.**
# 
# **Will explore the following k tags to gain a better understanding of the selected map:
# * 'brand' tags - Which brands occur with the most frequency?
# * 'city' tags - What cities are represented as labels?
# * 'leisure' tags - What leisure facilities are available in the area?
# * 'golf' tags - What golf related labels exist in the map selection?  
# * 'healthcare' tags - What categories of healthcare facilities are located here?
