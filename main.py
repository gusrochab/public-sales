from crawler import *


sites_dict = {'brasilia_leiloes': 'https://www.brasilialeiloes.com.br'}

ignored_strs = ['.doc', '.docx', '.pdf', '.png', '.jpeg', '.jpg', '.peg', '/imprimir', 'mailto',
                'facebook', 'twitter', 'whatsapp', 'instagram', 'linkedin', 'cloudflare']
allowed_pages = ['https://www.brasilialeiloes.com.br']

for homepage_name, homepage_url in sites_dict.items():
    crawler = Crawler(homepage_url=homepage_url, partial_file_name=homepage_name, num_pages_file=500)
    crawler.crawl(text_parcer='first_parcer', link_parcer='first_parcer', ignored_strs=ignored_strs,
                  allowed_pages=allowed_pages, separator=' | ', link_tag='', link_attr='',
                  text_tag='div', text_attr_name='id', text_attr_value='l-lote-descricao', verbose=2)
    crawler.to_json(homepage_name)
    # crawler.to_txt(homepage_name)
