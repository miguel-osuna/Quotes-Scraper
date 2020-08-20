# Standard library imports
from scrapy import Spider
from scrapy.loader import ItemLoader

# Local application imports
from quotes.items import QuotesItem

quote_item = QuotesItem()


class QuotesSpider(Spider):
    """ Web Scraping Spider for Goodreads website. """

    # Class attributes
    name = "quotes"
    start_urls = ["https://www.goodreads.com/quotes?page=1"]

    def parse(self, response):
        """ Parsing function for the spider's requests. """

        # Remove the line breaks on the html
        response = response.replace(body=response.body.replace(b"<br>", b""))

        for quote in response.css(".quoteDetails"):
            # Create an item loader with the quote data and add it as a new quote_item

            self.logger.info("Creating quote_item")

            loader = ItemLoader(item=QuotesItem(), selector=quote)
            loader.add_css("quote_content", ".quoteText::text")
            print(loader.get_css(".quoteText::text"))
            loader.add_css("author_name", ".quoteText .authorOrTitle::text")
            loader.add_css("author_image", ".leftAlignedImage img::attr(src)")
            loader.add_css("tags", ".greyText.smallText.left a::text")
            quote_item = loader.load_item()

            yield quote_item

            # # Scrape the next page
            # next_page = response.css("a.next_page::attr(href)").get()
            # if next_page is not None:
            #     yield response.follow(next_page, self.parse)
