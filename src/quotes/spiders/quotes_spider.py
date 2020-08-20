import scrapy


class QuotesSpider(scrapy.Spider):
    """ Web Scraping Spider for Goodreads website. """

    # Class attributes
    name = "quotes"
    start_urls = ["https://www.goodreads.com/quotes?page=1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_tag_categories = [
            "love",
            "life",
            "inspiration",
            "humor",
            "philosophy",
            "god",
            "truth",
            "widsom",
            "romance",
            "poetry",
            "death",
            "happiness",
            "hope",
            "faith",
            "religion",
            "life-lessons",
            "success",
            "motivational",
            "time",
            "knowledge",
            "love",
            "spirituality",
            "science",
            "books",
        ]

    def sanitize_quote(self, quote_str):
        """ Sanitizes the text from the quote string. """
        pass

    def sanitize_author(self, author_str):
        """ Sanitizes the text from the author string. """
        return author_str.replace(",", "")

    def sanitize_quote_tags(self, tags):
        """ Sanitizes and filters the tags comparing them to the allowed quote tags. """
        quote_tags = []
        for tag in tags:
            if tag in self.allowed_tag_categories:
                quote_tags.append(tag)

        return quote_tags if len(quote_tags) else ["other"]

    def parse(self, response):
        """ Parsing function for the spider's requests. """

        for quote in response.css("div.quoteDetails"):
            text = quote.css("div.quoteText::text").get()
            authorName = quote.css("div.quoteText span.authorOrTitle::text").get()
            authorImage = quote.css("a.leftAlignedImage img::attr(src)").get()
            tags = quote.css(
                "div.quoteFooter div.greyText.smallText.left a::text"
            ).getall()

            # Parse and clean
            text = self.sanitize_quote(text)
            authorName = self.sanitize_author(authorName)
            tags = self.sanitize_quote_tags(tags)

            yield dict(
                text=text, authorName=authorName, authorImage=authorImage, tags=tags,
            )

            # Scrape the next page
            next_page = response.css("a.next_page::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)

