# https://arxiv.org/pdf/1909.03527.pdf
# Extracting entities for post

import nltk
from fuzzywuzzy import fuzz
from typing import Dict, List
from collections import defaultdict

class Processor:
	def __init__(self, cities: List[str], city_entities: Dict[str, Dict[str, dict]], neighborhood_words: List[str]) -> None:
		self.cities = cities
		self.city_entities = city_entities
		self.neighborhood_words = neighborhood_words

	def isNotNeighborhood(self, x, y):
		b1 = all("%s %s" % (x,z) not in y for z in ["road", "s"])
		b2 = all("%s %s" % (z,x) not in y for z in ["in the", "head up", "head up the", "not"])
		b3 = all(("%s %s" % (z, x) not in y) and ("%s the %s" % (z, x) not in y) and ("%s %s" % (x, z) not in y) for z in self.neighborhood_words)
		return b1 and b2 and b3

	def getEntitiesForPost(self, post: Dict[str, dict]) -> List[Dict[str, dict]]:
		entity_counts = defaultdict(int)

		city = self.cities.index(post["city"])
		entities = self.city_entities[str(city)]

		for answer in post["answers"]:
			try:
				chunk = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(answer["body"])))
				for node in chunk:
					x = ""
					if(type(node) == nltk.Tree):
						x = "".join([x[0] for x in node.leaves()])
					elif(node[1][:2] == "NN"):
						x = node[0]

					if(x == ""):
						continue

					for entity_id, entity_item in entities.items():
						if(fuzz.ratio(x, entity_item["name"]) > 95 and self.isNotNeighborhood(x.lower(), answer["body"].lower())):
							entity_counts[entity_id] += 1

				for entity_id, entity_item in entities.items():
					if((len(entity_item["name"]) > 6) and (" " + entity_item["name"].lower() in answer["body"].lower()) and self.isNotNeighborhood(x.lower(), answer["body"].lower())):
						entity_counts[entity_id] += 1
			except:
				pass

		post_entities = defaultdict(dict)
		for entity_id, count in entity_counts.items():
			post_entities[entity_id] = entities[entity_id]
			post_entities[entity_id]["count"] = count

		return post_entities

	def __call__(self, post: Dict[str, dict]) -> None:
		post_entities = self.getEntitiesForPost(post)
		post["entities"] = post_entities

		if(len(post["entities"]) == 0):
			raise Exception("No entities found")
