import os
import re
import json
import pickle

from utils import common

def isLongPost(post, average_post_length):
	is_long_post = len(post["body"]) > 1.7 * average_post_length
	return is_long_post

# to repair
def getCityFromPost(post):
	if(post["location1"] == "EMEA_Asia"):
		city = post["location2"].lower()
	elif("../Americas_EU" in p["location1"]):
		city = post["location1"][(post["location1"].rindex("/") + 1):].lower()
		if(city == "buenous aires"):
			city = "buenos aires"
	else:
		city = p["location1"][12:].lower()
		if(city == ""):
			city = post["location2"].lower()
	if(city == "champaign_urbana_illinois"):
		city = "champaign"
	if(city == "washington dc"):
		city = "washington"
	if(city == "ulan bator"):
		city = "ulaanbaatar"
	return city

def removeGooglePlaces(post, places):
	city = getCityFromPost(post = post)
	stop_words = ["", ",", ":", "a", "&", "or", "is", "as", "and", "the"]

	for entity, entity_item in list(post["entities"].items()):
		entity_name = entity_item["name"].lower().replace(city, " ")
		filter = all([word in places for word in entity_name.split(" ") if word not in stop_words])
		if(filter):
			del post["entities"][entity]

	return post

@common.catcher(1)
def process(post, *args, **kwargs):
	places = kwargs["places"]
	average_post_length = kwargs["average_post_length"]

	is_long_post = isLongPost(post = post, average_post_length = average_post_length)
	if(is_long_post == True):
		raise Exception("Long post")

	post = removeGooglePlaces(post = post, places = places)
	return post
