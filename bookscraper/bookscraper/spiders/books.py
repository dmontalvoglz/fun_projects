import scrapy
import re

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

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        # Extract the information from the book's page
        stars_path = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        stars_split = stars_path.split()

        tbl_dict = {}

        tbl_rows = response.xpath('//*[@id="content_inner"]/article/table/tr')
        for row in tbl_rows:
            th_value = row.xpath('.//th/text()').get()
            match th_value:
                case 'UPC':
                    tbl_dict[th_value] = row.xpath('.//td/text()').get()
                case 'Price (excl. tax)':
                    tbl_dict['Price(notax)'] = row.xpath('.//td/text()').get()
                case 'Price (incl. tax)':
                    tbl_dict['Price(tax)'] = row.xpath('.//td/text()').get()
                case 'Availability':
                    raw_string = row.xpath('.//td/text()').get()
                    reg_pattern = re.search(r'\((.*?)\)', raw_string)
                    stock_extracted = reg_pattern.group(1)
                    tbl_dict[th_value] = stock_extracted

        yield {
            'title': response.xpath('//div[contains(@class, "product_main")]/h1/text()').get(),
            'stars': stars_split[1],
            **tbl_dict
        }