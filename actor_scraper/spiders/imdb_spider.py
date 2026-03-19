import scrapy
from actor_scraper.items import ActorScraperItem


class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com", "www.imdb.com"]

    start_urls = [
        "https://www.imdb.com/name/nm0000138/",
        "https://www.imdb.com/name/nm0000329/",
    ]

    def parse(self, response):
        seed_actor = self.get_seed_actor(response.url)

        # try to find title links from actor page
        title_links = response.xpath('//a[contains(@href, "/title/tt")]/@href').getall()

        seen = set()

        for link in title_links:
            if not link:
                continue

            clean_link = link.split("?")[0]

            if "/title/tt" not in clean_link:
                continue

            full_url = response.urljoin(clean_link)

            if full_url in seen:
                continue

            seen.add(full_url)

            yield response.follow(
                full_url,
                callback=self.parse_movie,
                meta={"seed_actor": seed_actor}
            )

    def parse_movie(self, response):
        seed_actor = response.meta["seed_actor"]

        movie_title = self.extract_movie_title(response)
        year = self.extract_year(response)
        director = self.extract_director(response)
        genre = self.extract_genre(response)
        cast = self.extract_cast(response)

        clean_cast = []

        for actor in cast:
            actor = actor.strip()
            if not actor:
                continue
            if actor.lower() == seed_actor.lower():
                continue
            if actor not in clean_cast:
                clean_cast.append(actor)

        if not clean_cast:
            item = ActorScraperItem()
            item["seed_actor"] = seed_actor
            item["movie_title"] = movie_title
            item["co_actor"] = None
            item["source"] = "imdb"
            item["year"] = year
            item["director"] = director
            item["genre"] = genre
            yield item
        else:
            for co_actor in clean_cast:
                item = ActorScraperItem()
                item["seed_actor"] = seed_actor
                item["movie_title"] = movie_title
                item["co_actor"] = co_actor
                item["source"] = "imdb"
                item["year"] = year
                item["director"] = director
                item["genre"] = genre
                yield item

    def get_seed_actor(self, url):
        if "nm0000138" in url:
            return "Leonardo DiCaprio"
        if "nm0000329" in url:
            return "Jackie Chan"
        return "Unknown"

    def extract_movie_title(self, response):
        title = response.xpath('//h1/text()').get()
        if title:
            return title.strip()

        title = response.xpath('//title/text()').get()
        if title:
            return title.strip()

        return None

    def extract_year(self, response):
        texts = response.xpath('//text()').getall()

        for text in texts:
            if not text:
                continue

            words = (
                text.replace("(", " ")
                .replace(")", " ")
                .replace(",", " ")
                .replace("/", " ")
                .split()
            )

            for word in words:
                if len(word) == 4 and word.isdigit():
                    year_num = int(word)
                    if 1900 <= year_num <= 2099:
                        return year_num

        return None

    def extract_director(self, response):
        directors = response.xpath(
            '//a[contains(@href, "/name/") and contains(@href, "ref_=tt_ov_dr")]/text()'
        ).getall()

        if not directors:
            directors = response.xpath(
                '//*[contains(text(), "Director")]/following::a[contains(@href, "/name/")][1]/text()'
            ).getall()

        directors = [d.strip() for d in directors if d.strip()]

        if directors:
            return ", ".join(directors)

        return None

    def extract_genre(self, response):
        genres = response.xpath(
            '//a[contains(@href, "/search/title?genres=")]/text()'
        ).getall()

        if not genres:
            genres = response.xpath(
                '//*[contains(text(), "Genre")]/following::a[1]/text()'
            ).getall()

        genres = [g.strip() for g in genres if g.strip()]

        if genres:
            unique_genres = []
            for g in genres:
                if g not in unique_genres:
                    unique_genres.append(g)
            return ", ".join(unique_genres)

        return None

    def extract_cast(self, response):
        cast = response.xpath(
            '//a[contains(@href, "/name/") and contains(@href, "ref_=tt_cl_i")]/text()'
        ).getall()

        if not cast:
            cast = response.xpath(
                '//a[contains(@href, "/name/nm")]/text()'
            ).getall()

        clean_names = []

        for name in cast:
            name = name.strip()
            if not name:
                continue

            if name.lower() in ["cast", "director", "writers", "stars"]:
                continue

            if name not in clean_names:
                clean_names.append(name)

        return clean_names