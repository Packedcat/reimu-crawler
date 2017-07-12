import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allow_domains = ['blog.reimu.net']
    start_urls = [
        'https://blog.reimu.net',
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split('/')[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
            # f.write(response.body)
        # self.log('Saved file %s' % filename)
        for article in response.css('article.hentry'):
            img = article.css('div.entry-content').css('img')
            yield {
                'title': article.css('h2.entry-title').css('a::text').extract_first(),
                'link':  article.css('h2.entry-title').css('a').re(r'href="(.*?)"')[0],
                'image': len(img) > 0 and img.re(r'src="(.*?)"')[0] or None,
            }
