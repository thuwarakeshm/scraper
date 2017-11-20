import re
# import requests #If using python direct alls
from selenium import webdriver  # If using selenium webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_review(base_url, pages_count, PROXY='127.0.0.9666'):
    start_time = datetime.now()
    print(bcolors.OKBLUE + '{} : Initiate Amazon Scraper'.format(datetime.now()))

    # Chrome Options if using a selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(r'C:\Users\thuwarakeshm\Documents\scraping\Yelp\chromedriver.exe',
                              chrome_options=chrome_options)

    pages = range(1, pages_count + 1)
    splitted = re.split(r'paging_btm_', base_url)

    urls = [splitted[0] + re.sub(r'\d+', '{}'.format(page), splitted[1]) for page in pages]

    reviews = []

    for url in urls:
        print(bcolors.OKBLUE + '{0} : trying to fetch url {1}'.format(datetime.now(), url))
        try:

            # page = requests.get(url, proxies={'http': PROXY, 'https': PROXY}) #To be used with python direct calls
            driver.get(url)  # To be used with selenium webdriver

            print(bcolors.OKGREEN + '{0} : Successfully fetched url {1}'.format(datetime.now(), url))
        except:
            print(bcolors.FAIL + '{0} : Failed to fetched url {1}'.format(datetime.now(), url))
            break

        # soup = BeautifulSoup(page.content, 'html.parser') # To be used with python direct calls
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # To be used with selenium webdriver

        try:
            reviews_blocks = soup.find('div', id='cm_cr-review_list').find_all('div', attrs={'class': 'review'})
        except:
            print(bcolors.FAIL + '{0} : Could not extract reviews for url {1}'.format(datetime.now(), url))
            break

        for review in reviews_blocks:
            try:
                review_num = reviews.index(review) + 1
            except:
                review_num = 0
            try:
                rating = review.find('a').attrs['title'][0]
            except:
                print(bcolors.WARNING + '{0} : Could not extract rating for {2}th review of url {1}'.format(
                    datetime.now(), url, review_num))
                rating = 0
            try:
                review_title = review.find('a', attrs={'data-hook': 'review-title'}).text
            except:
                print(bcolors.WARNING + '{0} : Could not extract review_title for {2}th review of url {1}'.format(
                    datetime.now(), url, review_num))
                review_title = 'Unknown'
            try:
                author_name = review.find('a', attrs={'data-hook': "review-author"}).text
            except:
                print(bcolors.WARNING + '{0} : Could not extract author_name for {2}th review of url {1}'.format(
                    datetime.now(), url, review_num))
                author_name = 'Unknown'

            try:
                review_date = re.search(r'\w+ \d+, \d+',
                                        review.find('span', attrs={'data-hook': "review-date"}).text).group()
                # review_date = datetime(review_date)
            except:
                print(bcolors.WARNING + '{0} : Could not extract review_date for {2}th review of url {1}'.format(
                    datetime.now(), url, review_num))
                review_date = datetime(1990, 1, 1)
            try:
                review_text = review.find('span', attrs={'data-hook': "review-body"}).text
            except:
                print(bcolors.WARNING + '{0} : Could not extract review_text for {2}th review of url {1}'.format(
                    datetime.now(), url, review_num))
                review_text = 'Blank'

            reviews.append(
                {'rating': rating, 'review_title': review_title,
                 'author_name': author_name, 'review_date': review_date,
                 'review_text': review_text})
            # time.sleep(5)

    driver.close()

    return pd.DataFrame(reviews)
