import scrapy


class ActorScraperItem:
    pass


class ActorScraperItem(scrapy.Item):
    seed_actor = scrapy.Field()
    movie_title = scrapy.Field()
    co_actor = scrapy.Field()
    source = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    genre = scrapy.Field()

print(ActorScraperItem.fields)