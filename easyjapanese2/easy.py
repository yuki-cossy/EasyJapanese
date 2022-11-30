import re
import traceback

from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Easy():
    def __init__(self):
        self.DRIVER_PATH = 'filepath of your Chrome driver'
        self.service = fs.Service(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.options.add_argument('--window-size=1920,1200')
        self.options.add_argument('--headless')
        self.BASE_URL = 'https://www3.nhk.or.jp/news/easy'

        
    def start_url(self):    
        self.driver = webdriver.Chrome(options=self.options, service=self.service)
        self.driver.get(self.BASE_URL)
        print('Done starting up a new browser!')

        self.driver.execute_script('window.scrollBy(0, 1200);')
        element = self.driver.find_element(
                By.XPATH, '//*[@id="easy-wrapper"]/div[2]/aside/section[2]/div[1]/a[1]'
                )
        element.click()
        print('Done displyaing the list of the URLs')

        self.html_url = self.driver.page_source.encode('utf-8')
        self.soup_url = BeautifulSoup(self.html_url, 'html.parser')
        print('Done parsing the JavaScript data to HTML!')

        print('All done start_url(). Hello!')


    # url := each element of easy_urls
    def start_extract(self, url):
        self.driver = webdriver.Chrome(options=self.options, service=self.service)
        self.driver.get(url)
        print('Done starting up a new browswer!')

        self.html_article = self.driver.page_source.encode('utf-8')
        self.soup_article = BeautifulSoup(self.html_article, 'html.parser')
        print('Done parsing the JavaScript data to HTML!')

        print('All done start_extract(). Hello!')
        return self.soup_article


    def shutdown(self):
        self.driver.quit()
        print('All done shutdown(). Goodbye!')

    def get_raw_url_date(self):
        self.easy_urls_raw = self.soup_url.select('#js-archives-list > a')
        self.date = self.soup_url.select_one('#js-pager-date').text
        print('Done getting the raw text of URLs!')


    # url := each element of self.easy_urls_raw
    def get_url(self, url):
        try:
            raw_url = url.get('href')
            print('Done extracting the raw URL!')
            easy_url = re.sub(r'^./', self.BASE_URL+'/', raw_url)
            print('Done retrieving the URL!')
        except:
            print('An unexpected error has occured during obtaining the URL.')
            traceback.print_exc()
            easy_url = 'Unexpected'
        return easy_url


    # soup := each element of self.soup_article
    def get_article(self, soup):
        try:
            for ruby in soup(['rt']):
                ruby.decompose()
            print('Done removing the noise!')
            article_raw = soup.select_one('#js-article-body').text
            article_raw = re.sub('\n', '', article_raw)
            easy_article = re.sub(' ', '', article_raw) 

        except:
            print('An unexpected error has occured during obtaining the article.')
            print(f'soup: {soup}\n')
            traceback.print_exc()
            easy_article = 'Unexpected'
        return easy_article
    
