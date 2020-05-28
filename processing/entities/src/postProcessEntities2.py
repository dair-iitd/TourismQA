import os
import json

# POST PROCESS : ENTITIES WITH CLASHING NAMES, SOME BLACKLISTED ENTITIES

def removeEntity(post, entity_id):
	del post["entities"][entity_id]

def removeChainEntities(post, remove_entity_names):
	entity_name_count = {}
	for entity in post["entities"]:
		entity_name = post["entities"][entity]["name"]
		if(entity_name in entity_name_count):
			entity_name_count[entity_name].append(entity)
		else:
			entity_name_count[entity_name] = [entity]
	for entity_name in entity_name_count:
		if(len(entity_name_count[entity_name]) > 1 or (entity_name in remove_entity_names)):
			map(lambda x: removeEntity(post, x), entity_name_count[entity_name])
	return post["entities"]
