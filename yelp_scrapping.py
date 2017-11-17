from datetime import datetime

from Scrapers.YelpScrapper import get_data

# Corky's ribs bbq
urls = ['https://www.yelp.com/biz/corkys-bar-b-q-collierville',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-memphis-2',
        'https://www.yelp.com/biz/corkys-bar-b-q-memphis',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-memphis-3',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-olive-branch',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-little-rock-2',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-north-little-rock',
        'https://www.yelp.com/biz/corkys-ribs-and-bbq-pigeon-forge']

# priery's Competitors
# urls = ['https://www.yelp.com/biz/goldfish-swim-school-burr-ridge-burr-ridge-5',
#         'https://www.yelp.com/biz/goldfish-swim-school-roscoe-village-chicago',
#         'https://www.yelp.com/biz/goldfish-swim-school-glen-ellyn-glen-ellyn-2',
#         'https://www.yelp.com/biz/british-swim-school-downtown-chicago-chicago',
#         'https://www.yelp.com/biz/british-swim-school-oak-brook-3',
#         'https://www.yelp.com/biz/british-swim-school-southlands-chicago-tinley-park?osq=British+Swim+School',
#         'https://www.yelp.com/biz/chicago-blue-dolphins-chicago',
#         'https://www.yelp.com/biz/go-swim-chicago-chicago',
#         'https://www.yelp.com/biz/swim-in-chicago-chicago-3',
#         'https://www.yelp.com/biz/big-blue-swim-school-niles-niles']

for url in urls:
    process_start_time = datetime.now()

    # (df, info, options, open_hours) = get_data(url, 1)
    (df, info, options, open_hours) = get_data(url, PROXY='127.0.0.1:4653')

    PATH = r'C:\projects\YelpScrapper\data\{0}-{1}'.format(info.business_name, urls.index(url))
    df.to_csv(PATH + '_review.csv')
    # info.to_csv(PATH + '_info')
    # options.to_csv(PATH + '_options')
    # open_hours.to_csv(PATH + '_open_hours')

process_duration = datetime.now() - process_start_time
(hours, mins, seconds) = int(process_duration.seconds / 3600), int((process_duration.seconds % 3600) / 60), int(
    (process_duration.seconds % 3600) % 60)
print('{0} : Whole Process finished successfully in {2} hours, {3} mins {4} seconds'.format(str(datetime.now()), 'a',
                                                                                            hours, mins, seconds))
