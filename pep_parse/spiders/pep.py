from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        peps = response.css('section#numerical-index tbody tr')
        for pep_url in peps:
            pep = urljoin(PepSpider.start_urls[0],
                          pep_url.css('td a::attr(href)').getall()[0])
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        h1 = response.css('h1.page-title::text').get().strip()
        num = h1.partition(' – ')[0]
        status = response.css('dt:contains("Status") + dd::text').get()
        data = {
            'number': num.replace('PEP ', ''),
            'name': h1,
            'status': status,
        }
        yield PepParseItem(data)
