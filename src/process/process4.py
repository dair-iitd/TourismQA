from utils import common

def isBadPost(post):
	post_title = post["title"].lower()
	post_body = post["body"].lower()
	return ("route" in post_title) or ("transfer" in post_title) or ("how" in post_title) or ("itinerary" in post_title) or ("itinerary" in post_body) or ("review" in post_title)

def removeEntityNamesInBody(post):
	post_body = post["body"].lower()
	remove_entity_names = {"Atmosphere", "Current", "Departure", "Next Door", "Remember", "Sunday", "Very Nice"}
	for entity_id, entity_item in list(post["entities"].items()):
		entity_name = entity_item["name"].lower()
		if(entity_name in post_body):
			del post["entities"][entity_id]
		if(entity_item["name"] in remove_entity_names):
			del post["entities"][entity_id]
	return post

@common.catcher(4)
def process(post, *args, **kwargs):
	is_bad_post = isBadPost(post = post)
	if(is_bad_post == True):
		raise Exception("Bad Post")

	post = removeEntityNamesInBody(post = post)

	return post
