import scrapy

#XPAth

#link    =  response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
#title   = response.xpath('//h1[@class="documentFirstHeading"]/text()').getall()
#body    = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').getall()
#adjunto = response.xpath('//div[@class="links"]//a/@href').getall()

class SpiderCia(scrapy.Spider):
    name       = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI'             : 'cia.json',
        'FEED_FORMAT'          : 'json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    }

    def parse(self, response):
        links_declassified = response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').extract()
        for link in links_declassified:
            #para que pueda trabajar en scraping hub necesitamos cambiar cb_kwargs por meta y get y getall por extract
            yield response.follow(link, callback = self.parse_link, meta={'url': response.urljoin(link)})

    def parse_link(self, response):
        link    = response.meta['url']
        title   = response.xpath('//h1[@class="documentFirstHeading"]/text()').extract()
        body    = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').extract()

        yield{
            'url'     : link,
            'title'   : title,
            'body'    : body
        }
            