import scrapy

from scrapy.loader import ItemLoader
from ..items import NlbkmufgjpItem
from itemloaders.processors import TakeFirst


class NlbkmufgjpSpider(scrapy.Spider):
	name = 'nlbkmufgjp'
	start_urls = ['https://www.nl.bk.mufg.jp/news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="row newsitem"]')
		for post in post_links:
			url = post.xpath('./div[contains(@class, "title")]/a/@href').get()
			date = post.xpath('./div[contains(@class, "date")]/text()').get()

			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//div[@class="text"]/h1/text()').get()
		description = response.xpath('//div[@class="text"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=NlbkmufgjpItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
