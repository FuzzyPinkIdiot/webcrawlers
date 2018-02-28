from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	count = 1
	print("ID,Name,Members,QuestItem,Tradeable,Equipable,Stackable,Examine")
	possibleCategories=['Members only', 'Tradeable', 'Equipable', 
						'Stackable', 'Alchemy', 'Destroy', 'Store price', 'Weight', 
						'Examine', 'Members only', 'Quest item', 'Tradeable', 'Equipable', 
						'Stackable', 'Alchemy', 'Destroy', 'Store price', 'Weight', 
						'Examine', 'High Alch', 'Low Alch', 'Exchange price', 'Buy limit', 
						'Edible']
	
	def start_requests(self):
		global urls
		urls = ['http://runescape.wikia.com/wiki/Category:Items#mw-pages']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse_collections)
	
	def parse_collections(self, response):
		itemPages = HtmlXPathSelector(response).select('//div[@class="mw-content-ltr"]/table/tr/td/ul/li/a/@href')
		for item in itemPages:
			nextItemPage = ("http://oldschoolrunescape.wikia.com" + item.extract())
			yield scrapy.Request(url=nextItemPage, callback=self.parse_item)
		nextPage = HtmlXPathSelector(response).select('//div[@id="mw-pages"]/a[contains(text(),"next 200")]/@href')
		nextPageURL = ("http://oldschoolrunescape.wikia.com" + nextPage[0].extract())
		yield scrapy.Request(url=nextPageURL, callback=self.parse_collections)
		#print(self.possibleCategories)
	
	def parse_item(self,response):
		titles = HtmlXPathSelector(response).select('//title/text()').extract()
		title = titles[0].split(" | ")
		#categories = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr/th/a/text()').extract()
		#categoryValues = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr/td/text()').extract()
		membersList = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[3]/td/text()').extract()
		members = membersList[0]
		members = members[0:len(members)-1]
		
		questItem = ""
		if HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[4]/td/a'):
			questItemList = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[4]/td/a/text()').extract()
			questItem = questItemList[0]
		else:
			questItemList = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[4]/td/text()').extract()
			questItem = questItemList[0]
			questItem = questItem[0:len(questItem)-1]
			
		tradeableList = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[5]/td/text()').extract()
		tradeable = tradeableList[0]
		tradeable = tradeable[0:len(tradeable)-1]
		
		equipableList = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[6]/td/text()').extract()
		equipable = equipableList[0]
		equipable = equipable[0:len(equipable)-1]
		if "," in equipable:
			equipable = "'" + equipable + "'"
		
		stackableList = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr[7]/td/text()').extract()
		stackable = stackableList[0]
		stackable = stackable[0:len(stackable)-1]
		
		categoryValues = HtmlXPathSelector(response).select('//table[@class="wikitable infobox"]/tr/td/text()').extract()
		examine = categoryValues[len(categoryValues)-1]
		examine = examine[0:len(examine)-1]
		if "," in examine:
			examine = "'" + examine + "'"
		
		finalString = str(self.count) + "," + title[0] + "," + members + "," + questItem + "," + tradeable + "," + equipable + "," + stackable + "," + examine
		self.count = self.count + 1
		print(finalString)
