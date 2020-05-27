import json
import csv
from page import Page


class Crawler:
    def __init__(self, homepage_url, partial_file_name='', num_pages_file=0):
        """
        :param homepage_url: Homepage url
        :param partial_file_name: Name for the partial files saved during runtime
        :param num_pages_file: Number of pages in partial file
        """

        # If partial file is defined num_pages_file must be different than 0
        if partial_file_name and num_pages_file == 0:
            raise ValueError("num_pages_file must be > 0 if file_name is defined")

        self.homepage_url = homepage_url
        # All links form all pages
        self.all_crawer_links = []
        # Links of pages that didn't load
        self.broken_links = {}
        # All pages object
        self.pages_list = []
        self.partial_file_name = partial_file_name
        self.num_pages_file = int(num_pages_file)
        # Number of pages
        self.count = 0


    def crawl(self, text_parcer='first_parcer', link_parcer='first_parcer', ignored_strs=[],
              allowed_pages=[], separator=' | ', link_tag='', link_attr='', text_tag='', text_attr_name='',
              text_attr_value='', verbose=0, page='homepage'):
        """
        Recursive function to crawl a web page and create a Page object from valid links
        Append's all Page objects in self.pages_list

        :param text_parcer: Define the format the text page will be parced
        :param link_parcer: Define the format the link's page will be parced
        :param ignored_strs: List of strings that URLs must not contain
        :param allowed_pages: Allowed domains
        :param separator: Character used to separate strings from different tags
        :param link_tag: Used if searching for links in specific tag
        :param link_attr: Tags attribute
        :param text_tag: Tag searched in page
        :param text_attr_name: Name of tags attribute
        :param text_attr_value: Value of tags attribute
        :param page: Define the homepage as the first page to be crawled. Must be 'homepage'
        """

        # Runs at the first time to create the first Page object
        if page == 'homepage':
            self.count = 1
            page = Page(self.homepage_url)
            page.get_page_text(text_parcer, separator, text_tag, text_attr_name, text_attr_value)
            page.get_page_links(self.homepage_url, link_parcer, ignored_strs,
                                allowed_pages, link_tag, link_attr)
            page.depth = 0
            self.pages_list.append(page)

        # Verify if the links from the current page was already crawled
        new_links = []
        if page.valid_links:
            for link in page.valid_links:
                if link not in self.all_crawer_links:
                    # If it is a new link, append it to the list of all links in the home_page object
                    self.all_crawer_links.append(link)
                    # List of links to be crawled
                    new_links.append(link)

        self.print_verbose(verbose, page, new_links)

        # Return condition for the recursive function
        if len(new_links) == 0:
            return
        # Return condition to avoid recursion depth error
        if page.depth == 10:
            return

        # If there are links to be crawled
        else:
            for link in new_links:
                self.count += 1
                new_page = Page(link)
                new_page.get_page_text(text_parcer, separator, text_tag, text_attr_name, text_attr_value)
                new_page.get_page_links(self.homepage_url, link_parcer, ignored_strs,
                allowed_pages, link_tag, link_attr)
                new_page.depth = page.depth + 1
                self.pages_list.append(new_page)
                # Save the partial files
                if self.partial_file_name:
                    if len(self.pages_list) % self.num_pages_file == 0:
                        file_count = str(int(self.count / self.num_pages_file))
                        file_name = self.partial_file_name + '_' + file_count
                        self.to_json(file_name, file_count)
                # Recursive call
                self.crawl(new_page, text_parcer, link_parcer, ignored_strs, allowed_pages, separator,
                           link_tag, link_attr, text_tag, text_attr_name, text_attr_value, verbose)

            # Save the last partial file
            if self.num_pages_file != 0:
                if page.depth == 0:
                    file_count = str(int(len(self.pages_list) / self.num_pages_file) + 1)
                    file_name = self.partial_file_name + '_' + file_count
                    self.to_json(file_name, file_count)


    def to_json(self, file_name, file_count='', encoding='utf-8'):
        """
        :param file_name: json file name
        :param file_count: Utilized while saving parial files. Must be set to ''
        :return: a json file with pages object attributes
        """

        pages_attributes_list = []

        if file_name[-5:] != '.json':
            file_name = f'{file_name}.json'

        # Define the start and end in self.pages_list to create the partial .json file
        if file_count:
            start_page = (int(file_count) - 1) * self.num_pages_file
            if int(file_count) * self.num_pages_file > len(self.pages_list):
                end_page = len(self.pages_list)
            else:
                end_page = int(file_count) * self.num_pages_file
        else:
            start_page = 0
            end_page = len(self.pages_list) - 1

        file_path = f'crawled pages/{file_name}'

        for page in self.pages_list[start_page: end_page]:
            pages_attributes_list.append(
                {
                    'link': page.link,
                    'status': page.html_status,
                    'label': '',
                    'depth': page.depth,
                    'text': str(page.text),
                    'text_from_tag': page.text_from_tag
                })

        # TODO pages['broken links'] = self.broken_links

        pages_json = json.dumps({'pages': pages_attributes_list}, ensure_ascii=False).encode(encoding=encoding)

        with open(file_path, 'w') as f:
            f.write(pages_json.decode())


    def to_txt(self, file_name):
        """
        :param file_name: txt file name
        :return: txt file with pages object attributes
        """

        if file_name[-4:] != '.txt':
            file_name = f'{file_name}.txt'

        file_path = f'crawled pages/{file_name}'

        with open(file_path, 'w') as f:
            f.write('########## RESUME ##########\n\n')
            f.write(f'Number of pages: {len(self.pages_list)}\n\n')
            for page in self.pages_list:
                f.write(f'{page.link} - {page.html_status}\n')
            f.write('\n\n\n')

            f.write('########## PAGES CONTENT ##########')
            f.write('\n\n\n')
            for page in self.pages_list:
                f.write(f'{page.link}\n\n')
                f.write(f'Page depth: {page.depth}\n\n')
                f.write(f'Page status: {page.html_status}\n\n')
                if page.all_page_links:
                    f.write(f'Number of links: {len(page.all_page_links)}\n\n')
                    for link in page.all_page_links:
                        f.write(f'{link}\n')
                    f.write('\n')
                else:
                    f.write(f'Number of links: 0\n\n')
                f.write('Page text\n\n')
                f.write(f'{page.text}\n\n\n')
                f.write('-------------- NEW PAGE --------------\n\n')


    def to_csv(self, file_name):
        """
        :param file_name: csv file name
        :return: csv file
        """

        if file_name[-4:] != '.csv':
            file_name = f'{file_name}.csv'

        file_path = f'crawled pages/{file_name}'

        with open(file_path, 'w') as f:
            writer = csv.DictWriter(f, ['link', 'status', 'label', 'text'])
            writer.writeheader()
            for page in self.pages_list:
                dic = {'link': page.link, 'status': page.html_status, 'label': '?', 'text': page.text}
                writer.writerow(dic)


    def print_verbose(self, verbose, page, new_links):
        if verbose == 1:
            print(f'Page num: {self.count}')
            print(f'link da pagina: {page.link}')
            print(f'status: {page.html_status}')
            print(f'page depth: {page.depth}')
            print('\n-----------------------------------------\n')

        if verbose == 2:
            print(f'Page num: {self.count}')
            print(f'pages link: {page.link}')
            print(f'status: {page.html_status}')
            print(f'page depth: {page.depth}')
            print(f'pages valid links: {len(page.valid_links)}')
            print(f'page new links: {len(new_links)}')
            print(new_links)
            print('\n-----------------------------------------\n')