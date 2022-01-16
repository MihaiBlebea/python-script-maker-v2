#!/usr/bin/env python3

SCRAPER_TEMPLATE = """
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

from spider import DemoSpider

results = []

def crawler_results(signal, sender, item, response, spider):
	results.append(item)

def scrape():
	dispatcher.connect(crawler_results, signal=signals.item_scraped)

	process = CrawlerProcess()

	process.crawl(DemoSpider)

	process.start()

	return results

if __name__ == "__main__":
	print(scrape())
"""

SPIDER_TEMPLATE = """
from scrapy import Spider, Request


class DemoSpider(Spider):

	name = "demo"

	start_url = "https://google.com"

	def start_requests(self):
		yield Request(self.start_url, callback=self.parse_results)

	def parse_results(self, response):
		pass
"""

def main():
    write_file("scraper.py", SCRAPER_TEMPLATE.strip())
    write_file("spider.py", SPIDER_TEMPLATE.strip())


def write_file(file_path: str, content: str):
    f = open(file_path, "w")
    f.write(content)
    f.close()


if __name__ == "__main__":
    main()