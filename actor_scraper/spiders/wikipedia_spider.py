import scrapy
from actor_scraper.items import ActorScraperItem


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]

    start_urls = [
        "https://en.wikipedia.org/wiki/Leonardo_DiCaprio_filmography",
        "https://en.wikipedia.org/wiki/Jackie_Chan_filmography",
    ]

    def parse(self, response):
        seed_actor = self.get_seed_actor(response.url)
        seen_links = set()

        rows = response.xpath('//table[contains(@class, "wikitable")]//tr')

        for row in rows:
            movie_link = row.xpath('.//i//a/@href').get()
            movie_title = row.xpath('.//i//a/text()').get()

            if not movie_link:
                movie_link = row.xpath('.//td[2]//a[1]/@href').get()

            if not movie_title:
                movie_title = row.xpath('.//td[2]//a[1]/text()').get()

            if not movie_link or not movie_title:
                continue

            if not movie_link.startswith("/wiki/"):
                continue

            if ":" in movie_link:
                continue

            full_url = response.urljoin(movie_link)

            if full_url not in seen_links:
                seen_links.add(full_url)
                yield response.follow(
                    full_url,
                    callback=self.parse_movie,
                    meta={"seed_actor": seed_actor}
                )

    def parse_movie(self, response):
        seed_actor = response.meta["seed_actor"]

        movie_title = response.xpath('//h1[@id="firstHeading"]/text()').get()
        if movie_title:
            movie_title = movie_title.strip()

        year = self.extract_year(response)
        director = self.extract_director(response)
        genre = self.extract_genre(response)
        cast = self.extract_starring(response)

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
            item["source"] = "wikipedia"
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
                item["source"] = "wikipedia"
                item["year"] = year
                item["director"] = director
                item["genre"] = genre
                yield item

    def get_seed_actor(self, url):
        if "Leonardo_DiCaprio" in url:
            return "Leonardo DiCaprio"
        if "Jackie_Chan" in url:
            return "Jackie Chan"
        return "Unknown"

    def extract_year(self, response):
        release_text = " ".join(
            response.xpath(
                '//table[contains(@class, "infobox")]//th[contains(text(), "Release date")]/following-sibling::td//text()'
            ).getall()
        ).strip()

        year = self.find_year_in_text(release_text)
        if year is not None:
            return year

        first_paragraph = " ".join(response.xpath('//p[1]//text()').getall()).strip()
        return self.find_year_in_text(first_paragraph)

    def find_year_in_text(self, text):
        cleaned_text = text.replace("(", " ").replace(")", " ").replace(",", " ")
        words = cleaned_text.split()

        for word in words:
            if len(word) == 4 and word.isdigit():
                year_num = int(word)
                if 1900 <= year_num <= 2099:
                    return year_num
        return None

    def extract_director(self, response):
        directors = response.xpath(
            '//table[contains(@class, "infobox")]//th[contains(text(), "Directed by")]/following-sibling::td//a/text()'
        ).getall()

        if not directors:
            directors = response.xpath(
                '//table[contains(@class, "infobox")]//th[contains(text(), "Directed by")]/following-sibling::td//text()'
            ).getall()

        directors = [d.strip() for d in directors if d.strip()]

        if directors:
            return ", ".join(directors)
        return None

    def extract_starring(self, response):
        starring = response.xpath(
            '//table[contains(@class, "infobox")]//th[contains(text(), "Starring")]/following-sibling::td//a/text()'
        ).getall()

        if not starring:
            starring = response.xpath(
                '//table[contains(@class, "infobox")]//th[contains(text(), "Starring")]/following-sibling::td//li//text()'
            ).getall()

        return [name.strip() for name in starring if name.strip()]

    def extract_genre(self, response):
        categories = response.xpath('//div[@id="mw-normal-catlinks"]//a/text()').getall()
        categories = [c.strip() for c in categories if c.strip() and c.strip() != "Categories"]

        keywords = [
            "action", "comedy", "drama", "thriller", "crime", "science fiction",
            "romance", "adventure", "fantasy", "martial arts", "animation",
            "war", "mystery", "biographical", "historical", "sports",
            "western", "horror"
        ]

        found_genres = []

        for category in categories:
            lower_category = category.lower()
            for word in keywords:
                if word in lower_category and word not in found_genres:
                    found_genres.append(word)

        if found_genres:
            return ", ".join(found_genres)
        return None