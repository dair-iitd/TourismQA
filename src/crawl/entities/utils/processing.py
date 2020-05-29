import re
import string
from collections import OrderedDict

def processString(s):
    s = re.sub("\s+", " ", s)
    s = re.sub("\.+", ".", s)
    s = re.sub("\?+", "?", s)
    s = s.strip(string.punctuation + " ")
    return s

def processReviewItem(item):
    ordered_item = OrderedDict()

    ordered_item["name"] = processString(item["name"])
    ordered_item["description"] = processString(item["description"])
    ordered_item["rating"] = float(item["rating"])
    ordered_item["url"] = processString(item["url"])

    return ordered_item

def processEntityItem(item):
    ordered_item = OrderedDict()

    ordered_item["name"] = processString(item["name"])
    ordered_item["properties"] = list(filter(lambda x: x != "", list(map(processString, item["properties"]))))
    ordered_item["description"] = processString(item["description"])
    ordered_item["address"] = processString(item["address"])
    ordered_item["latitude"] = float(item["latitude"])
    ordered_item["longitude"] = float(item["longitude"])
    ordered_item["rating"] = float(item["rating"])
    ordered_item["url"] = processString(item["url"])
    ordered_item["reviews"] = []
    for review in item["reviews"]:
        ordered_item["reviews"].append(processReviewItem(review))

    return ordered_item
