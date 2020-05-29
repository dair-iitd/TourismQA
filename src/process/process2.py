import os
import json
from collections import defaultdict

from utils import common

@common.catcher(2)
def removeRepeatedEntityNames(post):
	entity_name_entity_ids = defaultdict(list)
	remove_entity_names = {"Atmosphere", "Current", "Delicious", "Departure", "District", "Dome", "Enjoy", "Factory", "Holiday", "Hotel L", "Husband",
						   "Mango", "Metro", "Morning", "Next Door", "Note", "Picnic", "Remember", "Restaurant", "Rice", "Sea", "September", "Spicy",
						   "Sunday", "Test", "The Beach", "The Restaurant", "The World", "UnderGround", "Very Nice", "paper", "restaurant"}
	for entity_id, entity_item in post["entities"].items():
		entity_name_entity_ids[entity_item["name"]].append(entity_id)
	for entity_name, entity_ids in entity_name_entity_ids.items():
		if(len(entity_ids) > 1 or (entity_name in remove_entity_names)):
			for entity_id in entity_ids:
				del post["entities"][entity_id]
	return post

def process(post, *args, **kwargs):
	post = removeRepeatedEntityNames(post = post)
	return post
