import os
import re
import sys
import json
import time
import pickle
import pyprind
import argparse

import postProcessEntities1
import postProcessEntities2
import postProcessEntities3
import postProcessEntities4

remove_entity_names = set(["September", "The Beach", "Delicious", "restaurant", "Holiday", "Restaurant", "The Restaurant", "Spicy", "Picnic", "Mango", "District", "Hotel L", "The World", "UnderGround", "Sea", "Rice", "Test", "Morning", "paper", "Metro", "Husband", "Factory", "Dome", "Note", "Enjoy", "Departure", "Sunday", "Atmosphere", "Next Door", "Very Nice", "Current", "Remember"])

def postProcessMerged(options):
	post_folder_path = options.post_folder_path
	processed_folder_path = options.processed_folder_path

	if(not os.path.exists(processed_folder_path)):
		os.mkdir(processed_folder_path)

	places = [x.split("_")[0] for x in open(options.places_file_path, "r").readlines()]
	cities = open(options.cities_file_path, "r").readlines()
	city_entity_data_map = pickle.load(open(options.city_entity_data_map_path, "rb"))

	posts_with_answers = 0
	total_question_answer_pairs = 0

	processed_posts_set = set()
	for file_name in os.listdir(post_folder_path):
		input_file = open(os.path.join(post_folder_path, file_name), "r")
		output_file = open(os.path.join(processed_folder_path, file_name), "a")

		posts = list(map(json.loads, re.split("(?<=\\})(?=\\{)", input_file.read())))

		bar = pyprind.ProgBar(len(posts), bar_char = "█", monitor = True, title = "Processing %d posts for %s" % (len(posts), file_name))
		for post in posts:
			if(post["link"] in processed_posts_set):
				bar.update()
				continue
			processed_posts_set.add(post["link"])

			if(postProcessEntities1.isLongQuestion(post, postProcessEntities1.getAverageQuestionLength(post_folder_path))):
				bar.update()
				continue
			post["entities"] = postProcessEntities1.removeGooglePlaces(post, places)
			if(not post["entities"]):
				bar.update()
				continue

			post["entities"] = postProcessEntities2.removeChainEntities(post, remove_entity_names)
			if(not post["entities"]):
				bar.update()
				continue

			if(postProcessEntities3.isBadQuestion(post)):
				bar.update()
				continue
			bad_city_entity_names = postProcessEntities3.getCitySharedEntityNames(city_entity_data_map, cities)
			post["entities"] = postProcessEntities3.removeBadEntities(post, remove_entity_names, bad_city_entity_names)
			post["entities"] = postProcessEntities3.removeNeighborhoodEntities(post)
			if(not post["entities"]):
				bar.update()
				continue

			if(postProcessEntities4.isBadQuestion(post)):
				bar.update()
				continue
			post["entities"] = postProcessEntities4.removeEntityNamesInBody(post)
			if(not post["entities"]):
				bar.update()
				continue

			posts_with_answers += 1
			total_question_answer_pairs += len(post["entities"])
			output_file.write(json.dumps(post, indent = 4))

			bar.update()

		print()

if(__name__ == "__main__"):
	parser = argparse.ArgumentParser(description = "Merged Processing Step")
	parser.add_argument("--post_folder_path", type = str, default = "../temp")
	parser.add_argument("--cities_file_path", type = str, default = "../data/cities.txt")
	parser.add_argument("--city_entity_data_map_path", type = str, default = "../data/city_entity_data_map.pkl")
	parser.add_argument("--places_file_path", type = str, default = "../data/places.txt")
	parser.add_argument("--processed_folder_path", type = str, default = "../output")
	options = parser.parse_args(sys.argv[1:])
	postProcessMerged(options)
