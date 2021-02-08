#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag in tags.keys():
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
            print(tags)
    return tags

def test():
    
    tags = count_tags('vegas')
    print("\nUnique tabs:\n")
    pprint.pprint(tags)

if __name__ == "__main__":
    test()


# **Used iterative parsing to process the source file and find how many unique tabs exist in the data:**
# 
# **Next, I explored lower level tags to identify name and count of each occurance.**

# In[2]:


import xml.etree.ElementTree as ET
from pprint import pprint
import operator

OSMFILE = 'vegas'

def count_tags(filename):
    element_count = {}
    k_attributes = {}

    for event, element in ET.iterparse(filename, events=("start",)):
        element_count[element.tag] = element_count.get(element.tag, 0) + 1

        if element.tag == 'tag' and 'k' in element.attrib:
            k_attributes[element.get("k")] = k_attributes.get(element.get("k"), 0) + 1

    # sort the dictionary by counts in decending order
    k_attributes = sorted(k_attributes.items(), key=operator.itemgetter(1))[::-1]
    element_count = sorted(element_count.items(), key=operator.itemgetter(1))[::-1]

    return element_count, k_attributes

def main():
    """ main function """
    element_count, k_attributes = count_tags(OSMFILE)
    print(element_count)
    print(k_attributes)
    return element_count, k_attributes

if __name__ == "__main__":
    main()


# **List of all of the different tags in the area and the number of occurances of each.  Will use to identify further areas of exploration.  Looking for tags with multiple instances in order to gain more in-depth understanding.**

# In[3]:


import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if lower.match(element.attrib['k']):
            keys["lower"] += 1
        elif lower_colon.search(element.attrib['k']):
            keys["lower_colon"] += 1
        elif problemchars.search(element.attrib['k']):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
        pass
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test2():
    
    keys = process_map('vegas')
    pprint.pprint(keys)

if __name__ == "__main__":
    test2()


# **Process to find tag types with problem characters.  There were none.**
