import re
from bs4 import BeautifulSoup as bs
from bs4. element import Tag

class FirstTextParcer:
    """
    Parser to get and format texts from pages
    """

    def __init__(self, html, separator):
        """
        :param html: Response object
        """

        self.html = html
        self.separator = separator

        # In case there are characters that BeautifulSoup can't parse
        try:
            self.soup = bs(self.html.text, 'html.parser')
        except TypeError:
            self.soup = bs('', 'html.parser')


    def get_text(self):
        """
        :param separator: Character used to separate strings from different tags
        :return: All text in the page
        """

        # In case some encoding error
        try:
            text = self.soup.get_text(self.separator)
        except UnicodeEncodeError:
            text = f'UnicodeEncodeError. Apparent encode: {self.html.apparent_encoding}'
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\t', ' ', text)
        text = re.sub(r' +', ' ', text)
        return text


    def get_status(self):
        """
        :return: Html status code form the page
        """

        # In case some encoding error
        try:
            html_status = self.html.status_code
        except UnicodeEncodeError:
            html_status = f'UnicodeEncodeError. Apparent encode: {self.html.apparent_encoding}'
        return html_status


    def get_text_from_tag(self, text_tag, text_attr_name, text_attr_value):
        """
        If the tag passed in text_tag is found in the html, return the text in the text_attr_name

        :param text_tag: Tag searched in page
        :param text_attr_name: Name of tags attribute
        :param text_attr_value: Value of tags attribute
        :return: Text within the tag
        """

        tags_text = ''
        # Get all the searched tag elements in the page
        tags = self.soup.find_all(text_tag, {text_attr_name: text_attr_value})
        for tag in tags:
            # Get the descendants from the tag
            tag_descendants = list(tag.descendants)
            for descendant in tag_descendants:
                if isinstance(descendant, Tag):
                    # Check if the element has descendants
                    if len(list(descendant.descendants)) == 1:
                        tags_text += descendant.text + ' '
            tags_text += self.separator
        return tags_text



