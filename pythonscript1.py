from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "chester"
	count = 1
	print("ID,Name,Members,Tradeable,Bankable,Disassembly,Weight,Examine")
	
	def start_requests(self):
		global urls
		urls = ['http://runescape.wikia.com/wiki/Category:Items#mw-pages']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse_collections)
	
	def parse_collections(self, response):
		itemPages = HtmlXPathSelector(response).select('//div[@class="mw-content-ltr"]/table/tr/td/ul/li/a/@href')
		for item in itemPages:
			nextItemPage = ("http://runescape.wikia.com" + item.extract())
			yield scrapy.Request(url=nextItemPage, callback=self.parse_item)
		nextPage = HtmlXPathSelector(response).select('//div[@id="mw-pages"]/a[contains(text(),"next 200")]/@href')
		nextPageURL = ("http://runescape.wikia.com" + nextPage[0].extract())
		yield scrapy.Request(url=nextPageURL, callback=self.parse_collections)
		#print(self.possibleCategories)
	
	def parse_item(self,response):
		titles = HtmlXPathSelector(response).select('//title/text()').extract()
		title = titles[0].split(" | ")
		title = title[0]
		if title == "Findable items" or title == "Items":
			title = "not valid"
		else:
			disassembly = ""
			members = ""
			tradeable = ""
			examine = ""
			bankable = ""
			weight = ""
			for tr in HtmlXPathSelector(response).select('//table/tr'):
				root = tr.xpath('th/a/text()').extract()
				if "Disassembly" in root:
					disassembText = tr.xpath('td/a/text()').extract()
					if "Yes" in disassembText:
						disassembly = "Yes"
					else:
						disassembly = "No"
				if "Members" in root:
					membersText = tr.xpath('td/text()').extract()
					members = membersText[0]
				if "Tradeable" in root:
					tradeableText = tr.xpath('td/text()').extract()
					tradeable = tradeableText[0]
				if "Examine" in root:
					examineText = tr.xpath('td/text()').extract()
					examine = examineText[0]
				if "Bankable" in root:
					bankText = tr.xpath('td/text()').extract()
					bankable = bankText[0]
				if "Weight" in root:
					weightText = tr.xpath('td/text()').extract()
					weight = weightText[0]
					
			if bankable == "":
				bankable = "yes"
			finalString = str(self.count) + "," + title + "," + members + "," + tradeable + "," + bankable + "," + disassembly + "," + weight + "," + examine
			self.count = self.count + 1
		
			print (finalString)
