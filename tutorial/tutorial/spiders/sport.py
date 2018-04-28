# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tutorial.items import TutorialItem

class SportSpider(CrawlSpider):
    name = "sport"
    start_urls = ['https://thethao.vnexpress.net/']
    def parse(self, response):
        for article in response.xpath('//section[@id="news_home"]/article[@class="list_news"]'):
	    link = article.xpath('.//h3[@class="title_news"]/a/@href').extract_first()
	    yield scrapy.Request(link, callback=self.parse_content)            
    	next_page_url = response.xpath('//div[@id="pagination"]/a[@class="active"]/following-sibling::*/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url)

    def parse_content(self, response):
    	item = TutorialItem()
	item["origin"] = 'Nhom_13'    	
	item["link"] = response.url
    	item["title"] = response.xpath('//section[@class="sidebar_1"]/h1/text()').extract_first()
	link = ''
	for p in response.xpath('//section[@class="sidebar_1"]/article/p'):
	    if(p.xpath('.//span/text()') != []):
    	        link = link + p.xpath('.//span/text()').extract_first() + ' '
	    if(p.xpath('.//text()') != []):
    	        link = link + p.xpath('.//text()').extract_first() + ' '
	item["content"] = link
	yield item

