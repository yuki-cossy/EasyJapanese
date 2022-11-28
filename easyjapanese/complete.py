import traceback
import datetime

import pandas as pd


class Complete():
    def __init__(self, easy_urls, easy_articles,
                regular_urls, regular_articles, date):
        self.easy_urls = easy_urls
        self.easy_articles = easy_articles
        self.regular_urls = regular_urls
        self.regular_articles = regular_articles
        self.date = date

    def make_df(self):
        self.test()
        new_date = self.date()
        self.df = pd.DataFrame({
            'Date': new_date,
            'Easy URL': self.easy_urls,
            'Easy article': self.easy_articles,
            'Regular URL': self.regular_urls,
            'Regular article': self.regular_articles
        })
        
    def concat(self):
        df_old = pd.read_csv('../data/data_pool.csv')
        self.df_piled = pd.concat([self.df, df_old])
        df_piled.to_csv('../data/data_pool.csv', index=False)
        return self.df_piled
    
    def test(self):
        try:
            if ~(
                len(self.easy_urls) == len(self.easy_articles)\
                == len(self.regular_urls) == len(self.regular_articles)
            ):
                raise LengthError('Something is wrong with any or all of the four inputs.')
        except LengthError:
            print(traceback.print_exc())

    def date(self):
        df = pd.read_csv('../data/data_pool.csv')
        old_date = datetime.datetime.strptime(
            df['Date'][0], '%Y-%m-%d'
            )
        new_date_raw = datetime.datetime.strptime(
                self.date, '%m年%d日'
                )
        if (old_date.month==12) & (new_date_raw.month==1):
            new_year = old_date.year + 1
        else:
            new_year = old_date.year
        self.date = datetime.datetime(
                new_year, new_date_raw.month, new_date_raw.day)
        return self.date



class LengthError(Exception):
    """This error notifies the unequal length of the URLs and articles.
    """
    pass