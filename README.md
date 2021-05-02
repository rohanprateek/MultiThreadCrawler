# MultiThreadCrawler
Multi Threaded Crawler and Scraper

This is a Multi Threaded Web Crawler. It takes a base url and finds all the links embedded in the web page.
The root url is stored to ensure that the scraper does not end up on another website.

Since Python allows threading, we use it to speed up the scraping process. The urls found are passed on to a thread pool and 
results are collected through callback. 

A set of the pages scraped so far is maintained to prevent recursive behaviour.

Parsing is done using BeautifulSoup and the results are stored in a .txt file. Each web page results in a separate text file.
