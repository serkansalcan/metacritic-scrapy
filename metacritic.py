import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MetacriticSpider(CrawlSpider):
    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    start_urls = ["https://www.metacritic.com/game"]

    rules = (
        Rule(LinkExtractor(restrict_css=".genre_text"), callback="parse_item", follow=False),
    )

    def parse_item(self, response):
        genre = response.css(".browse-list-heading::text").get().strip()
        games = response.css("td.clamp-summary-wrap")
        for game in games:
            yield{
                "title": game.css(".title h3::text").get().strip(),
                "metaScore": game.css("div.clamp-metascore a.metascore_anchor div::text").get(),
                "userScore": game.css("div.clamp-userscore a.metascore_anchor div::text").get(),
                "genre": genre,
                "platform": game.css(".platform .data::text").get().strip(),
                "releaseDate": game.css(".platform+ span::text").get().strip(),
                "link": "www.metacritic.com" + game.css(".title::attr(href)").get().strip()
            }

        next_page = response.css(".next .action::attr(href)").get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_item)
