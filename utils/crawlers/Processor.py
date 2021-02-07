import re
import string
import dateparser
from collections import OrderedDict

class Processor:
    def __init__(self):
        pass

    def processString(self, s):
        s = re.sub("\s+", " ", s)
        s = re.sub("\.+", ".", s)
        s = re.sub("\?+", "?", s)
        s = s.strip(string.punctuation + " ")
        return s

    def processReviewItem(self, item):
        ordered_item = OrderedDict()

        ordered_item["title"] = self.processString(item["title"])
        ordered_item["description"] = self.processString(item["description"])
        ordered_item["rating"] = float(item["rating"])
        ordered_item["date"] = dateparser.parse(item["date"].strip(), date_formats = ["%d %B %Y", "%B %d, %Y", "%Y-%m-%d"]).strftime("%d %B %Y")
        ordered_item["url"] = self.processString(item["url"])

        return ordered_item

    def processEntityItem(self, item):
        ordered_item = OrderedDict()

        ordered_item["id"] = self.processString(item["id"])
        ordered_item["name"] = self.processString(item["name"])
        ordered_item["properties"] = list(filter(lambda x: x != "", list(map(self.processString, item["properties"]))))
        ordered_item["description"] = self.processString(item["description"])
        ordered_item["address"] = self.processString(item["address"])
        ordered_item["latitude"] = float(item["latitude"])
        ordered_item["longitude"] = float(item["longitude"])
        ordered_item["rating"] = float(item["rating"])
        ordered_item["url"] = self.processString(item["url"])
        ordered_item["reviews"] = []
        for review in item["reviews"]:
            ordered_item["reviews"].append(self.processReviewItem(review))

        return ordered_item
