# EasyJapanese
Let's study Easy Japanese (やさしいにほんご) with NHK news web easy!  
This module helps you study intermediate level Japanese! This module mainly covers the topics listed below.  
- To get the URLs of the most recent easy Japanese news articles
- To extract the body texts of them
- To get the URL of the original articles of them
- To extract the original ones as well
- To concatenate all the above data
- To save them all as a csv file


Specifically, you can use this module to retrieve daily Easy Japanese(やさしいにほんご) news articles. Here's how it works. 
1. Prepare the dataframe that has the columns named {'Date', 'Easy URL', 'Easy article', 'Regular URL', 'Regular article'}
2. Edit the DRIVER_PATH (in easy.py), pd.read_csv() & pd.df.to_csv() (in complete.py) 
3. Run the code below
```
>>> from easyjapanese2 import EasyJapanese  
>>> EasyJapanese()  
```



I do not own any rights for the articles, nor take any responsibility caused 
by the use of this module. 

Have a great Easy Japanese (やさしいにほんご) life!
