from Scrapers.AmazonScraper import get_review

urls = [
    '# https://www.amazon.com/Champion-Powerblend-Fleece-Pullover-Hoodie/product-reviews/B01HIURMZU/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=4']

for url in urls:
    print(get_review(url, 2))

