import re
import time
import traceback

from tqdm import tqdm
import numpy as np
from selenium import webdriver # webdriver 操作一般用
from selenium.webdriver.chrome import service as fs # Chrome を driver として設定する用
from selenium.webdriver.chrome.options import Options # headless モードで作業する用
from selenium.webdriver.common.by import By # find_element() で参照したい位置を特定する用
from bs4 import BeautifulSoup


class Regular():
    def __init__(self, easy_urls):
        self.regular_urls = []
        self.regular_articles = []
        self.easy_urls = easy_urls

    def get_urls(self):
        get_urls = Url()
        get_urls.startup()
        for url in tqdm(self.easy_urls):
            get_urls.open(url)
            time.sleep(1)
            regular_url = get_urls\
                    .parse_to_html()\
                    .get_url()
            self.regular_urls.append(regular_url)
        get_urls.shutdown()
        return self.regular_urls
    
    def get_articles(self):
        get_articles = Extract()
        get_articles.startup()
        for url in tqdm(self.regular_urls):
            get_articles.open(url)
            time.sleep(1)
            get_articles.parse_to_html\
                .remove()\
                .get_articles()
        self.regular_articles = get_articles.regular_articles
        get_articles.shutdown()
        return self.regular_articles



    

class Url():
    def __init__(self):
        self.DRIVER_PATH = '/Users/domolm/.pyenv/versions/3.10.8/lib/python3.10/site-packages/selenium/chromedriver'
        self.service = fs.Service(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.options.add_argument('--window-size=1920,1200')
        # self.options.add_argument('--headless')
        self.regular_url = []

    def startup(self):
        self.driver = webdriver.Chrome(options=self.options, service=self.service)

    def open(self, url):
        self.driver.get(url)

    def shutdown(self):
        self.driver.quit()

    def parse_to_html(self):
        self.html = self.driver.page_source.encode('utf-8')
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_url(self):
        try:
            self.regular_url = self.soup.select_one('#js-regular-news').get('href')
        except:
            print('An unexpected error has occured during obtaining the URL.')
            traceback.print_exc()
            self.regular_url = 'Unexpected'
        return self.regular_url
    


class Extract():
    def __init__(self):
        self.DRIVER_PATH = '/Users/domolm/.pyenv/versions/3.10.8/lib/python3.10/site-packages/selenium/chromedriver'
        self.service = fs.Service(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.options.add_argument('--window-size=1920,1200')
        self.options.add_argument('--headless')
        self.regular_articles = []

    def startup(self):
        self.driver = webdriver.Chrome(options=self.options, service=self.service)

    def open(self, url):
        self.driver.get(url)

    def shutdown(self):
        self.driver.quit()

    def parse_to_html(self):
        self.html = self.driver.page_source.encode('utf-8')
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def remove(self):
        try:
            for nav in self.soup(['nav']):
                nav.decompose()
            for title in self.soup(['h2']):
                title.decompose()
            for fig in self.soup(['figcaption']):
                fig.decompose()
            for editor in self.soup.findAll(class_='content--editor-body'):
                editor.decompose()
        
        except:
            print('An expected error has occured during editing the html data.')
            traceback.print_exc()
            self.soup = None
    
    def get_articles(self):
        try:
            # this shoud be it if there happened an error in the extraction process.
            article = self.soup.find(class_='content--detail-body').text
            article = re.sub('\n', '', article)
            article = re.sub(' ', '', article)
            self.regular_articles.append(article)

        except:
            print('An expected error has occured during extracting the text.')
            traceback.print_exc()
            self.regular_articles.append('Unexpected')
            
