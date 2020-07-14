# https://arxiv.org/pdf/1909.03527.pdf
# Remove Attractions/Hotels in a Restaurant Post
# Remove Type Shared Entity Names
# Remove Category Places
# Remove Entity Names in Question
# Remove Repeated Entity Names

import nltk
import itertools
from fuzzywuzzy import fuzz
from typing import Dict, List

class Processor:
	def __init__(self, common_names: List[str], city_entities: Dict[str, Dict[str, dict]], places: List[str], stop_words: List[str]) -> None:
		self.common_names = common_names
		self.places = places
		self.stop_words = stop_words
		self.type_shared_entity_names = self.getTypeSharedEntityNames(city_entities)

	def getTypeSharedEntityNames(self, city_entities: Dict[str, Dict[str, dict]]) -> List[str]:
		type_shared_entity_names = set()
		for city, entities in city_entities.items():
			entity_data = [(entity_item["name"], entity_id.split("_")[1]) for entity_id, entity_item in entities.items()]
			for key, group in itertools.groupby(sorted(entity_data), lambda t: t[0]):
				types = {entity_type for entity_name, entity_type in list(group)}
				if(len(types) > 1):
					type_shared_entity_names.add(key.lower())
		return type_shared_entity_names

	def removeSelectedEntitiesInRestaurantPost(self, post: Dict[str, dict]) -> None:
		for entity_id, entity_item in list(post["entities"].items()):
			if(("where to eat" in post["title"].lower()) and ("_R_" not in entity_id)):
				del post["entities"][entity_id]

	def removeCategoryPlaces(self, post: Dict[str, dict]) -> None:
		for entity_id, entity_item in list(post["entities"].items()):
			entity_name = entity_item["name"].lower().replace(post["city"].lower(), " ").strip()
			if(all([word in self.places for word in entity_name.split(" ") if word not in self.stop_words])):
				del post["entities"][entity_id]

	def removeEntityNamesInPost(self, post: Dict[str, dict]) -> None:
		for entity_id, entity_item in list(post["entities"].items()):
			if(entity_item["name"].lower() in post["question"].lower() or entity_item["name"].lower() in post["title"].lower()):
				del post["entities"][entity_id]

	def removeRepeatedEntityNames(self, post: Dict[str, dict]) -> None:
		entity_data = [(entity_item["name"], entity_id) for entity_id, entity_item in post["entities"].items()]
		for key, group in itertools.groupby(sorted(entity_data), lambda t: t[0]):
			if(len(list(group)) > 1):
				for entity_name, entity_id in list(group):
					del post["entities"][entity_id]

	def removeTypeSharedEntityNames(self, post: Dict[str, dict]) -> None:
		for entity_id, entity_item in list(post["entities"].items()):
			if(entity_item["name"].lower() in self.type_shared_entity_names):
				del post["entities"][entity_id]

	def __call__(self, post: Dict[str, dict]) -> None:
		self.removeSelectedEntitiesInRestaurantPost(post)
		if(len(post["entities"]) == 0):
			raise Exception("Removed Selected Entities in Restaurant Post. No entities left.")

		self.removeCategoryPlaces(post)
		if(len(post["entities"]) == 0):
			raise Exception("Removed Category Places. No entities left.")

		self.removeEntityNamesInPost(post)
		if(len(post["entities"]) == 0):
			raise Exception("Removed Entity Names in Post. No entities left.")

		self.removeRepeatedEntityNames(post)
		if(len(post["entities"]) == 0):
			raise Exception("Removed Repeated Entity Names. No entities left.")

		self.removeTypeSharedEntityNames(post)
		if(len(post["entities"]) == 0):
			raise Exception("Removed Type Shared Entity Names. No entities left.")
