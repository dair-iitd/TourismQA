import scrapy
from hotel_sentiment.items import RestaurantSentimentItem
from hotel_sentiment.items import RestaurantItem

#TODO use loaders
class TripadvisorRestaurantsSpider(scrapy.Spider):
    name = "restaurants"
    start_urls = [
	#'https://www.tripadvisor.in/Restaurants-g60763-New_York_City_New_York.html',
	#'https://www.tripadvisor.in/Restaurants-g28970-Washington_DC_District_of_Columbia.html',
	#'https://www.tripadvisor.in/Restaurants-g35805-Chicago_Illinois.html',
	#'https://www.tripadvisor.in/Restaurants-g60713-San_Francisco_California.html',
	#'https://www.tripadvisor.in/Restaurants-g154943-Vancouver_British_Columbia.html',
	#'https://www.tripadvisor.in/Restaurants-g150800-Mexico_City_Central_Mexico_and_Gulf_Coast.html',
	#'https://www.tripadvisor.in/Restaurants-g34438-Miami_Florida.html',
	#'https://www.tripadvisor.in/Restaurants-g303631-Sao_Paulo_State_of_Sao_Paulo.html',
	#'https://www.tripadvisor.in/Restaurants-g312741-Buenos_Aires_Capital_Federal_District.html',
	#'https://www.tripadvisor.in/Restaurants-g303506-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html'
	#'https://www.tripadvisor.in/Restaurants-g45963-Las_Vegas_Nevada.html'	
	#'https://www.tripadvisor.in/Restaurants-g186338-London_England.html',
	#'https://www.tripadvisor.in/Restaurants-g187147-Paris_Ile_de_France.html',
	#'https://www.tripadvisor.in/Restaurants-g186605-Dublin_County_Dublin.html',
	#'https://www.tripadvisor.in/Restaurants-g187791-Rome_Lazio.html',
	#'https://www.tripadvisor.in/Restaurants-g189852-Stockholm.html',
	#'https://www.tripadvisor.in/Restaurants-g190479-Oslo_Eastern_Norway.html',
	#'https://www.tripadvisor.in/Restaurants-g188113-Zurich.html',
	#'https://www.tripadvisor.in/Restaurants-g190454-Vienna.html',
	#'https://www.tripadvisor.in/Restaurants-g187323-Berlin.html',
	#'https://www.tripadvisor.in/Restaurants-g274887-Budapest_Central_Hungary.html',
	#'https://www.tripadvisor.in/Restaurants-g294458-Bucharest.html',
	#'https://www.tripadvisor.in/Restaurants-g298484-Moscow_Central_Russia.html',
	#'https://www.tripadvisor.in/Restaurants-g188590-Amsterdam_North_Holland_Province.html'
	'https://www.tripadvisor.in/Restaurants-g294212-Beijing.html',
	'https://www.tripadvisor.in/Restaurants-g304551-New_Delhi_National_Capital_Territory_of_Delhi.html',
	'https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Bombay_Maharashtra.html',
	'https://www.tripadvisor.in/Restaurants-g297683-Agra_Agra_District_Uttar_Pradesh.html',
	'https://www.tripadvisor.in/Restaurants-g293916-Bangkok.html',
	'https://www.tripadvisor.in/Restaurants-g295414-Karachi_Sindh_Province.html',
	'https://www.tripadvisor.in/Restaurants-g294262-Singapore.html',
	'https://www.tripadvisor.in/Restaurants-g294229-Jakarta_Java.html',
	'https://www.tripadvisor.in/Restaurants-g298184-Tokyo_Tokyo_Prefecture_Kanto.html',
	'https://www.tripadvisor.in/Restaurants-g294197-Seoul.html',
	'https://www.tripadvisor.in/Restaurants-g303936-Bukhara_Bukhara_Province.html',
	'https://www.tripadvisor.in/Restaurants-g293956-Ulaanbaatar.html',
	'https://www.tripadvisor.in/Restaurants-g293890-Kathmandu_Kathmandu_Valley_Bagmati_Zone_Central_Region.html',
	'https://www.tripadvisor.in/Restaurants-g255100-Melbourne_Victoria.html',
	'https://www.tripadvisor.in/Restaurants-g255060-Sydney_New_South_Wales.html',
	'https://www.tripadvisor.in/Restaurants-g255106-Auckland_Central_North_Island.html',
	'https://www.tripadvisor.in/Restaurants-g147271-Havana_Ciudad_de_la_Habana_Province_Cuba.html',
	'https://www.tripadvisor.in/Restaurants-g60982-Honolulu_Oahu_Hawaii.html',
	'https://www.tripadvisor.in/Restaurants-g147310-Kingston_Kingston_Parish_Jamaica.html',
	'https://www.tripadvisor.in/Restaurants-g293738-Seychelles.html',
	'https://www.tripadvisor.in/Restaurants-g295424-Dubai_Emirate_of_Dubai.html',
	'https://www.tripadvisor.in/Restaurants-g294201-Cairo_Cairo_Governorate.html',
	'https://www.tripadvisor.in/Restaurants-g293986-Amman_Amman_Governorate.html',
	'https://www.tripadvisor.in/Restaurants-g293983-Jerusalem_Jerusalem_District.html',
	'https://www.tripadvisor.in/Restaurants-g312578-Johannesburg_Greater_Johannesburg_Gauteng.html',
	'https://www.tripadvisor.in/Restaurants-g1722390-Cape_Town_Western_Cape.html',
	'https://www.tripadvisor.in/Restaurants-g294207-Nairobi.html'
	]

    def parse(self, response):
        #print response.xpath('//div[starts-with(@class,"listing_title")]/a/@href').extract()
        #print response.xpath('//div[starts-with(@class,"listing rebrand")]/div/div/div[@class="title"]/a/@href')
        for href in response.xpath('//div[starts-with(@class,"listing rebrand")]/div/div/div[@class="title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_restaurant)
        next_page = response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]/@href')
        #next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/child::*[2][self::a]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_restaurant(self, response):
        item_attr=RestaurantItem()
        item_attr['name']= response.xpath('//div[@id="taplc_location_detail_header_restaurants_0"]/h1/text()').extract()
        item_attr['address']= response.xpath('(//span[@class="street-address"])[1]/text()').extract() + response.xpath('(//span[@class="extended-address"])[1]/text()').extract() + response.xpath('(//span[@class="locality"])[1]/text()').extract()# + 
        item_attr['type']=response.xpath('//span[@class="header_links rating_and_popularity"]/a/text()').extract()
        item_attr['description']=response.xpath('//div[@data-prwidget-name="common_location_description"]/div/div[@class="text"]/text()').extract()
        yield item_attr
		
        for href in response.xpath('//div[starts-with(@class,"quote")]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_review)
        #print response.xpath('//div[@id="REVIEWS"]/div/div[@data-prwidget-name="common_north_star_pagination"]/div/div[@class="pageNumbers"]/span/@data-href').extract()
        #print "DANISH",response.xpath('//div[@id="REVIEWS"]/div/div/div[@data-prwidget-name="common_north_star_pagination"]/div/div[@class="pageNumbers"]/span/@data-href').extract()
		#sys.exit()
        #next_page = response.xpath('//div[@class="unified pagination "]/child::*[2][self::a]/@href')
        #for href in response.xpath('//div[@id="REVIEWS"]/div/div[@data-prwidget-name="common_north_star_pagination"]/div/div[@class="pageNumbers"]/span/@data-href'):
        for href in response.xpath('//div[@id="REVIEWS"]/div/div/div[@data-prwidget-name="common_north_star_pagination"]/div/div[@class="pageNumbers"]/span/@data-href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, self.parse_restaurant)


    #to get the full review content I open its page, because I don't get the full content on the main page
    #there's probably a better way to do it, requires investigation
    def parse_review(self, response):
        item = RestaurantSentimentItem()
        item['json']=response.xpath('//script[@type="application/ld+json"]/text()').extract()
       
        item['name']= response.xpath('//span[@class="altHeadInline"]/a/text()').extract()
        item['address']= response.xpath('(//span[@class="street-address"])[1]/text()').extract() + response.xpath('(//span[@class="extended-address"])[1]/text()').extract() + response.xpath('(//span[@class="locality"])[1]/text()').extract()# + response.xpath('//span[@class="extended-address"]/text()').extract() + response.xpath('//span[@class="locality"]/text()').extract()
        #item['title'] = response.xpath('//div[@class="quote"]/text()').extract()[0][1:-1] #strip the quotes (first and last char)
        item['title'] = response.xpath('//span[@class="noQuotes"]/text()').extract() #strip the quotes (first and last char)
        item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract()[0]
        item['review_rating']=  response.xpath('//span[@property="reviewRating"]/span/@content').extract()
        item['review_date']=  response.xpath('//span[@class="ratingDate"]/@content').extract()
        #item['type']=response.xpath('//div[@class="rating_and_popularity"]/span/div[@class="listing_details"]/div[@class="detail"]/text()').extract()
        #item['description']=response.xpath('//div[@data-prwidget-name="common_location_description"]/div/div[@class="text"]/text()').extract()
        
        #item['stars'] = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()[0]
        return item
