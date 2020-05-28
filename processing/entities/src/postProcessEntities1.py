import os
import re
import json
import pickle

# POST PROCESS : MAJORITY CATEGORY OF ENTITIES, LONG QUESTIONS (1.7), GOOGLE PLACES API

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

def getAverageQuestionLength(post_folder_path):
	count = 0
	length = 0
	for file_name in os.listdir(post_folder_path):
		infile = open(os.path.join(post_folder_path, file_name), "r")
		posts = list(map(json.loads, re.split("(?<=\\})(?=\\{)", infile.read())))
		count += len(posts)
		length += sum(len(post["body"]) for post in posts)

	average_question_length = float(length)/count
	return average_question_length

def removeGooglePlaces(post, places):
	entities = post["entities"]
	filtered_entities = {}

	city = getCityFromPost(post)
	stop_words = ["", ",", ":", "a", "&", "or", "is", "as", "and", "the"]

	for entity in entities:
		entity_json = entities[entity]
		entity_name_words = entity_json["name"].lower().replace(city, " ").split(" ")
		dont_filter = any([word not in places and word not in places for word in entity_name_words])
		if(dont_filter):
			filtered_entities[entity] = entity_json
	return filtered_entities

def isLongQuestion(post, average_question_length):
	return (len(post["body"]) > 1.7 * average_question_length)
