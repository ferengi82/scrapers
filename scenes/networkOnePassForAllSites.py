import re

import dateparser
import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper


class OnePassForAllSitesSpider(BaseSceneScraper):
    name = 'OnePassForAllSites'
    network = "1 Pass for All Sites"

    start_urls = [
        'https://www.1passforallsites.com'
    ]

    selector_map = {
        'title': '//div[@class="block-title"]/p[@class="path"]/span[@class="path-arrow"]/following-sibling::text()',
        'description': '//div[@class="sp-info-txt"]/h3/following-sibling::p/text()',
        'date': '//div[@class="movie-info"]/ul/li[contains(text(),"Added:")]/span/text()',
        'image': '//video/@poster',
        'performers': '//p[@class="sp-info-name"]/a/text()',
        'tags': '//p[@class="niches-list"]/a/text()',
        'external_id': '\\/episode\\/(\\d+)\\/',
        'trailer': '//video/source[@data-quality="SD"]/@src',
        'pagination': '/scenes/date?page=%s&site=0&order=date'
    }

    def get_scenes(self, response):
        scenes = response.xpath(
            "//ul[@class='thumbs tn-updates tn-allmovs']/li/a[@class='tn']/@href").getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene)

    def get_site(self, response):
        site = response.xpath('//p[@class="path"]/a/text()').get().strip()
        return site

    def get_image(self, response):
        image = self.process_xpath(
            response, self.get_selector_map('image')).get()
        if not image:
            image = "http://1passforallsites.com/media/thumbs/movie_tn.jpg"

        return self.format_link(response, image)

    def get_title(self, response):
        title = self.process_xpath(
            response, self.get_selector_map('title')).get()
        if not title:
            title = "No Title Available"
        else:
            title = title.strip().replace(u'\xa0', u' ')
        return title
