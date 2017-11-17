import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def author_details(ref):
    # This function extracts the author details given a block of review as a BeautifulSoup object
    # Return is a Dict of author details

    author_name = ref.find('a', attrs={'class': 'user-display-name js-analytics-click'}).text
    author_profile = ref.find_all('b')
    return {'author_name': author_name, 'author_location': author_profile[0].text,
            'author_friends': author_profile[1].text, 'author_reviews': author_profile[2].text}


def review_details(ref):
    # This function extracts all the review details  given review bloc as BeautifulSoup object
    # Return is a Dict review details

    review_date = re.search(r'\d+/\d+/\d+',
                            ref.find('div', attrs={'class': 'review-content'})
                            .find('span', attrs={'class': 'rating-qualifier'}).text).group()
    rating = ref.find('div', attrs={'class': 'review-content'}).find('div', attrs={'class': 'i-stars'}).attrs['title'][
        0]
    review = ref.find('p').text

    review_feedback_useful = 0
    review_feedback_funny = 0
    review_feedback_cool = 0

    try:
        review_feedback = ref.find('div', attrs={'class': 'rateReview'}).findChildren('a')[1:]
        review_feedback_useful = review_feedback[0].find('span', attrs={'class': 'count'}).text
        review_feedback_funny = review_feedback[1].find('span', attrs={'class': 'count'}).text
        review_feedback_cool = review_feedback[2].find('span', attrs={'class': 'count'}).text
    except:
        pass

    try:
        prev_review_date = re.search(r'\d+/\d+/\d+',
                                     ref.find('div', attrs={'class': 'previous-review'})
                                     .find('span', attrs={'class': 'rating-qualifier'}).text).group()
        prev_rating = \
            ref.find('div', attrs={'class': 'previous-review'}).find('div', attrs={'class': 'i-stars'}).attrs['title'][
                0]

        prev_review = ref.find('div', attrs={'class': 'previous-review'}).find('span', attr={
            'class': 'js-content-toggleable'}).text

    except:
        prev_review_date = '1/1/1990'
        prev_rating = 0

        prev_review = 'No Previous Review Available'

    return {'review_date': datetime.strptime(review_date, '%m/%d/%Y'), 'rating': rating, 'review': review,
            'review_feedback_useful': review_feedback_useful, 'review_feedback_funny': review_feedback_funny,
            'review_feedback_cool': review_feedback_cool,
            'prev_review_date': datetime.strptime(prev_review_date, '%m/%d/%Y'),
            'prev_rating': prev_rating, 'prev_review': prev_review}


def create_entry(ref):
    # This function extracts author details and review details from a given review block
    # Return is a pandas Series of author details with review information

    ref_auth = author_details(ref)
    ref_rev = review_details(ref)
    ref_auth.update(ref_rev)

    return pd.Series(ref_auth)


def get_business_details(soup):
    # This function extracts the business details for a given business
    # This function takes a BeautifulSoup object, a full Yelp page as in put
    # returns:
    #        A Pandas Series of basic business info
    #        A Pandas Series of available facilities
    #        A Pandas DataFrame of open hours

    business_name = str.strip(soup.find('h1', attrs={'class': 'biz-page-title'}).text)

    try:
        business_type = soup.find('span', attrs={'class': 'category-str-list'}).find('a').text
    except:
        business_type = 'Not Available'

    try:
        business_address = str.strip(soup.find('address').text)
    except:
        business_address = 'Not Available'

    try:
        business_phone = str.strip(soup.find('span', attrs={'class': 'biz-phone'}).text)
    except:
        business_phone = 'Not Available'

    try:
        business_web = str.strip(soup.find('span', attrs={'class': 'biz-website js-add-url-tagging'}).find('a').text)
    except:
        business_web = 'Not Available'

    hours_table = soup.find('table', attrs={'class': 'table table-simple hours-table'})
    days = [row.text for row in hours_table.findChildren('th')]

    times = re.findall(r'\d+:\d+ [ap]m', str(hours_table.find_all('td')))
    open_hours = [(times[i], times[i + 1]) for i in range(0, len(times), 2)]

    try:
        business_hours = [{'day': days[i], 'open_at': open_hours[i][0], 'close_at': open_hours[i][1]} for i in
                          range(len(days))]
    except:
        business_hours = {}

    try:
        other_serv = soup.find('div', attrs={'class': 'ywidget menu-preview js-menu-preview'}).find_next_sibling()
        servs = [str.strip(serv.text) for serv in other_serv.find_all('dt')]
        avaiabiity = [str.strip(serv.text) for serv in other_serv.find_all('dd')]
        services = dict(zip(servs, avaiabiity))
    except:
        services = {}

    return pd.Series(
        {'business_name': business_name, 'business_address': business_address, 'business_type': business_type,
         'business_phone': business_phone, 'business_web': business_web}), pd.Series(services), pd.DataFrame(
        {'business_hours': business_hours})


def get_data(base_url, pages_count=0, PROXY='127.0.0.1:9666'):
    # This function takes base_url and pages_count as parameters and fetch data from each review page of the url
    # Proxy address can be given as an optional parameter. 127.0.0.1:9666 will be used as default
    # Returns:
    #        A Pandas DataFrame of reviews
    #        A Pandas Series of basic business info
    #        A Pandas Series of available facilities
    #        A Pandas DataFrame of open hours

    process_start_time = datetime.now()
    print('{0} : Initiating Yelp scraper'.format(str(process_start_time)))

    pages = 100 if not pages_count else pages_count

    page_starts = range(0, pages * 20, 20)
    urls = [base_url + '?start={0}'.format(x) for x in page_starts]
    df = pd.DataFrame()

    for url in urls:

        if urls.index(url) == int(pages):
            break

        print(bcolors.OKBLUE + '{1} : Trying to fetch page {0}'.format(url, str(datetime.now())))
        page = requests.get(url, proxies={'http': PROXY, 'https': PROXY})
        print(bcolors.OKGREEN + '{1} : Fetching page {0} completed'.format(url, str(datetime.now())))
        soup = BeautifulSoup(page.content, 'html.parser')

        if not pages_count:
            try:
                pages = str.split(str.strip(soup.find('div', attrs={'class': 'page-of-pages'}).text), ' ')[-1]
            except:
                break

        try:
            reviews_blocks = soup.find_all('ul', attrs={'class': 'ylist ylist-bordered reviews'})[0].find_all('div',
                                                                                                              attrs={
                                                                                                                  'class': 'review review--with-sidebar'})
            df = pd.concat([df, pd.DataFrame([create_entry(block) for block in reviews_blocks])], ignore_index=True)
            print(bcolors.OKGREEN + '{1} : Processing page {0} completed. Results appended to DataFrame'.format(url,
                                                                                                                str(
                                                                                                                    datetime.now())))
        except:
            print(bcolors.WARNING + '{0} : Extracting review blocks failed for url : {1}!'.format(str(datetime.now()),
                                                                                                  url))

    print(bcolors.OKBLUE + '{0} : Trying to fetch business_details'.format(str(datetime.now())))
    (info, options, open_hours) = get_business_details(BeautifulSoup(page.content, 'html.parser'))
    print(bcolors.OKGREEN + '{0} : Fetching business_details is completed'.format(str(datetime.now())))

    process_duration = datetime.now() - process_start_time
    hours, mins, seconds = int(process_duration.seconds / 3600), int((process_duration.seconds % 3600) / 60), int(
        (process_duration.seconds % 3600) % 60)
    print(bcolors.OKGREEN + '{0} : {1} pages scraped successfully in {2} hours, {3} minuets {4} seconds'.format(
        str(datetime.now()),
        pages_count, hours, mins,
        seconds))
    print('{0} : Process Successfully completed Completed!'.format(str(datetime.now())))

    for i in info.index:
        df[i] = info[i]

    for i in options.index:
        df[i] = options[i]

    return df, info, options, open_hours
