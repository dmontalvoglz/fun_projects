import scrapy


class QuoteSpider(scrapy.Spider):
    name = "quote"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for book in response.xpath('//article[@class="product_pod"]'):
            star_rating = book.xpath('./p/@class').get()
            star_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            star_number = star_dict.get(star_rating.split()[-1], 'No rating')
            yield {
                'title': book.xpath('./h3/a/@title').get(),
                'rating': star_number,
                'price': book.xpath('.//p[@class="price_color"]/text()').get()
            }
        #next_page = response.xpath('//li[@class="next"]/a/@href').get()
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)
        