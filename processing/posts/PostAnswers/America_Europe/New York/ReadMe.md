# TourQue Data

> This repository supports a high-level web crawling and web scraping API framework to crawl entities and posts in a structured format from tourism based websites viz., TripAdvisor.com and Booking.com.

> It can be used for a range of purposes, from scraping restaurants, attractions & hotels for multiple cities to getting forum posts and generating datasets that can be used for NLP research purposes.

---

## Requirements

-   Python 3.4+
-   Linux-based system
---

## Installation

### Clone

> Clone this repository to your local machine.
```bash
git clone "https://github.com/danishContractor/TourQueData"
```

### Environment Setup

Please follow the instructions at the following link to set up anaconda. [https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)
> Set up the conda environment
```bash
$ conda env create -f environment.yml
```

> Install the required python packages

```bash
$ conda activate tourquedata
$ pip install -r requirements.txt
```
---

## Description

The code structure is divided into three separate steps viz., `crawling` the entity and post data from the web, `organizing` the entities data in a structured fashion and finally `processing` the posts data. The repository further supports building a Question-Answering dataset that can be used for NLP research purposes.

A sample post structure is shown below:
```json
{
	"posts": [
		{
			"city": "New York",
			"url": "http://www.tripadvisor.in//ShowTopic-g60763-i5-k12988893-Options_for_getting_into_the_city_from_NJ-New_York_City_New_York.html",
			"title": "Manhatten Hotels",
			"body": "Hello, I will be attending a conference in Lower Manhatten around 435 Hudson for 1 day, the next day we will be at 205 W. 39th St. I don't know my way around NY at all. I wanted to ask if anyone has a recommendation for a reasonably priced hotel in the area. It doesn't have to be fancy, just clean and with a fitness center. Thank you for any advice anyone may have."
			"timestamp": "17 Oct 2019, 11:09 PM",
			"answers": [
				{
					"title": "\\n7.\\n\\nRe: Manhatten Hotels \\n",
					"body": "We think that the best area for visitors to stay is in Greenwich Village....but hey, we've lived here for almost 50 years. That said, we like the Washington Square Hotel just across the street from Washington Square Park in the heart of Greenwich Village (and not far from your conference!)",
					"date": "18 Oct 2019, 6:26 AM"
				}
			]
		}
	]
}
```

A sample entity structure is shown below:

```json
[
	"hotels" : [
		{
			"name": "The Lalit New Delhi",
			"city": "New Delhi",
			"properties": [
				"Soundproof rooms",
				"Air conditioning",
				"Shops",
				"Butler service",
				"Doorperson",
				"24-hour front desk",
				"Dry cleaning",
				"Laundry service"
	        ],
			"description": "The LaLiT Hotels in Delhi, one of the best luxury hotels in Delhi India, stands tall right in the middle of city’s premier business and commercial district – Connaught Place. Being the central luxury business hotel in Delhi, it is located right next to lively shopping centres, office complexes and colourful streets, the hotel is 24 kms from the international airport and just minutes away from government offices, cultural centres and international trade fairgrounds. With the largest room sizes amongst all luxury hotels Delhi, The LaLiT New Delhi offers a total of 461 five star hotel rooms. The bedrooms are all well tailored to the needs of both a business traveler as well as a vacationer and accompanied by hotels modern amenities and elegant decor. Guests at our luxury hotels, have an option of choosing from a Deluxe Rooms, LaLiT Luxury Rooms and the suites.",
			"address": "Barakhamba Avenue Connaught Place, New Delhi 110001 India",
			"latitude": 28.631432,
			"longitude": 77.22716,
			"rating": 4.5,
			"url": "https://www.tripadvisor.in/Hotel_Review-g304551-d299120-Reviews-The_Lalit_New_Delhi-New_Delhi_National_Capital_Territory_of_Delhi.html",
			"reviews": [
				{
					"name": "Great Hotel",
					"description": "The facilities were great. I loved how there were speakers in the washroom. Staff were friendly. Room was spacious. The bed and pillows were comfy . All in all it was a great experience to stay in this hotel and I would definitely recommend others to stay here.",
					"rating": 5.0,
					"url": "https://www.tripadvisor.in/ShowUserReviews-g304551-d299120-r752534401-The_Lalit_New_Delhi-New_Delhi_National_Capital_Territory_of_Delhi.html"
				}
			]
		}
	]
]
```

## Functionality

### Entities

---

> CRAWLING

The following functions can be used to fetch the entities (restaurants/attractions/hotels). The code base currently supports four different spiders i.e. TripAdvisorAttractions, TripAdvisorHotels, TripAdvisorRestaurants and BookingHotels.

```python
getEntities(city = "Toronto", url = "https://www.tripadvisor.in/Attractions-g155019-Activities-a_allAttractions.true-Toronto_Ontario.html",
            spider = "TripAdvisorAttractions", output_dir_path = "./TorontoEntities", num_entities = 50, num_reviews = 100)
```

| Argument             | Type | Description                                     |
| ---                  | ---  | ---                                             |
| city                 | str  | name of the city                                |
| url                  | str  | url of the city entities home page              |
| spider               | str  | the spider to be used for crawlng the data      |
| output_dir_path      | str  | the output directory path to dump the data      |
| num_entities         | int  | number of entities to be fetched                |
| num_reviews          | int  | number of reviews to be fetched for each entity |

There is a provision for crawling data for multiple cities together.

---

> ORGANIZING

The following function can be used to organize the fetched data into a structured directory.

```python
organizeEntityData(file_paths = ["data/TripAdvisorAttractions.json", "data/BookingHotels.json"],
                   cities_file_path = "cities.json", output_dir_path = "TOURQUE_DATA")
```
| Argument             | Type | Description                                  |
| ---                  | ---  | ---                                          |
| file_paths           | str  | files crawled by the fetch API       	     |
| cities_file_path     | str  | file containing dict mapping from city to id |
| output_dir_path      | str  | the output directory path to dump the data   |

The cities_file_path is expected to contain the cities for which the data has been crawled. If a city is missing, the data from that city is ignored. Please find a sample `cities.json ` below:

```json
{
	"cities": {
		"New York": 0,
		"Chicago": 1,
		"New Delhi": 2,
		"London": 3
	}
}
```

---


### Posts

> CRAWLING

The following function can be used to fetch forum posts for a given city url. The code base currently supports links from TripAdvisor.com only. The code structure can be modified by developers to crawl data from other tourism forums.

```python
getPosts(city = "Chicago", url = "https://www.tripadvisor.in/ShowForum-g35805-i32-Chicago_Illinois.html",
		 output_dir_path = "./Posts" num_posts = 50, num_pinned_posts = 2, num_entries_per_page = 20, num_retries = 5)
```

| Argument             | Type | Description                                       |
| ---                  | ---  | ---                                               |
| city                 | str  | name of the city                                  |
| url                  | str  | url of the city tourism forum                     |
| output_dir_path      | str  | the output directory path to dump the data        |
| num_posts            | int  | number of posts to be fetched                     |
| num_pinned_posts     | int  | number of pinned posts on forum not to be fetched |
| num_entries_per_page | int  | number of post entries on a page                  |
| num_retries          | int  | number of retries for the web page crawler        |

> PROCESSING

The following function can be used to get the potential answers for a post and further eliminating those through a series of processing steps.

```python
processPosts(posts_folder_path = "PostData", processed_folder_path = "ProcessedPostData",
             cities_file_path = "cities.json", city_entity_data_map_path = "city_entity_data_map.json",
             places_file_path = "places.txt")

```

| Argument                    | Type | Description                                       |
| ---                         | ---  | ---                                               |
| posts_folder_path           | str  | raw posts foler path                              |
| processed_posts_folder_path | str  | processed posts folder path                       |
| cities_file_path            | str  | file containing dict mapping from city to id      |
| city_entity_data_map_path   | str  | city wise entities data in a json                 |

The cities file path should be the exactly same as the one supplied to generate the tourque data in the organization step of entities data.

The city_entity_data_map can be generated using the following function:

```python
generateCityEntityDataMap(entity_data_dir_path = "TOURQUE_DATA", city_entity_data_map_path = "city_entity_data_map.json")
```

The city_entity_data_map contains the data in the following format:

```json
{
	"7": [
		{
			"id": "7_H_3816",
			"name": "The Lalit New Delhi"
		}
	]
}
```

## TourQue QA Dataset

The following function can be used to generate the TourQue QA dataset:

```python
generateTourQueQADataSet(question_entity_map_path = "question_entity_tourqueQA.json",
                         entity_url_map_path = "entity_url_tourqueQA.json", output_dir_path = "TourQueQA")
```

| Argument                    | Type | Description                                       |
| ---                         | ---  | ---                                               |
| question_entity_map_path    | str  | Mapping from question urls to entity ids          |
| entity_url_map_path         | str  | Mapping from entity ids to urls                   |
| output_dir_path             | str  | the output directory to dump the train, dev and test data |

The question_entity_map and entity_url_map have been provided in the repository.

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2015 © <a href="[https://deepai.org/](https://deepai.org/)" target="_blank">DeepAI</a>.
