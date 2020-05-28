import json
import nltk
from fuzzywuzzy import fuzz
from collections import defaultdict

def getCitySharedEntityNames(city_entity_data_map, cities):
	city_entity_names = defaultdict(set)
	num_cities = len(cities)

	for city_id in range(num_cities):
		if(str(city_id) in city_entity_data_map):
			entities = city_entity_data_map[str(city_id)]
			entity_names_types = defaultdict(lambda: [0, 0, 0])
			for entity in entities:
				entity_id = entity["id"]
				entity_name = entity["name"]
				if("_R_" in entity_id):
					entity_names_types[entity_name][0] = 1
				if("_H_" in entity_id):
					entity_names_types[entity_name][1] = 1
				if("_A_" in entity_id):
					entity_names_types[entity_name][2] = 1

			for entity_name, entity_types in entity_names_types.items():
				if(sum(entity_types) > 1):
					city_entity_names[city_id].add(entity_name)

	return city_entity_names

def removeBadEntities(post, remove_entity_names, bad_city_entity_names):
	post_title = post["title"].lower()
	for entity_id, entity_data in list(post["entities"].items()):
		city_id = int(entity_id.split("_")[0])
		if (entity_data["name"] in remove_entity_names) or (("where to eat" in post_title) and ("_R_" not in entity_id)) or (entity_data["name"].lower() in bad_city_entity_names[city_id]) or (entity_data["name"].lower() in post_title):
			del post["entities"][entity_id]
	return post["entities"]

def isBadQuestion(post):
	post_title = post["title"].lower()
	return (("vs" in post_title) or (" or "  in post_title) or ("your thoughts"  in post_title))

def checkNeighborhood(x, answer):
	neighborhood_words = ["opposite", "behind", "overlooking", "near", "across", "at", "from", "on", "to", "along"]
	value = (x + " road" in answer) or (x + "s" in answer) or ("in " + x in answer) or ("in the " + x in answer) or ("head up " + x in answer) or ("head up the " + x in answer) or ("not " + x in answer)
	for words in neighborhood_words:
		value = value or ((words + " " + x) in answer) or ((words + " the " + x) in answer) or ((x + " " + words) in answer)
	return value

def removeNeighborhoodEntities(post):
	entities_data = list(post["entities"].values())
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
			for entity in entities_data:
				if(fuzz.ratio(x, entity["name"]) > 95 and checkNeighborhood(x.lower(), answer["body"].lower())):
					entity["count"] -= 1

		for entity in entities_data:
			entity_name = " " + entity["name"].lower()
			if((len(entity_name) > 7) and (entity_name in answer["body"].lower()) and (checkNeighborhood(entity["name"].lower(), answer["body"].lower()))):
				entity["count"] -= 1

	for entity in entities_data:
		if(entity["count"] <= 0):
			del post["entities"][entity["key"]]

	return post["entities"]
