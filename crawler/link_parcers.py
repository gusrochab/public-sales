from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs

class LinkParcer(ABC):
    """
    Abstract Parcer to get the links in page
    """

    def __init__(self, html):
        """
        :param html: Response object
        """
        self.html = html

        # In case there are characters that BeautifulSoup can't parse
        try:
            self.soup = bs(self.html.text, 'html.parser')
        except TypeError:
            self.soup = bs('', 'html.parser')


    def get_all_links(self, link_tag, link_attr):
        """
        Get all links in page. By default search for links in anchor tags. If link_tag and link_attr
        parameters are given, search into these html tags.

        :param link_tag: Used if searching for links in specific tag
        :param link_attr: Tags attribute
        :return: List with all links in anchor tags and link_tag tags
        """

        all_links = []
        anchor_tags = self.soup.find_all('a')
        # Get all links in anchor tags
        if anchor_tags:
            for anchor_tag in anchor_tags:
                all_links.append(str(anchor_tag.get('href')))
        custom_tags = self.soup.find_all(link_tag)
        # If link_tag and link_attr is defined, get all links in link_tag<link_attr>
        if custom_tags:
            for custom_tag in custom_tags:
                all_links.append(str(custom_tag.get(link_attr)))
        return all_links


    def is_valid_link(self, link, ignored_strs, allowed_pages):
        """
        Test if the link is a valid link. If the link is in the domain of allowed pages and if there is
        no ignored strings in the link string.

        :param link: Link to be analyzed
        :param ignored_strs: list of strings that the link must not contain
        :param allowed_pages: url that the link must contain
        :return: Bool if it`s valid or not
        """

        valid_link = True
        i = 0

        # Look if link is in allowed pages
        for page in allowed_pages:
            i += 1
            if page in link:
                break
            if i == len(allowed_pages):
                valid_link = False

        if valid_link:
            # Search if the link has ignored text in it
            for text in ignored_strs:
                if text in link.lower() or link == './':
                    valid_link = False
                    break
        return valid_link


    def padronize_link(self, link, homepage_url):
        """
        Return the link as an absolute path in a specified pattern.
        Deals with absolute and relative paths and paths with parameters in it (like paths with '?')

        :param link: Link to be padronized
        :param homepage_url: Homepages url
        :return: String with the absolute links path
        """

        url = self.html.url

        # If link in absolute path
        if 'http' in link:
            pass
        # If link is relative path
        else:
            # Padronize if link is relatve path
            if len(link) > 0 and link[0] == '/':
                while link[0] == '/':
                    link = link[1:]
                    if len(link) == 0:
                        break
                if '?' not in link:
                    link = f'{homepage_url}/{link}'

            # Handle relative links with '?'
            if '?' in link:
                # Handle if the link and the actual pages url has '?'
                if '?' in url:
                    question_mark_place = url.find('?')
                    link = url[:question_mark_place] + link
                else:
                    link = url + link
        return link


    def is_link_loop(self, link):
        """
        Check if the link refers to itself

        :param link: Link to be analyzed
        :return: Bool if the link is looping the same page
        """

        link_loop = False
        link_split = link.split('/')
        if len(link_split) > 1:
            if link_split[-1] == link_split[-2]:
                link_loop = True
        return link_loop


    @abstractmethod
    def get_valid_links(self, homepage_url, ignored_strs, allowed_pages, link_tag, link_attr):
        pass


class FirstLinkParcer(LinkParcer):
    """
    Format the text page will be parced
    """

    def __init__(self, html):
        """
        :param html: Response object
        """

        LinkParcer.__init__(self, html)


    def get_valid_links(self, homepage_url, ignored_strs, allowed_pages, link_tag, link_attr):
        """
        :param homepage_url: Homepages url
        :param ignored_strs: list of strings that URLs must not contain
        :param allowed_pages: alowed domains
        :param link_tag: Used if searching for links in specific tag
        :param link_attr: Tags attribute
        :return: List with all valid links
        """

        valid_links = []
        all_links = self.get_all_links(link_tag, link_attr)
        for link in all_links:
            # put the links in the same pattern
            link = self.padronize_link(link, homepage_url)
            # Check in the link is valid
            if self.is_valid_link(link, ignored_strs, allowed_pages):
                # Check if the page is referring to it self
                if not self.is_link_loop(link):
                    valid_links.append(link)
        return valid_links

