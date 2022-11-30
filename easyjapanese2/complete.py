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
        self.SAVEPATH = 'set the filepath on your own, where you save the final output data.'
        self.df_old = pd.read_csv(self.SAVEPATH)
        

    def make_df(self):
        self.input_length_test()
        new_date = self.get_date()
        self.df = pd.DataFrame({
            'Date': new_date,
            'Easy URL': self.easy_urls,
            'Easy article': self.easy_articles,
            'Regular URL': self.regular_urls,
            'Regular article': self.regular_articles
        })
        
        
    def concat(self):
        self.df_piled = pd.concat([self.df, self.df_old])
        self.df_piled['Date'] = pd.to_datetime(self.df_piled['Date'])
        self.df_piled.to_csv(self.SAVEPATH, index=False)
        return self.df_piled
    

    
    def input_length_test(self):
        try:
            if ~(
                len(self.easy_urls) == len(self.easy_articles)\
                == len(self.regular_urls) == len(self.regular_articles)
            ):
                raise LengthError('An unexpected error has occured with some or all of the four inputs.')
        except LengthError:
            print(traceback.print_exc())

    def get_date(self):
        old_date = datetime.datetime.strptime(
            self.df_old['Date'][0], '%Y-%m-%d'
            )
        new_date_raw = datetime.datetime.strptime(
                self.date, '%m月%d日'
                )
        if (old_date.month==12) & (new_date_raw.month==1):
            new_year = old_date.year + 1
        else:
            new_year = old_date.year
        self.date = datetime.datetime(
                new_year, new_date_raw.month, new_date_raw.day)
        return self.date



class LengthError(Exception):
    """This error notifies the unequal length of the inputs; URLs and articles.
    """
    pass