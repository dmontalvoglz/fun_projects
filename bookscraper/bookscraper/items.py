import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    stars = scrapy.Field()
    UPC = scrapy.Field()
    price_notax = scrapy.Field()
    price_tax = scrapy.Field()
    availability = scrapy.Field()