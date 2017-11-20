from Scrapers.AmazonScraper import get_review
import time

urls = [
    'https://www.amazon.com/Champion-Powerblend-Fleece-Pullover-Hoodie/product-reviews/B01HIURMZU/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=4']

for url in urls:
    df = get_review(url, 2, PROXY='127.0.0.1:10000')

    df.to_csv(r'C:\Users\thuwarakeshm\Documents\scraping\Yelp\data\dataframe.csv')

    if urls.index(url)/5 == 0:
        time.sleep(5)
