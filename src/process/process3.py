import json
import nltk
from fuzzywuzzy import fuzz
from collections import defaultdict

from utils import common

def isBadPost(post):
	post_title = post["title"].lower()
	return (("vs" in post_title) or (" or "  in post_title) or ("your thoughts"  in post_title))

def getTypeSharedEntityNames(cities, city_entities):
	type_shared_entity_names = set()

	for city_id in range(len(cities)):
		if(str(city_id) in city_entities):
			entities = city_entities[str(city_id)]
			entity_names_types = defaultdict(lambda: [0, 0, 0])
			for entity in entities:
				if("_R_" in entity["id"]):
					entity_names_types[entity["name"]][0] = 1
				if("_H_" in entity["id"]):
					entity_names_types[entity["name"]][1] = 1
				if("_A_" in entity["id"]):
					entity_names_types[entity["name"]][2] = 1

			for entity_name, entity_types in entity_names_types.items():
				if(sum(entity_types) > 1):
					type_shared_entity_names.add(entity_name)

	return type_shared_entity_names

def removeBadEntities(post, cities, city_entities):
	type_shared_entity_names = getTypeSharedEntityNames(cities, city_entities)

	for entity_id, entity_item in list(post["entities"].items()):
		if((("where to eat" in post["title"].lower()) and ("_R_" not in entity_id)) or (entity_item["name"].lower() in type_shared_entity_names) or (entity_item["name"].lower() in post["title"].lower())):
			del post["entities"][entity_id]

	return post

def checkNeighborhood(x, answer):
	neighborhood_words = ["opposite", "behind", "overlooking", "near", "across", "at", "from", "on", "to", "along"]
	value = (x + " road" in answer) or (x + "s" in answer) or ("in " + x in answer) or ("in the " + x in answer) or ("head up " + x in answer) or ("head up the " + x in answer) or ("not " + x in answer)
	for words in neighborhood_words:
		value = value or ((words + " " + x) in answer) or ((words + " the " + x) in answer) or ((x + " " + words) in answer)
	return value

def removeNeighborhoodEntities(post):
	entity_items = list(post["entities"].values())
	for answer in post["answers"]:
		if("Message from TripAdvisor staff" in answer["body"]):
			continue

		chunked = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(answer["body"])))
		for node in chunked:
			x = None
			if(type(node) == nltk.Tree):
				x = " ".join([i[0] for i in node.leaves()])
			elif(node[1].startswith("NN")):
				x = node[0]

			if(not x):
				continue

			for entity_item in entity_items:
				if(fuzz.ratio(x, entity_item["name"]) > 95 and checkNeighborhood(x.lower(), answer["body"].lower())):
					entity_item["count"] -= 1

		for entity_item in entity_items:
			entity_name = " " + entity_item["name"].lower()
			if((len(entity_name) > 7) and (entity_name in answer["body"].lower()) and (checkNeighborhood(entity_item["name"].lower(), answer["body"].lower()))):
				entity_item["count"] -= 1

	for entity_item in entity_items:
		if(entity_item["count"] <= 0):
			del post["entities"][entity_item["key"]]

	return post

@common.catcher(3)
def process(post, *args, **kwargs):
	cities = kwargs["cities"]
	city_entities = kwargs["city_entities"]

	is_bad_post = isBadPost(post = post)
	if(is_bad_post == True):
		raise Exception("Bad Post")

	post = removeBadEntities(post = post, cities = cities, city_entities = city_entities)
	post = removeNeighborhoodEntities(post = post)

	return post
