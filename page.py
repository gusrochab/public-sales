import requests
from urllib3.exceptions import NewConnectionError, LocationParseError
from requests.exceptions import ConnectionError, InvalidURL
from text_parcers import *
from link_parcers import *


class Page:
    """
    A webpage object
    """

    def __init__(self, link):
        """
        :param link: Pages link
        """
        self.all_page_links = []
        # True if the page status is 200
        self.broken = False
        # recursion depth
        self.depth = None
        self.html_status = None
        self.label = None
        self.link = link
        self.text = ''
        # links that does not contains strings in ignored_str list
        self.valid_links = []
        # Text from a tag specified by the user
        self.text_from_tag = None
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

        # Get the Response object
        try:
            self.html = requests.get(self.link, headers=headers)
        except ConnectionError as e:
            self.broken = True
            self.text = e
        except NewConnectionError as e:
            self.broken = True
            self.text = e
        except LocationParseError as e:
            self.broken = True
            self.text = e
        except InvalidURL as e:
            self.broken = True
            self.text = e


    def __repr__(self):
        return self.link


    def get_page_text(self, text_parcer, separator, text_tag, text_attr_name, text_attr_value):
        """
        Get pages text

        :param text_parcer: Define the format the text page will be parced
        :param separator: Character used to separate strings from different tags
        :param text_tag: Tag searched in page
        :param text_attr_name: Name of tags attribute
        :param text_attr_value: Value of tags attribute
        """

        if not self.broken:
            if text_parcer == 'first_parcer':
                text_parcer = FirstTextParcer(self.html, separator)

            self.text = text_parcer.get_text()
            self.html_status = text_parcer.get_status()
            if text_tag:
                self.text_from_tag = text_parcer.get_text_from_tag(text_tag, text_attr_name, text_attr_value)

            else:
                raise TypeError(f'text_parcer {text_parcer} not found')


    def get_page_links(self, homepage_url, link_parcer, ignored_strs, allowed_pages, link_tag, link_attr):
        """
        :param link_parcer: Define the format the link's page will be parced
        :param ignored_strs: List of strings that URLs must not contain
        :param allowed_pages: Allowed domains
        :param link_tag: Used if searching for links in specific tag
        :param link_attr: Tags attribute
        """

        if not self.broken:
            if link_parcer == 'first_parcer':
                link_parcer = FirstLinkParcer(self.html)
            else:
                raise TypeError(f'link_parcer {link_parcer} not found')

            self.all_page_links = link_parcer.get_all_links(link_tag, link_attr)
            self.valid_links = link_parcer.get_valid_links(homepage_url, ignored_strs, allowed_pages, link_tag, link_attr)


