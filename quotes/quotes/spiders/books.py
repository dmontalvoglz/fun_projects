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
        yield {
            'title': response.xpath('//div[contains(@class, "product_main")]/h1/text()').get(),
            # Add more fields here as needed
        }