import scrapy
import re


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
        regex = re.compile("\u201c(.+?)\u201d")
        text = re.search(regex, quote_str)

        if text is not None:
            return text.group()
        else:
            return " ".join(quote_str.split())

    def sanitize_author(self, author_str):
        """ Sanitizes the text from the author string. """
        return " ".join(author_str.split())

    def sanitize_image(self, author_img_url):
        """ Sanitizes the text from the author string. """
        if author_img_url is None:
            author_img_url = "https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png"
        return author_img_url

    def sanitize_quote_tags(self, tags):
        """ Sanitizes and filters the tags comparing them to the allowed quote tags. """
        quote_tags = []
        for tag in tags:
            if tag in self.allowed_tag_categories:
                quote_tags.append(tag)

        return quote_tags if len(quote_tags) else ["other"]

    def parse(self, response):
        """ Parsing function for the spider's requests. """

        # Remove the line breaks on the html
        response = response.replace(body=response.body.replace(b"<br>", b""))

        for quote in response.css("div.quoteDetails"):
            text = quote.css("div.quoteText *::text").get()
            authorName = quote.css("div.quoteText span.authorOrTitle::text").get()
            authorImage = quote.css("a.leftAlignedImage img::attr(src)").get()
            tags = quote.css(
                "div.quoteFooter div.greyText.smallText.left a::text"
            ).getall()

            # Sanitize the data scraped
            self.logger.info("Sanitizing data")
            text = self.sanitize_quote(text)
            authorName = self.sanitize_author(authorName)
            authorImage = self.sanitize_image(authorImage)
            tags = self.sanitize_quote_tags(tags)

            yield dict(
                text=text, authorName=authorName, authorImage=authorImage, tags=tags,
            )

            # Scrape the next page
            next_page = response.css("a.next_page::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
