#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

osm_file = open("West Vegas Valley.osm", "rb", buffering=0)

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Circle", "Road", "Lane", "Road", "Trail", "Parkway", "Commons"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s:s.lower())
    for k in keys:
        v = d[k]
        print("%s: %d" % (k, v))
        
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    print("\n")
    pprint.pprint(dict(street_types))
    
if __name__ == '__main__':
    audit()
                    


# ## Notes on audited street names (unexpected street types):
# 
# * '1' and '705' - Valid apartment/suite numbers.  No changes needed.
# * 'Ave' and 'Ave.' - Abbreviations of Avenue.  Will update in subsequent code.
# * 'Blv' , 'Blvd.', and 'Blvd' - Abbreviations of Boulevard.  Will update in subsequent code. 
# * 'Buckskin' - Valid street name.  Google search reveals not missing street label.  Will add to 'expected' list. 
# * 'Dr,' - Abbreviation of Drive with an added character (,).  Will update in subsequent code.
# * 'Rd' - Abbreviation of Road.  Will update in subsequent code.
# * 'Robindale' - Valid street name.  Will add to 'expected' list in subsequent code.
# * 'S' - Valid abbreviation of directional.  Will update to full word in subsequent code.
# * 'St' - Valid abbreviation of Street.  Will update in subsequent code.
# * 'Way' - Valid street name.  Will add to 'expected' list in subsequent code.
# * 'drive' - Valid lowercase version of Drive.  Not sure why the IGNORECASE code did not catch it so will update in subsequent code. 
# 
# **Conclusions:  Overall pretty pleased with the low number of 'problem' street name abnormalities, especially considering the size of the source data set.** 

# In[2]:


import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

OSMFILE = "vegas"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Circle", "Road", "Lane", "Road", "Trail", "Parkway", "Commons",
                          "Buckskin", "Robindale", "Way"]

# Updated dictionary 'mapping' reflects changes needed in SW Vegas file
mapping = { "E": "East", "E.": "East", "W.":"West", "W": "West", "N.": "North", "N": "North", "S": "South", "Rd": "Road",
            "Rd.": "Road", "ln": "Lane", "ln.": "Lane", "Ln": "Lane", "Ln.": "Lane", "Ct": "Court", "dr": "Drive",
            "dr.": "Drive", "Dr": "Drive", "Dr.": "Drive", "drive" : "Drive", "st": "Street", "St": "Street", "St.": "Street", "Ste": "Suite",
            "Ste.": "Suite", "Trl": "Trail", "Cir": "Circle", "cir": "Circle", "Av": "Avenue", "Ave": "Avenue",
            "Ave.": "Avenue", "Pky": "Parkway", "Pky.": "Parkway",
            "Pkwy": "Parkway", "pkwy": "Parkway", "Fwy": "Freeway", "Fwy.": "Freeway", "BLVD": "Boulevard", "Blvd": "Boulevard",
            "Blvd.": "Boulevard", "Blv" : "Boulevard"
            }


def audit_street_type(street_types, street_name):
   
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if street_type.isdigit():
                try:
                    true_street_type = street_name.split()[-2]
                    if true_street_type not in expected:
                        street_types[true_street_type].add(street_name)
                except IndexError:
                    pass
            else:
                street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    Redoing audit to make sure expected changes and updates have taken place.
    """
    osm_file = open(osmfile, "rb")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update(name, mapping):
  
    words = name.split()
    for w in range(len(words)):
        if words[w] in mapping:
            words[w] = mapping[words[w]]
    name = " ".join(words)
    return name


def example_test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update(name, mapping)
            print(name, "=>", better_name)
            if name == "S Fort Apache Rd":
                assert better_name == "South Fort Apache Road"
            if name == "S Edmond St":
                assert better_name == "South Edmond Street"


if __name__ == '__main__':
    example_test()

