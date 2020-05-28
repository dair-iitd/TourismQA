remove_entity_names = ["Departure", "Sunday", "Atmosphere", "Next Door", "Very Nice", "Current", "Remember"]

def isBadQuestion(post):
	post_title = post["title"].lower()
	post_body = post["body"].lower()
	return ("route" in post_title) or ("transfer" in post_title) or ("how" in post_title) or ("itinerary" in post_title) or ("itinerary" in post_body) or ("review" in post_title)

def removeEntityNamesInBody(post):
	post_body = post["body"].lower()
	for entity_id, entity_data in list(post["entities"].items()):
		entity_name = entity_data["name"].lower()
		if(entity_name in post_body):
			del post["entities"][entity_id]
		if(entity_data["name"] in remove_entity_names):
			del post["entities"][entity_id]
	return post["entities"]
