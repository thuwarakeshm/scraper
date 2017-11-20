import re
import requests
import pandas as pd

from bs4 import BeautifulSoup


def get_review_details(review):
    return True


def get_auther_detail(review):
    return True


def get_review(base_url, pages_count, PROXY='127.0.0.9666'):
    pages = range(1, pages_count + 1)
    url_core = re.split(r'pageNumber=', base_url)[0]

    urls = [url_core + 'pageNumber={}'.format(page) for page in pages]

    [print(url) for url in urls]
    return True
