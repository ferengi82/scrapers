import dateparser
import scrapy
import re
import tldextract
from urllib.parse import urlparse

from tpdb.BaseSceneScraper import BaseSceneScraper


def match_site(argument):
    match = {
        'ariellynn': "Ariel Lynn",
        'behindtheporno': "Behind the Porno",
        'bigboobiesclub': "Big Boobies Club",
        'bigbouncybabes': "Big Bouncy Babes",
        'bigtoyxxx': "Big Toy XXX",
        'bondagelegend': "Bondage Legend",
        'bradsterling': "Brad Sterling",
        'britstudio': "BritStudio",
        'brittanysbubbles': "Brittany Andrews",
        'chocolatepov': "Chocolate POV",
        'furrychicks': "Furry Chicks",
        'hollyhotwife': "Holly Hotwife",
        'houseofyre': "House of Fyre",
        'internationalnudes': "International Nudes",
        'johnnygoodluck': "Johnny Goodluck",
        'meanawolf': "Meana Wolf",
        'minkaxxx': "Minka XXX",
        'oldsexygrannies': "Old Sexy Grannies",
        'ravenswallowzxxx': "Raven Swallows",
        'reidmylips': "Reid My Lips",
        'rionkingxxx': "Rion King",
        'seanmichaelsxxx': "Sean Michaels",
        'secretsusan': "Secret Susan",
        'sexykarenxxx': "Karen Fisher",
        'sheseducedme': "She Seduced Me",
        'sofiemariexxx': "Sofie Marie",
        'tabooadventures': "Taboo Adventures",
        'vanillapov': "Vanilla POV",
        'willtilexxx': "Will Tile",
        'xxxcellentadventures': "XXXCellent Adventures",
        'younggunsxxx': "Young Guns",
        'yummybikinimodel': "YummyBikiniModel",
        'yummygirlz': "YummyGirlz",
        'yummypinkxxx': "YummyPinkXXX",
        'yummypornclub': "YummyPornClub",
        'yummygirl': "YummyGirl",
        'yummywomen': "YummyWomen",
    }
    return match.get(argument, '')

class AndomarkSpider(BaseSceneScraper):
    name = 'Andomark'
    network = 'Andomark'

    # ~ custom_settings = {'CONCURRENT_REQUESTS': '2',
                       # ~ 'AUTOTHROTTLE_ENABLED': 'True',
                       # ~ 'AUTOTHROTTLE_DEBUG': 'False',
                       # ~ 'ITEM_PIPELINES': {
                           # ~ 'tpdb.pipelines.TpdbApiScenePipeline': 400,
                       # ~ },
                       # ~ 'DOWNLOADER_MIDDLEWARES': {
                           # ~ 'tpdb.middlewares.TpdbSceneDownloaderMiddleware': 543,
                       # ~ }
                       # ~ }

    start_urls = [
        'https://ariellynn.com',
        'https://behindtheporno.com',
        'https://bigboobiesclub.com',
        'https://bigbouncybabes.com',
        'https://bigtoyxxx.com',
        'https://bondagelegend.com',
        'https://bradsterling.elxcomplete.com',
        'https://britstudio.xxx',
        'https://brittanysbubbles.com',
        'https://chocolatepov.com',
        'https://furrychicks.elxcomplete.com',
        'https://hollyhotwife.elxcomplete.com',
        'https://www.houseofyre.com',
        'https://internationalnudes.com',
        'https://johnnygoodluck.com',
        'https://www.meanawolf.com',
        'https://www.minkaxxx.com',
        'https://oldsexygrannies.com',
        'https://ravenswallowzxxx.com',
        'https://reidmylips.elxcomplete.com',
        'https://rionkingxxx.com',
        'https://seanmichaelsxxx.com',
        'https://secretsusan.com',
        'http://sexykarenxxx.com',
        'https://sheseducedme.com',
        'https://sofiemariexxx.com',
        'https://tabooadventures.elxcomplete.com',
        'https://vanillapov.com',
        'https://willtilexxx.com',
        'https://xxxcellentadventures.com',
        'https://younggunsxxx.com',
        'https://yummybikinimodel.com',
        'https://yummygirlz.elxcomplete.com',
        'https://yummypinkxxx.elxcomplete.com',
        'https://yummypornclub.elxcomplete.com',
        # ~ #'https://yummygirl.com'  #screwed up, left in for list completion. Videos on other sites  
        'https://yummywomen.elxcomplete.com',
    ]

    selector_map = {
        'title': '//span[@class="update_title"]/text()',
        'date': '//span[@class="availdate"]/text()',
        'description': '//span[contains(@class,"description")]/text()',
        'image': '//meta[@property="og:image"]/@content',
        'performers': '//span[@class="tour_update_models"]/a/text()',
        'tags': '//span[@class="update_tags"]/a/text()',
        'external_id': 'updates/(.+)\\.html',
        'trailer': '//a[@class="update_image_big"]/@onclick',
        'pagination': '/categories/movies_%s_d.html'
    }
    
    cookies = {
        'SPSI':'1d516e4fb3be12e8c9f490625a3ae7b7',
    }

    def get_next_page_url(self, base, page):
        if 'yummygirl' in base:
            selector = '/updates/page_%s.html'
        elif 'sheseducedme' in base:
            selector = '/updates/page_%s.html'
        elif 'ariellynn' in base:
            selector = '/tour/categories/updates_%s_d.html'
        elif 'britstudio' in base or 'houseoffyre' in base:
            selector = '/categories/updates_%s_p.html'
        elif 'minkaxxx' in base:
            selector = '/tour/categories/movies_%s_d.html'
        elif 'sexykaren' in base:
            selector = '/tour2/categories/movies_%s_d.html'
        else:
            selector = '/categories/movies_%s_d.html'

        return self.format_url(base, selector % page)  
            
    def get_scenes(self, response):
        if 'britstudio' in response.url:
            scenes = response.xpath('//div[@class="update_details"]/div[contains(text(),"of video")]/../a[1]/@href').getall()
        if 'meanawolf' in response.url:
            scenes = response.xpath('//div[contains(@class,"videothumb")]/a[contains(@href,"/scenes/")]/@href').getall()
        elif 'minkaxxx' in response.url:
            scenes = response.xpath('//div[@class="modelimg"]/a/@href').getall()
        elif 'sexykaren' in response.url:
            scenes = response.xpath('//div[@class="modeldata"]/h3/a/@href').getall()
        else:
            scenes = response.xpath('//div[@class="updateItem"]/a/@href').getall()
        for scene in scenes:
            yield scrapy.Request(url=scene, callback=self.parse_scene,
                                 cookies=self.cookies)

    def get_trailer(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        trailer = self.process_xpath(response, self.get_selector_map('trailer')).get()
        if trailer:
            trailer = re.search('\'(.*.mp4)\'', trailer).group(1)
            if trailer:
                return domain + trailer
        
        return ''


    def get_date(self, response):
        if 'meanawolf' in response.url:
            date = response.xpath('//span[contains(text(),"ADDED:")]/following-sibling::text()').get()
        else:
            date = self.process_xpath(response, self.get_selector_map('date')).get()
            if not date:
                date = response.xpath('//span[@class="update_date"]/text()').get()
            if not date:
                date = response.xpath('//p[@class="date"]/text()').get()
            if date:
                date = date.strip()
                date = re.search('(\d{2}\/\d{2}\/\d{4})', date).group(1)


        if date:
            return dateparser.parse(date).isoformat()      

    def get_title(self, response):
        if 'minkaxxx' in response.url or 'sexykaren' in response.url:
            titlesearch = '//meta[@name="twitter:title"]/@content'
        elif 'houseofyre' in response.url:
            titlesearch = '//div[@class="update_block_info"]/span[@class="update_title"]/text()'
        elif 'meanawolf' in response.url:
            titlesearch = '//h3/text()'
        else:
            titlesearch = '//span[@class="update_title"]/text()'
                    
        title = response.xpath(titlesearch).get()
        if not title:
            title = response.xpath('//meta[@property="og:title"]/@content').get()
            if " - " in title:
                title = re.search('^(.*)\ -\ ', title).group(1)
            else:
                title = ''
        
        return title.strip()
        
                
    def get_image(self, response):
        if 'minkaxxx' in response.url:
            imagesearch = '//div[@class="videoplayer"]/img/@src0_1x'
            image = response.xpath(imagesearch).get()
            if image:
                image = "https://minkaxxx.com" + image
        elif 'sexykaren' in response.url:
            imagesearch = '//script[contains(text(),"video_content")]'
            image = response.xpath(imagesearch).get()
            if image:
                image = re.search('poster=\"(.*?.jpg)\"', image).group(1)

            if not image:
                image = response.xpath('//div[@class="videoplayer"]/img/@src0_1x').get()
            if image:
                image = "http://sexykarenxxx.com" + image
        elif 'meanawolf' in response.url:
            imagesearch = '//script[contains(text(),"useimage")]/text()'
            image = response.xpath(imagesearch).get()
            if image:
                image = re.search('useimage\ =\ \"(.*?)\";', image).group(1)
        else:
            imagesearch = '//meta[@property="og:image"]/@content'
            image = response.xpath(imagesearch).get()
            
        if not image:
            image = response.xpath('//meta[@name="twitter:image"]/@content').get()
            if not image:
                return ''

        return self.format_link(response, image)      
        
    def get_tags(self, response):
        if 'minkaxxx' in response.url or 'sexykaren' in response.url:
            tagsearch = '//div[@class="videodetails"]/p/a/text()'
        elif 'meanawolf' in response.url:
            tagsearch = '//span[contains(text(),"TAGS:")]/following-sibling::a[contains(@href,"/categories/")]/text()'
        else:
            tagsearch = '//span[@class="update_tags"]/a/text()'
                    
        tags = response.xpath(tagsearch).getall()
        if not tags:
            tags = response.xpath('//span[@class="tour_update_tags"]/a/text()').getall()
        
        if tags:
            return list(map(lambda x: x.strip().title(), tags))
        return []

        
    def get_site(self, response):
        parsed_uri = tldextract.extract(response.url)
        if parsed_uri.domain == "elxcomplete":
            domain = parsed_uri.subdomain
        else:
            domain = parsed_uri.domain
        site = match_site(domain)
        if not site:
            site = tldextract.extract(response.url).domain
            
        return site
        
    def get_parent(self, response):
        parsed_uri = tldextract.extract(response.url)
        if parsed_uri.domain == "elxcomplete":
            domain = parsed_uri.subdomain
        else:
            domain = parsed_uri.domain
        parent = match_site(domain)
        if not parent:
            parent = tldextract.extract(response.url).domain
            
        return parent
        
    def get_id(self, response):
        if 'minkaxxx' in response.url or 'sexykaren' in response.url:
            idsearch = 'trailers\/(.+)\\.html'
        elif 'meanawolf' in response.url:
            idsearch = 'scenes\/(.+)\\.html'
        else:
            idsearch = 'updates\/(.+)\\.html'
            
        search = re.search(idsearch, response.url, re.IGNORECASE)
        return search.group(1)        

    def get_performers(self, response):
        if 'minkaxxx' in response.url:
            return ["Minka"]
        elif 'sexykaren' in response.url:
            return ["Karen Fisher"]
        elif 'houseofyre' in response.url:
            performersearch = '//div[@class="update_block_info"]/span[@class="tour_update_models"]/a/text()'
        elif 'meanawolf' in response.url:
            performersearch = '//span[contains(text(),"FEATURING:")]/following-sibling::a[contains(@href,"/models/")]/text()'
        else:
            performersearch = self.get_selector_map('performers')
            
        performers = response.xpath(performersearch).getall()
        return list(map(lambda x: x.strip(), performers))
        
    def get_description(self, response):
        if 'meanawolf' in response.url:
            description = response.xpath('//div[@class="trailerContent"]/p/text()').getall()
            if description:
                if len(description) > 1:
                    description = " ".join(description)
                return description
        if 'description' not in self.get_selector_map():
            return ''

        description = self.process_xpath(
            response, self.get_selector_map('description')).get()

        if description is not None:
            return description.replace('Description:', '').strip()
        return ""        
