

# TourismQA

> This repository supports a high-level web crawling and web scraping API framework to crawl entities (Restaurant/Hotel/Attraction) and forum posts in a structured format from tourism based website viz., TripAdvisor.com. It can be used for a range of purposes, from scraping different entities for multiple cities to getting forum posts and generating datasets that can be used for NLP research purposes.

---

## Requirements

-   Python 3.4+
-   Linux-based system
---

## Installation

### Clone

> Clone this repository to your local machine.
```bash
git clone https://github.com/dair-iitd/TourismQA.git
```

### Environment Setup

Please follow the instructions at the following link to set up anaconda. [https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)
> Set up the conda environment
```bash
$ conda env create -f environment.yml
```

> Install the required python packages

```bash
$ conda activate tourismqa
$ pip install -r requirements.txt
```
---

## Description

The code base provides direct methods for generating the Tourque Dataset used [in this paper]([https://arxiv.org/abs/2009.13613](https://arxiv.org/abs/2009.13613)). The structure is divided into two separate components viz., `fetching` the entities and posts from Trip Advisor, and `processing` the fetched data to filter out noise and generating a high-precision Question-Answering Dataset.

A sample post structure is shown below:
```json
{
	"city": "New York",
	"url": "http://www.tripadvisor.in//ShowTopic-g60763-i5-k12988893-Options_for_getting_into_the_city_from_NJ-New_York_City_New_York.html",
	"title": "Manhatten Hotels",
	"body": "Hello, I will be attending a conference in Lower Manhatten around 435 Hudson for 1 day, the next day we will be at 205 W. 39th St. I don't know my way around NY at all. I wanted to ask if anyone has a recommendation for a reasonably priced hotel in the area. It doesn't have to be fancy, just clean and with a fitness center. Thank you for any advice anyone may have."
	"date": "17 Oct 2019, 11:09 PM",
	"answers": [
		{
			"title": "Manhatten Hotels",
			"body": "We think that the best area for visitors to stay is in Greenwich Village....but hey, we've lived here for almost 50 years. That said, we like the Washington Square Hotel just across the street from Washington Square Park in the heart of Greenwich Village (and not far from your conference!)",
			"date": "18 Oct 2019, 6:26 AM"
		}
	]
}
```

A sample entity structure is shown below:

```json
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
```

## TourQueQA Dataset

The following sections describe utilities that can be used to generate the `TourqueData`  posts and pre-extracted answer entities used by the author [in this paper]([https://arxiv.org/abs/2009.13613](https://arxiv.org/abs/2009.13613)).

### Entities
---

The support files in the "data/tourque/entities/help" directory can be used to generate the answer entities data. Each entity has a custom answer entity id used by the author.

The following utility is used to fetch the tourque answer entities:

```bash
python -m src.tourque.entities.getTourqueEntities --input_file_path "data/tourque/entities/help/entity_ids_to_entity_urls.json" --output_dir_path "data/tourque/entities/data"
```

The following utility can be used to generate a comprehensive city entities file (required in the next section) using the data generated above:
```bash
python -m utils.generateCityEntitiesFile --input_dir_path  "data/tourque/entities/data" --output_file_path "data/generate/city_entities.tourque.json"
```

### Posts
---

 The support files in the *data/tourque/posts/help* directory can be used for generating the train, validation and test posts data and in . The answer entity ids in the posts data are used as hashes by the author that map a particular post/question to the set of pre-extracted answer entities.

The following utility is used to fetch the tourque data posts (with answer responses):

```bash
python -m src.tourque.posts.getTourquePosts --input_file_path "data/tourque/posts/help/train_question_urls_to_answer_entity_ids.json" --output_file_path "data/tourque/posts/data/train_posts.json" --cities_file_path "data/common/cities.json"
```

#### Recommended:

The tourque data used in the paper follows a different format, combining the posts with their answer entities.    The following utility can be used to achieve this directly:

```bash
python -m src.tourque.posts.getTourqueData --input_file_path "data/tourque/posts/help/train_question_urls_to_answer_entity_ids_map.json" --output_file_path "data/tourque/posts/data/train.data.json" --city_entities_file_path "data/generated/city_entities.tourque.json"
```
Please note that this utility does not fetch the answer responses to the post and is considerably faster than the above.

## Custom Data   

### Fetching
---

#### Entities

`TO BE FIXED: BROKEN API`

#### Posts

The following utilities can be used to fetch tourism posts from TripAdvisor. The code is pipelined into two parts

i) Crawling posts' urls for a given list of city urls

```bash
python -m src.custom.fetch.posts.getPostsURLs --city_urls_file_path "data/common/city_urls.posts.json" --posts_urls_file_path "data/custom/posts/fetched/posts.urls.json" --sleep 0.05 --retries 5 --num_posts 100
```

ii) Crawling posts' data from the crawled posts' urls

```bash
python -m src.tourque.posts.getPosts --posts_urls_file_path "data/custom/posts/urls/posts.urls.json" --posts_file_path "data/posts/fetched/posts.fetched.json"
```

Please note that the answer entities are unknown for these posts and the answer entities extraction pipeline is discussed in the next section.


### Answer Extraction Pipeline
---

This section describes the answer entities extraction pipeline. The processing steps (described in the paper) are used to extract a high-precision Question-Answering Dataset.

#### Preliminary setup

The code base accesses files that cannot be put on the repository due to big sizes, licensing issues, etc. Please contact the repository collaborators to access these files .

- An entity tagger used in the  is required in the path /java.
- A word embeddings file is  required in the path /data/common/word_embeddings.pkl

Installing glpk

Install both the files in a directory and cd to that directory
http://ftp.gnu.org/gnu/glpk/glpk-4.65.tar.gz
http://ftp.gnu.org/gnu/glpk/glpk-4.65.tar.gz.sig

Please run the following commands in bash:

```bash
gpg --verify glpk-4.65.tar.gz.sig

# If above fails then run the next two commands
gpg --keyserver keys.gnupg.net --recv-keys 5981E818
gpg --verify glpk-4.65.tar.gz.sig

gzip -d glpk-4.65.tar.gz
cd glpk-4.65
./configure
make
sudo make
sudo apt-get update -y
sudo apt-get install -y libglpk-dev
pip install glpk
```



The following utility can be used to extract the answer entities for the fetched custom posts described in the previous section.

```bash
python -m src.custom.process.process --fetched_dir_path "data/posts/fetched" --processed_dir_path "data/posts/processed" --city_entities_file_path "data/generated/city_entities.custom.json"
python -m src.custom.process.postprocess --processed_dir_path "data/posts/processed" --postprocessed_dir_path "data/posts/postprocessed"
```

The process file uses other arguments with default values that can be changed as per requirements.

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)

- **[Apache 2.0 license](https://opensource.org/licenses/Apache-2.0)**
