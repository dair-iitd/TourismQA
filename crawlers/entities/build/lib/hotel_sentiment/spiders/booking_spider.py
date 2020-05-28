import json
import codecs
import scrapy
import os
from scrapy.loader import ItemLoader
from hotel_sentiment.items import BookingReviewItem
from hotel_sentiment.items import BookingHotelItem
import pdb
#crawl up to 6 pages of review per hotel
max_pages_per_hotel = 5

class BookingSpider(scrapy.Spider):
    name = "booking"
    def read_urls_from_file(self,filename):
        cwd = os.getcwd()
        print cwd
        file=codecs.open(cwd+"/"+filename,'r',encoding='utf8')
        #cities=codecs.open("cities.3.txt",'r',encoding='utf8')
        start_url_list=[]
        URL_COUNTS=100
        ctr=0;
        for entry in file:
            json_obj=json.loads(entry)
            if json_obj['url'] is not None:
                start_url_list.append(str(json_obj['url']))
                print json_obj['city']
                ctr+=1
            if ctr>URL_COUNTS:
                 return start_url_list
        return start_url_list
	
	
	
	#start_urls = 
    #start_urls = [
    # "#https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYAS64AQbIAQ_YAQPoAQGSAgF5qAID&lang=en-gb&sid=72ae66c523c133d421a0e0513da66b2d&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYAS64AQbIAQ_YAQPoAQGSAgF5qAID%3Bsid%3D72ae66c523c133d421a0e0513da66b2d%3Bsb_price_type%3Dtotal%26%3B&ss=Alwar%2C+Delhi+NCR%2C+India&ssne=New+Delhi&ssne_untouched=New+Delhi&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&genius_rate=1&ss_raw=Alwar&ac_position=0&ac_langcode=en&dest_id=-2088558&dest_type=city&search_pageview_id=9e8839fbb6f00129&search_selected=true&search_pageview_id=9e8839fbb6f00129&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"

    #]

    pageNumber = 1
    
    def __init__(self):
     #start_url=self.read_urls_from_file("cities.urls.txt")
     #   start_url = self.read_from_file(url_filename)
     #start_url = ['https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQHoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=1593&dest_type=district&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&map=1&no_rooms=1&offset=0&postcard=0&raw_dest_type=district&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Melbourne%20CBD%2C%20%E2%80%8BMelbourne%2C%20%E2%80%8BVictoria%2C%20%E2%80%8BAustralia&ss_all=0&ss_raw=Melbourne&ssb=empty&sshis=0&#map_closed','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-1603135&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Sydney%2C%20%E2%80%8BNew%20South%20Wales%2C%20%E2%80%8BAustralia&ss_all=0&ss_raw=Syd&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-1506909&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Auckland%2C%20%E2%80%8BAuckland%20Region%2C%20%E2%80%8BNew%20Zealand&ss_all=0&ss_raw=Auckland&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-1628751&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Havana%2C%20%E2%80%8BCaribbean%20Islands%2C%20%E2%80%8BCuba&ss_all=0&ss_raw=Havana&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=20030916&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Honolulu%2C%20%E2%80%8BHawaii%2C%20%E2%80%8BUSA&ss_all=0&ss_raw=Honolulu&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-3752438&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Kingston%2C%20%E2%80%8BCaribbean%20Islands%2C%20%E2%80%8BJamaica&ss_all=0&ss_raw=Kingston&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=188&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Seychelles&ss_all=0&ss_raw=Seychelles&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-782831&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Dubai%2C%20%E2%80%8BDubai%20Emirate%2C%20%E2%80%8BUnited%20Arab%20Emirates&ss_all=0&ss_raw=Dubai&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-290692&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Cairo%2C%20%E2%80%8BCairo%20Governate%2C%20%E2%80%8BEgypt&ss_all=0&ss_raw=Cairo&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-970362&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Amman%2C%20%E2%80%8BAmman%20Governorate%2C%20%E2%80%8BJordan&ss_all=0&ss_raw=Amman&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=900000000&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Jerusalem%2C%20%E2%80%8BJerusalem%20District%2C%20%E2%80%8BIsrael&ss_all=0&ss_raw=Jerusalem&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-1240261&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Johannesburg%2C%20%E2%80%8BGauteng%2C%20%E2%80%8BSouth%20Africa&ss_all=0&ss_raw=Johannesburg&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-1217214&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Cape%20Town%2C%20%E2%80%8BWestern%20Cape%2C%20%E2%80%8BSouth%20Africa&ss_all=0&ss_raw=Cape%20Town&ssb=empty&sshis=0&','https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQbIAQ_YAQPoAQH4AQKSAgF5qAID;sid=74e37a1cb1abf8e7edfd39b746f7e76e;class_interval=1&dest_id=-2258072&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Nairobi%2C%20%E2%80%8BNairobi%2C%20%E2%80%8BKenya&ss_all=0&ss_raw=Nairobi&ssb=empty&sshis=0&']
     start_url=['https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw;sid=8c6adec29ebabbc12fb44d6a26ec70f8;class_interval=1&dest_id=20033173&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Chicago%2C%20Illinois%2C%20USA&ss_all=0&ss_raw=Chic&ssb=empty&sshis=0&',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bclass_interval%3D1%3Bdest_id%3D20033173%3Bdest_type%3Dcity%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dindex%3Bsrc_elem%3Dsb%3Bss%3DChicago%252C%2520Illinois%252C%2520USA%3Bss_raw%3DChic%3Bssb%3Dempty%26%3B&ss=San+Francisco%2C+California%2C+USA&ssne=Chicago&ssne_untouched=Chicago&city=20033173&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=San+Fran&ac_position=0&ac_langcode=en&dest_id=20015732&dest_type=city&place_id_lat=37.787804&place_id_lon=-122.407503&search_pageview_id=d8cd3436215f0177&search_selected=true&search_pageview_id=d8cd3436215f0177&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D20033173%3Bclass_interval%3D1%3Bdest_id%3D20015732%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DSan%2520Francisco%252C%2520California%252C%2520USA%3Bss_all%3D0%3Bss_raw%3DSan%2520Fran%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DChicago%26%3B&ss=Mexico+City%2C+Mexico+DF%2C+Mexico&ssne=San+Francisco&ssne_untouched=San+Francisco&city=20015732&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Mexico&ac_position=0&ac_langcode=en&dest_id=-1658079&dest_type=city&place_id_lat=19.432863&place_id_lon=-99.133301&search_pageview_id=440f3464f39e0087&search_selected=true&search_pageview_id=440f3464f39e0087&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D20015732%3Bclass_interval%3D1%3Bdest_id%3D-1658079%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DMexico%2520City%252C%2520Mexico%2520DF%252C%2520Mexico%3Bss_all%3D0%3Bss_raw%3DMexico%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DSan%2520Francisco%26%3B&ss=Washington%2C+District+of+Columbia%2C+USA&ssne=Mexico+City&ssne_untouched=Mexico+City&city=-1658079&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Was&ac_position=0&ac_langcode=en&dest_id=20021296&dest_type=city&place_id_lat=38.901343&place_id_lon=-77.03654&search_pageview_id=440f3470ec6700cb&search_selected=true&search_pageview_id=440f3470ec6700cb&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D-1658079%3Bclass_interval%3D1%3Bdest_id%3D20021296%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DWashington%252C%2520District%2520of%2520Columbia%252C%2520USA%3Bss_all%3D0%3Bss_raw%3DWas%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DMexico%2520City%26%3B&ss=Vancouver%2C+British+Columbia%2C+Canada&ssne=Washington%2C+DC&ssne_untouched=Washington%2C+DC&city=20021296&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Van&ac_position=0&ac_langcode=en&dest_id=-575268&dest_type=city&place_id_lat=49.282412&place_id_lon=-123.121193&search_pageview_id=399b3478ea1b0152&search_selected=true&search_pageview_id=399b3478ea1b0152&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D20021296%3Bclass_interval%3D1%3Bdest_id%3D-575268%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DVancouver%252C%2520British%2520Columbia%252C%2520Canada%3Bss_all%3D0%3Bss_raw%3DVan%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DWashington%252C%2520DC%26%3B&ss=Miami%2C+Florida%2C+USA&ssne=Vancouver&ssne_untouched=Vancouver&city=-575268&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Miami&ac_position=1&ac_langcode=en&dest_id=20023181&dest_type=city&place_id_lat=25.772224&place_id_lon=-80.192581&search_pageview_id=03ce34864f9900b1&search_selected=true&search_pageview_id=03ce34864f9900b1&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D-575268%3Bclass_interval%3D1%3Bdest_id%3D20023181%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DMiami%252C%2520Florida%252C%2520USA%3Bss_all%3D0%3Bss_raw%3DMiami%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DVancouver%26%3B&ss=Buenos+Aires%2C+Argentina&ssne=Miami&ssne_untouched=Miami&city=20023181&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Bueno&ac_position=0&ac_langcode=en&dest_id=-979186&dest_type=city&place_id_lat=-34.603752&place_id_lon=-58.381561&search_pageview_id=30023497672400f0&search_selected=true&search_pageview_id=30023497672400f0&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D20023181%3Bclass_interval%3D1%3Bdest_id%3D-979186%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DBuenos%2520Aires%252C%2520Argentina%3Bss_all%3D0%3Bss_raw%3DBueno%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DMiami%26%3B&ss=Rome%2C+Lazio%2C+Italy&ssne=Buenos+Aires&ssne_untouched=Buenos+Aires&city=-979186&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Rome&ac_position=0&ac_langcode=en&dest_id=-126693&dest_type=city&place_id_lat=41.89587&place_id_lon=12.482617&search_pageview_id=67c434b8e4500007&search_selected=true&search_pageview_id=67c434b8e4500007&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw&sid=8c6adec29ebabbc12fb44d6a26ec70f8&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhsiAEBmAExuAEGyAEP2AEB6AEB-AECkgIBeagCAw%3Bsid%3D8c6adec29ebabbc12fb44d6a26ec70f8%3Bcity%3D-979186%3Bclass_interval%3D1%3Bdest_id%3D-126693%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DRome%252C%2520Lazio%252C%2520Italy%3Bss_all%3D0%3Bss_raw%3DRome%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DBuenos%2520Aires%26%3B&ss=Rio+de+Janeiro%2C+Rio+de+Janeiro+State%2C+Brazil&ssne=Rome&ssne_untouched=Rome&city=-126693&checkin_month=&checkin_monthday=&checkin_year=&checkout_month=&checkout_monthday=&checkout_year=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Rio&ac_position=0&ac_langcode=en&dest_id=-666610&dest_type=city&place_id_lat=-22.901271&place_id_lon=-43.179032&search_pageview_id=67c434c5cf9a006d&search_selected=true&search_pageview_id=67c434c5cf9a006d&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0']

     super(BookingSpider, self).__init__(start_urls=start_url)
        #super(BookingSpider, self).__init__(name=None,start_urls=["https://www.booking.com/searchresults.en-gb.html?aid=357026&label=gog235jc-city-XX-us-newNyork-unspec-uy-com-L%3Axu-O%3AosSx-B%3Achrome-N%3Ayes-S%3Abo-U%3Ac&lang=en-gb&sid=1eb6a8c3f421b9254d30c91d45d2c3fc&sb=1&src=country&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fcountry%2Fus.en-gb.html%3Faid%3D357026%3Blabel%3Dgog235jc-city-XX-us-newNyork-unspec-uy-com-L%253Axu-O%253AosSx-B%253Achrome-N%253Ayes-S%253Abo-U%253Ac%3Bsid%3D1eb6a8c3f421b9254d30c91d45d2c3fc%3Binac%3D0%26%3B&ss=London%2C+Greater+London%2C+United+Kingdom&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&genius_rate=1&ss_raw=London&ac_position=0&ac_langcode=xu&dest_id=-2601889&dest_type=city&search_pageview_id=2ec7965b7c6c0498&search_selected=true&search_pageview_id=2ec7965b7c6c0498&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"])
    
	
	
    
    #for every hotel
    def parse(self, response):
        for hotelurl in response.xpath('//a[@class="hotel_name_link url"]/@href'):
            #hotel_name_path=response.xpath('//a[@class="hotel_name_link url"]//span[@class="sr-hotel__name"]/text()')
            #hotel_name= hotel_name_path[0].extract()
            #print hotel_name
            url = response.urljoin(hotelurl.extract().strip())
            print url
            #hahahahhahah
        
            #yield scrapy.Request(url, callback=self.parse_hotel)
            yield scrapy.Request(url, callback=self.parse_hotel)
        #pdb.set_trace()
        next_page = response.xpath('//a[starts-with(@class,"paging-next")]/@href')
        #print type(next_page)
        if next_page is not None and next_page != '':
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    #get its reviews page
    def parse_hotel(self, response):
        hotel_obj = BookingHotelItem()
        hotel_name=response.xpath('//a[starts-with(@id,"hp_hotel_name_reviews")]/text()').extract()
        hotel_address=response.xpath('//span[starts-with(@class,"hp_address_subtitle")]/text()').extract()
        hotel_address_1=response.xpath('//span[contains(@class,"hp_address_subtitle")]/text()').extract()
        hotel_description=response.xpath('//div[starts-with(@class,"hp_desc_main_content")]/p/text()').extract()
        hotel_description_1=response.xpath('//div[starts-with(@class,"hp_desc_main_content")]/div[@id="summary"]/p/text()').extract()
        hotel_facilities=response.xpath('//div[@class="facilitiesChecklistSection"]/ul/li/span/text()').extract()
        hotel_obj['hotel_name']=hotel_name
        hotel_obj['hotel_address']=hotel_address
        hotel_obj['hotel_address_1']=hotel_address_1
		#if hotel_description:
        hotel_obj['hotel_description']=hotel_description
		#if hotel_description_1:
        hotel_obj['hotel_description_1']=hotel_description_1
        hotel_obj['hotel_facilities']=hotel_facilities
        yield hotel_obj
        #pdb.set_trace()
        reviewsurl = response.xpath('//a[@class="show_all_reviews_btn"]/@href')
        url = response.urljoin(reviewsurl[0].extract().strip())
        self.pageNumber = 1
        yield scrapy.Request(url, callback=self.parse_reviews)

    #and parse the reviews
    def parse_reviews(self, response):
        if self.pageNumber > max_pages_per_hotel:
            return
        hotel_name=response.xpath('//a[@class="standalone_header_hotel_link"]/text()')[0].extract()
        address = response.xpath('//p[@class="hotel_address"]/text()')[0].extract()
        hotel_class=response.xpath('//span[@class="invisible_spoken"]/text()')[0].extract()
        for rev in response.xpath('//li[starts-with(@class,"review_item")]'):
            item = BookingReviewItem()
            #item['url']=self
            #sometimes the title is empty because of some reason, not sure when it happens but this works
            title = rev.xpath('.//a[@class="review_item_header_content"]/span[@itemprop="name"]/text()')
            if title:
                item['title'] = title[0].extract()
                positive_content = rev.xpath('.//p[@class="review_pos"]//span/text()')
                if positive_content:
                    item['positive_content'] = positive_content[0].extract()
                negative_content = rev.xpath('.//p[@class="review_neg"]//span/text()')
                if negative_content:
                    item['negative_content'] = negative_content[0].extract()
                item['score'] = rev.xpath('.//span[@itemprop="reviewRating"]/meta[@itemprop="ratingValue"]/@content')[0].extract()
                #tags are separated by ;
                item['tags'] = ";".join(rev.xpath('.//li[starts-with(@class,"review_info_tag")]/text()').extract())
                item['hotel_name'] = hotel_name
                item['review_date'] = rev.xpath('//p[@class="review_item_date"]/text()')[0].extract()
                item['address'] = address
                item['hotel_class']=hotel_class
                yield item

        next_page = response.xpath('//a[@id="review_next_page_link"]/@href')
        if next_page:
            self.pageNumber += 1
            url = response.urljoin(next_page[0].extract().strip())
            yield scrapy.Request(url, self.parse_reviews)
