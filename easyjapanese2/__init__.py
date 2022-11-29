"""Let's study Easy Japanese (やさしいにほんご) with NHK news web easy!

This module mainly does the functions below.
- To get the URLs of the easy Japanese news articles
- To extract the body texts of them
- To get the URL of the original articles of them
- To extract the original ones as well
- To concatenate all the above data
- To fill up saves NaNs
- To save them all as a csv file

I do not own any rights for the articles, nor take any responsibility caused 
by the use of this module. 

Have a great Easy Japanese (やさしいにほんご) life!
"""
__all__ = ['easy', 'regular', 'complete']

import sys
import time

from tqdm import tqdm

from easyjapanese2.easy import Easy
from easyjapanese2.regular import Regular
from easyjapanese2.complete import Complete

# The very first thing we do is give a useful error if someone is
# running this code under Python 2.
if sys.version_info.major < 3:
    raise ImportError('You are trying to use a Python 3-specific version of Easy Japanese under Python 2. This will not work. Please do something on it lol')



def EasyJapanese():
    easy_urls = []
    easy_articles = []
    soups_easy = []
    regular_urls = []
    regular_articles = []
    soups_regular_url = []
    soups_regular_article = []

    e = Easy()
    # easy_urls
    e.start_url()
    e.get_raw_url_date()
    for url in tqdm(e.easy_urls_raw):
        easy_url = e.get_url(url)
        easy_urls.append(easy_url)
    print('Done retrieving the URLs!')
    print('All done with easy_urls! Great job!')
    e.shutdown()

    # easy_articles
    for url in tqdm(easy_urls):
        soup = e.start_extract(url)
        soups_easy.append(soup)
        time.sleep(1)
    for soup in tqdm(soups_easy):
        easy_article = e.get_article(soup)
        easy_articles.append(easy_article)
    print('Done retrieving the articles!')
    print('All done with easy_articles! Great job!')
    e.shutdown()

    # new_date
    new_date = e.date

    r = Regular()
    # regular_urls
    for url in tqdm(easy_urls):
        r.start(url, url_or_article=True)
        soups_regular_url.append(r.soup_url)
        time.sleep(1)
    for soup in tqdm(soups_regular_url):
        reg_url = r.get_url(soup)
        regular_urls.append(reg_url)
    r.shutdown()

    # regular_articles
    for url in tqdm(regular_urls):
        r.start(url, url_or_article=False)
        soups_regular_article.append(r.soup_article)
        time.sleep(1)
    for article in tqdm(soups_regular_article):
        reg_article = r.get_article(article)
        regular_articles.append(reg_article)
    r.shutdown()



    c = Complete(
            easy_urls, easy_articles,
            regular_urls, regular_articles,
            new_date
            )
    c.make_df()
    df_new = c.concat()
    return df_new
