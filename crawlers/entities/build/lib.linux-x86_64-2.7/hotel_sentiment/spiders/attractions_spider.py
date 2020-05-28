import scrapy
from hotel_sentiment.items import AttractionSentimentItem
from hotel_sentiment.items import AttractionItem

#TODO use loaders
class TripadvisorAttractionsSpider(scrapy.Spider):
    name = "attractions"
    start_urls = [
	#'https://www.tripadvisor.com/Attractions-g186525-Activities-Edinburgh_Scotland.html'
	# 'https://www.tripadvisor.in/Attractions-g187289-Activities-Karlsruhe_Baden_Wurttemberg.html',
	# 'https://www.tripadvisor.com/Attractions-g155032-Activities-Montreal_Quebec.html',
	# 'https://www.tripadvisor.in/Attractions-g181736-Activities-Waterloo_Region_of_Waterloo_Ontario.html',
	#'https://www.tripadvisor.in/Attractions-g53449-Activities-Pittsburgh_Pennsylvania.html',
	# 'https://www.tripadvisor.in/Attractions-g49022-Activities-Charlotte_North_Carolina.html',
	# 'https://www.tripadvisor.in/Attractions-g3511549-Activities-Champaign_Urbana_Illinois.html',
	# 'https://www.tripadvisor.in/Attractions-g31310-Activities-Phoenix_Arizona.html',
	# 'https://www.tripadvisor.in/Attractions-g45963-Activities-Las_Vegas_Nevada.html',
	# 'https://www.tripadvisor.in/Attractions-g60859-Activities-Madison_Wisconsin.html',
	# 'https://www.tripadvisor.in/Attractions-g50207-Activities-Cleveland_Ohio.html'
	#'https://www.tripadvisor.in/Attractions-g190441-Activities-Salzburg_Austrian_Alps.html'
	#'https://www.tripadvisor.in/Attractions-g190441-Activities-Salzburg_Austrian_Alps.html'
	#'https://www.tripadvisor.in/Attractions-g297672-Activities-Udaipur_Udaipur_District_Rajasthan.html'
	#'https://www.tripadvisor.in/Attractions-g189934-Activities-Helsinki_Uusimaa.html'
	#'https://www.tripadvisor.in/Attractions-g304552-Activities-Shimla_Shimla_District_Himachal_Pradesh.html'
	#'https://www.tripadvisor.in/Attractions-g297683-Activities-Agra_Agra_District_Uttar_Pradesh.html'
	#'https://www.tripadvisor.in/Attractions-g297623-Activities-Srinagar_Srinagar_District_Kashmir_Jammu_and_Kashmir.html'
	#'https://www.tripadvisor.in/Attractions-g303884-Activities-Amritsar_Amritsar_District_Punjab.html'
	#'https://www.tripadvisor.in/Attractions-g274958-Activities-Tallinn_Harju_County.html',
	#'https://www.tripadvisor.in/Attractions-g297685-Activities-Varanasi_Varanasi_District_Uttar_Pradesh.html',
	#'https://www.tripadvisor.in/Attractions-g503702-Activities-Shillong_East_Khasi_Hills_District_Meghalaya.html',
	#'https://www.tripadvisor.in/Attractions-g188590-Activities-Amsterdam_North_Holland_Province.html'
	#'https://www.tripadvisor.in/Attractions-g60978-Activities-Newport_Rhode_Island.html'	
	#'https://www.tripadvisor.in/Attractions-g60763-Activities-New_York_City_New_York.html',
	#'https://www.tripadvisor.in/Attractions-g28970-Activities-Washington_DC_District_of_Columbia.html',
	#'https://www.tripadvisor.in/Attractions-g35805-Activities-Chicago_Illinois.html,'
	#'https://www.tripadvisor.in/Attractions-g60713-Activities-San_Francisco_California.html',
	#'https://www.tripadvisor.in/Attractions-g154943-Activities-Vancouver_British_Columbia.html',
	#'https://www.tripadvisor.in/Attractions-g150800-Activities-Mexico_City_Central_Mexico_and_Gulf_Coast.html',
	#'https://www.tripadvisor.in/Attractions-g34438-Activities-Miami_Florida.html',
	#'https://www.tripadvisor.in/Attractions-g303631-Activities-Sao_Paulo_State_of_Sao_Paulo.html',
	#'https://www.tripadvisor.in/Attractions-g303506-Activities-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html',
	#'https://www.tripadvisor.in/Attractions-g312741-Activities-Buenos_Aires_Capital_Federal_District.html'
	#'https://www.tripadvisor.in/Attractions-g186338-Activities-London_England.html',
	#'https://www.tripadvisor.in/Attractions-g186605-Activities-Dublin_County_Dublin.html',
	#'https://www.tripadvisor.in/Attractions-g187147-Activities-Paris_Ile_de_France.html',
	#'https://www.tripadvisor.in/Attractions-g187791-Activities-Rome_Lazio.html',
	#'https://www.tripadvisor.in/Attractions-g189852-Activities-Stockholm.html',
	#'https://www.tripadvisor.in/Attractions-g190479-Activities-Oslo_Eastern_Norway.html',
	#'https://www.tripadvisor.in/Attractions-g188113-Activities-Zurich.html',
	#'https://www.tripadvisor.in/Attractions-g190454-Activities-Vienna.html',
	#'https://www.tripadvisor.in/Attractions-g187323-Activities-Berlin.html',
	#'https://www.tripadvisor.in/Attractions-g274887-Activities-Budapest_Central_Hungary.html',
	#'https://www.tripadvisor.in/Attractions-g294458-Activities-Bucharest.html',
	#'https://www.tripadvisor.in/Attractions-g298484-Activities-Moscow_Central_Russia.html',
	#'https://www.tripadvisor.in/Attractions-g188590-Activities-Amsterdam_North_Holland_Province.html'
	#'https://www.tripadvisor.in/Attractions-g294212-Activities-Beijing.html',
	#'https://www.tripadvisor.in/Attractions-g304551-Activities-New_Delhi_National_Capital_Territory_of_Delhi.html',
	#'https://www.tripadvisor.in/Attractions-g304554-Activities-Mumbai_Bombay_Maharashtra.html',
	#'https://www.tripadvisor.in/Attractions-g297683-Activities-Agra_Agra_District_Uttar_Pradesh.html',
	#'https://www.tripadvisor.in/Attractions-g293916-Activities-Bangkok.html',
	#'https://www.tripadvisor.in/Attractions-g295414-Activities-Karachi_Sindh_Province.html',
	#'https://www.tripadvisor.in/Attractions-g294262-Activities-Singapore.html',
	#'https://www.tripadvisor.in/Attractions-g294229-Activities-Jakarta_Java.html',
	#'https://www.tripadvisor.in/Attractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html',
	#'https://www.tripadvisor.in/Attractions-g294197-Activities-Seoul.html',
	#'https://www.tripadvisor.in/Attractions-g303936-Activities-Bukhara_Bukhara_Province.html',
	#'https://www.tripadvisor.in/Attractions-g293956-Activities-Ulaanbaatar.html',
	#'https://www.tripadvisor.in/Attractions-g293890-Activities-Kathmandu_Kathmandu_Valley_Bagmati_Zone_Central_Region.html'
	'https://www.tripadvisor.in/Attractions-g255100-Activities-Melbourne_Victoria.html',
	'https://www.tripadvisor.in/Attractions-g255060-Activities-Sydney_New_South_Wales.html',
	'https://www.tripadvisor.in/Attractions-g255106-Activities-Auckland_Central_North_Island.html',
	'https://www.tripadvisor.in/Attractions-g147271-Activities-Havana_Ciudad_de_la_Habana_Province_Cuba.html',
	'https://www.tripadvisor.in/Attractions-g60982-Activities-Honolulu_Oahu_Hawaii.html',
	'https://www.tripadvisor.in/Attractions-g147310-Activities-Kingston_Kingston_Parish_Jamaica.html',
	'https://www.tripadvisor.in/Attractions-g293738-Activities-Seychelles.html',
	'https://www.tripadvisor.in/Attractions-g295424-Activities-Dubai_Emirate_of_Dubai.html',
	'https://www.tripadvisor.in/Attractions-g294201-Activities-Cairo_Cairo_Governorate.html',
	'https://www.tripadvisor.in/Attractions-g293986-Activities-Amman_Amman_Governorate.html',
	'https://www.tripadvisor.in/Attractions-g293983-Activities-Jerusalem_Jerusalem_District.html',
	'https://www.tripadvisor.in/Attractions-g312578-Activities-Johannesburg_Greater_Johannesburg_Gauteng.html'
	'https://www.tripadvisor.in/Attractions-g1722390-Activities-Cape_Town_Western_Cape.html',
	'https://www.tripadvisor.in/Attractions-g294207-Activities-Nairobi.html'
	]

    def parse(self, response):
        #print response.xpath('//div[starts-with(@class,"listing_title")]/a/@href').extract()
        for href in response.xpath('//div[starts-with(@class,"listing_title")]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_attraction)
        next_page = response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]/@href')
        #next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/child::*[2][self::a]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_attraction(self, response):
        item_attr=AttractionItem()
        item_attr['name']= response.xpath('//div[@id="taplc_location_detail_header_attractions_0"]/h1/text()').extract()
        item_attr['address']= response.xpath('(//span[@class="street-address"])[1]/text()').extract() + response.xpath('(//span[@class="extended-address"])[1]/text()').extract() + response.xpath('(//span[@class="locality"])[1]/text()').extract()# + 
        item_attr['type']=response.xpath('//span[@class="header_detail attraction_details"]/div[@class="detail"]/a/text()').extract()
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
            yield scrapy.Request(url, self.parse_attraction)


    #to get the full review content I open its page, because I don't get the full content on the main page
    #there's probably a better way to do it, requires investigation
    def parse_review(self, response):
        item = AttractionSentimentItem()
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
