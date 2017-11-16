from datetime import datetime

from Scrapers.YelpScrapper import get_data

urls = ['https://www.yelp.com/biz/corkys-ribs-and-bbq-memphis-2',
        'https://www.yelp.com/biz/corkys-bar-b-q-collierville',
        'https://www.yelp.com/biz/corkys-bar-b-q-memphis',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-memphis-3',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-olive-branch',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-little-rock-2',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-north-little-rock',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-pigeon-forge']

for url in urls:
    process_start_time = datetime.now()

    (df, info, options, open_hours) = get_data(url, 1)

    PATH = r'~\projects\scraper\data\{0}-{1}'.format(info.business_name, urls.index(url))
    df.to_csv(PATH + '_review')
    info.to_csv(PATH + '_info')
    options.to_csv(PATH + '_options')
    open_hours.to_csv(PATH + '_open_hours')

process_duration = datetime.now() - process_start_time
(hours, mins, seconds) = int(process_duration.seconds / 3600), int((process_duration.seconds % 3600) / 60), int(
    (process_duration.seconds % 3600) % 60)
print('{0} : Whole Process finished successfully in {2} hours, {3} mins {4} seconds'.format(str(datetime.now()), 'a',
                                                                                            hours, mins, seconds))
