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
import re

# The very first thing we do is give a useful error if someone is
# running this code under Python 2.
if sys.version_info.major < 3:
    raise ImportError('You are trying to use a Python 3-specific version of Easy Japanese under Python 2. This will not work. Please do something on it lol')

from easyjapanese.easy import Easy
from easyjapanese.regular import Regular
from easyjapanese.complete import Complete

def EasyJapanese():
    easy = Easy()
    old_date, easy_urls = easy.get_urls_date()
    easy_articles = easy.get_articles(easy_urls)
    
    regular = Regular(easy_urls)
    regular_urls = regular.get_urls()
    regular_articles = regular.get_articles()

    complete = Complete(
            easy_urls, easy_articles,
            regular_urls, regular_articles,
            old_date
            )
    complete.make_df()
    df_new = complete.concat()
    return df_new
