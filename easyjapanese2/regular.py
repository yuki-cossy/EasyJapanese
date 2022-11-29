import re
import traceback

from selenium import webdriver # webdriver 操作一般用
from selenium.webdriver.chrome import service as fs # Chrome を driver として設定する用
from selenium.webdriver.chrome.options import Options # headless モードで作業する用
from selenium.webdriver.common.by import By # find_element() で参照したい位置を特定する用
from bs4 import BeautifulSoup


class Regular():
    def __init__(self):
        self.DRIVER_PATH = '/Users/domolm/.pyenv/versions/3.10.8/lib/python3.10/site-packages/selenium/chromedriver'
        self.service = fs.Service(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.options.add_argument('--window-size=1920,1200')
        # self.options.add_argument('--headless')

    # url := each element of easy_urls (url)
    # url := each element of regular_urls (extract)
    def start(self, url, url_or_article=True):
        self.driver = webdriver.Chrome(options=self.options, service=self.service)
        self.driver.get(url)
        print('Done starting up a new browser!')
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        if url_or_article:
            self.html_url = html 
            self.soup_url = soup
        else:
            self.html_article = html
            self.soup_article = soup
        print('Done parsing the JavaScript data to HTML!')

        print('All done start_url(). Hello!')


    def shutdown(self):
        self.driver.quit()
        print('All done shutdown(). Goodbye!')


    # soup := each element of self.soup_url
    def get_url(self, soup):
        try:
            reg_url = soup.select_one('#js-regular-news').get('href')
            print('Done retrieving the URL!')
        except:
            print('An unexpected error has occured during obtaining the URL.')
            traceback.print_exc()
            reg_url = 'Unexpected'
        return reg_url
    
    # soup := each element of self.soup_article
    def get_article(self, soup):
        try:
            for nav in soup(['nav']):
                nav.decompose()
            for title in soup(['h2']):
                title.decompose()
            for fig in soup(['figcaption']):
                fig.decompose()
            for editor in soup.findAll(class_='content--editor-body'):
                editor.decompose()
            print('Done removing the noise!')

        except:
            print('An expected error has occured during editing the html data.')
            traceback.print_exc()
            self.soup = None

        try:
            # this shoud be it if there happened an error in the extraction process.
            article = soup.find(class_='content--detail-body').text
            article = re.sub('\n', '', article)
            article = re.sub(' ', '', article)
            reg_article = article

        except:
            print('An expected error has occured during extracting the text.')
            traceback.print_exc()
            reg_article = 'Unexpected'
        return reg_article