import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper
import re
import dateparser
from datetime import datetime


class HotGuysFuckSpider(BaseSceneScraper):
    name = 'HotMilfsFuck'
    network = "Hot Milfs Fuck"
    parent = "Hot Milfs Fuck"

    start_urls = [
        'https://www.hotmilfsfuck.com',
    ]

    selector_map = {
        'title': '//div[@class="video-player"]/div[@class="title-block"]/h2/text()',
        'description': '//div[@class="update-info-block"]/h3[contains(text(),"Description")]/following-sibling::text()',
        'date': '//div[@class="update-info-block"]/div[@class="row"]/div/div/i[@class="fa fa-calendar"]/following-sibling::strong/following-sibling::text()',
        'image': '//script[contains(text(),"video_content")]',
        'performers': '//section[@class="p-tb-50 bio-section-head"]/div/div/h2/text()',
        'tags': '//ul[@class="tags"]/li/a/text()',
        'trailer': '//script[contains(text(),"video_content")]',
        'external_id': '.*\\/(.*?)\\.html',
        'pagination': '/categories/movies_%s_d.html'
    }

    def get_scenes(self, response):

        scenes = response.xpath(
            '//div[@class="item item-update item-video"]/div[@class="content-div"]/h4/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene)

    def get_image(self, response):
        image = self.process_xpath(
            response, self.get_selector_map('image')).get()
        image = "https://www.hotmilfsfuck.com/" + \
            re.search('poster=\"(.*.jpg)\"', image).group(1).strip()

        return self.format_link(response, image)

    def get_trailer(self, response):
        if 'trailer' in self.get_selector_map() and self.get_selector_map('trailer'):
            trailer = self.process_xpath(
                response, self.get_selector_map('trailer')).get()
            trailer = "https://www.hotmilfsfuck.com/" + \
                re.search('src=\"(.*.mp4)\"', trailer).group(1).strip()
            return trailer
        return ''

    def get_description(self, response):

        description = response.xpath(
            '//div[@class="update-info-block"]/h3[contains(text(),"Description")]/following-sibling::text()').get()
        description = description.replace('\r\n', '').strip()

        return description
