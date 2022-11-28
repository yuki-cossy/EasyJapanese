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

class Easy():
    def __init__(self):
        self.easy_urls = []
        self.easy_articles = []

    def get_urls_date(self):
        get_urls = Url()
        get_urls.startup()
        time.sleep(1)
        get_urls.get_latest()
        time.sleep(1)
        get_urls.parse_to_html()
        self.html = get_urls.html
        self.soup = get_urls.soup
        time.sleep(1)
        get_urls.get_raw()
        time.sleep(5)
        get_urls.shutdown()

        for url in get_urls.easy_urls:
            get_urls.get_urls(url)
            self.easy_urls = np.append(self.easy_urls, get_urls.easy_url)
        # get the date as well
        self.date = get_urls.date
        return self.date, self.easy_urls

    def get_articles(self, easy_urls):
        get_articles = Extract()
        get_articles.startup()
        try:
            # Most likely, .remove would be the culprit 
            # if there should be any exceptions.
            for url in tqdm(easy_urls):
                get_articles.open(url)
                time.sleep(1)
                get_articles.parse_to_html()
                time.sleep(1)
                get_articles.remove()
                time.sleep(1)
                article = get_articles\
                        .get_articles()
                self.easy_articles.append(article)
        except:
            print('An unexpected error has occured during obtaining the article.')
            print(f'article_raw: {get_articles.article_raw}\n')
            traceback.print_exc()
            self.easy_articles.append('Unexpected')
        finally:
            get_articles.shutdown()
        return self.easy_articles
    


class Url():
    def __init__(self):
        self.DRIVER_PATH = '/Users/domolm/.pyenv/versions/3.10.8/lib/python3.10/site-packages/selenium/chromedriver'
        self.service = fs.Service(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.options.add_argument('--window-size=1920,1200')
        # self.options.add_argument('--headless')
        self.easy_urls = []

    def startup(self):
        self.driver = webdriver.Chrome(options=self.options, service=self.service)
        self.BASE_URL = 'https://www3.nhk.or.jp/news/easy'
        self.driver.get(self.BASE_URL)

    def shutdown(self):
        self.driver.quit()

    def get_latest(self):
        self.driver.execute_script('window.scrollBy(0, 1000);')
        time.sleep(1)
        element = self.driver.find_element(
                By.XPATH, '//*[@id="easy-wrapper"]/div[2]/aside/section[2]/div[1]/a[1]'
                )
        element.click()

    def parse_to_html(self):
        self.html = self.driver.page_source.encode('utf-8')
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_raw(self):
        self.easy_urls_raw = self.soup.select('#js-archives-list > a')
        time.sleep(5)
        self.date = self.soup.select_one('#js-pager-date').text

    def get_urls(self, url):
        try:
            raw_url = url.get('href')
            self.easy_url = re.sub(r'^./', self.BASE_URL+'/', raw_url)
        except:
            print('An unexpected error has occured during obtaining the URL.')
            traceback.print_exc()
            self.easy_urls = 'Unexpected'
    

                
class Extract():
    def __init__(self):
        self.DRIVER_PATH = '/Users/domolm/.pyenv/versions/3.10.8/lib/python3.10/site-packages/selenium/chromedriver'
        self.service = fs.Service(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.options.add_argument('--window-size=1920,1200')
        self.options.add_argument('--headless')
        self.easy_articles = []

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
        for ruby in self.soup(['rt']):
            ruby.decompose()
            
    def get_articles(self):
        try:
            self.article_raw = self.soup.select_one('#js-article-body').text
            time.sleep(1)
            self.article_raw = re.sub('\n', '', self.article_raw)
            time.sleep(1)
            self.article = re.sub(' ', '', self.article_raw)
        except:
            self.easy_articles = 'Unexpected'
        return self.easy_articles




