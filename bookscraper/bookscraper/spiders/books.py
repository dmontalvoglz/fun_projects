import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # Extract the URLs of the books
        book_urls = response.xpath('//article[@class="product_pod"]/h3/a/@href').extract()
        for book_url in book_urls:
            # Send a request to each book's URL
            yield response.follow(book_url, self.parse_book)

    def parse_book(self, response):
        # Extract the information from the book's page
        stars_path = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        stars_split = stars_path.split()

        tbl_dict = {}

        tbl_rows = response.xpath('//*[@id="content_inner"]/article/table/tr')
        for row in tbl_rows:
            th_value = row.xpath('.//th/text()').get()
            if th_value in ('UPC', 'Price (excl. tax)', 'Price (incl. tax)', 'Availability'):
                tbl_dict[th_value] = row.xpath('.//td/text()').get()

        yield {
            'title': response.xpath('//div[contains(@class, "product_main")]/h1/text()').get(),
            'stars': stars_split[1],
            **tbl_dict
        }