import scrapy,random,string
from ..items import ReliancedigitalElectronicsItem

class RelianceSpider(scrapy.Spider):
    name = 'reliancecamera'
    pageno=2
    start_urls=['https://www.reliancedigital.in/dslr-cameras/c/S101110?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock&page=0']

    def parse(self, response, **kwargs):

        page = response.css(".sp a::attr('href')").getall()
        for p in page:
            url = 'https://www.reliancedigital.in' + p
            yield scrapy.Request(url, callback=self.parse_elec)

        for page in ['https://www.reliancedigital.in/mirrorlesss-cameras/c/S101119?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock&page=0',
                     'https://www.reliancedigital.in/point-shoot-cameras/c/S101111?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock&page=0',
                     'https://www.reliancedigital.in/prosumer-cameras/c/S101112?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock&page=0',
                     'https://www.reliancedigital.in/action-cameras/c/S101113?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock&page=0']:

                   yield response.follow(page, callback=self.parse)



    def parse_elec(self, response):

                    items = ReliancedigitalElectronicsItem()

                    product_name = response.css('.pdp__title::text').get()
                    storeprice = response.css('.pdp__offerPrice::text').extract()
                    storeLink = response.url
                    photos =  response.css(".pdp__mainHeroImgContainer::attr('data-srcset')").get()
                    id = storeLink[::-1][:storeLink[::-1].find('/')]
                    #rating = response.css('.hGSR34::text').extract()
                    #reviews = response.css('.qwjRop div div::text').extract()
                    product_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))
                    spec_title = response.css(".pdp__tab-info__list__name::text").extract()
                    spec_detail = response.css(".pdp__tab-info__list__value::text").extract()




                    stores = {
                        "rating" : "NA",
                        "reviews" : [],
                        "storeProductId": id[::-1],
                        "storeLink": storeLink,
                        "storeName": "RelianceDigital",
                        "storePrice": storeprice[0][1:]
                    }

                    items['product_name'] = product_name
                    items['product_id'] = product_id
                    items['stores'] = stores
                    items['category'] = 'electronics'
                    items['subcategory'] = 'cameras'
                    items['brand'] = product_name.split()[0]
                    items['description']={}

                    for i in range(len(spec_title)):

                                           items['description'][spec_title[i]] = spec_detail[i]


                    items["photos"] = 'https://www.reliancedigital.in'+ photos



                    yield items