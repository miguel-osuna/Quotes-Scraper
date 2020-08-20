import re
from scrapy.item import Item, Field
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def sanitize_quote(quote_list):
    """ Sanitizes the text from the quote string list. """
    quote_str = " ".join(quote_list)
    regex = re.compile("\u201c(.+?)\u201d")
    text = re.search(regex, quote_str)

    # If there was a match with the regular expressions
    if text is not None:
        text = text.group().strip(u"\u201c" u"\u201d")
        return text
    else:
        return quote_str


def sanitize_author(author_str):
    """ Sanitizes the text from the author string. """
    return " ".join(author_str.split())


def sanitize_image(author_img_url):
    """ Sanitizes the text from the author string. """
    if author_img_url is None:
        author_img_url = "https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png"
    return author_img_url


def sanitize_quote_tags(tag_list):
    allowed_tag_categories = [
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

    """ Sanitizes and filters the tags comparing them to the allowed quote tags. """
    quote_tags = []
    for tag in tag_list:
        if tag in allowed_tag_categories:
            quote_tags.append(tag)

    return quote_tags if len(quote_tags) else ["other"]


class QuotesItem(Item):
    quote_content = Field(
        input_processor=Compose(sanitize_quote), output_processor=TakeFirst()
    )
    author_name = Field(
        input_processor=MapCompose(sanitize_author), output_processor=TakeFirst()
    )
    author_image = Field(
        input_processor=MapCompose(sanitize_image), output_processor=TakeFirst()
    )
    tags = Field(input_processor=Compose(sanitize_quote_tags))
