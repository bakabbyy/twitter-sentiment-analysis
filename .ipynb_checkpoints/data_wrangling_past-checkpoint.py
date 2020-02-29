from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

# create list of hashtags in which to query tweets
hashtags = ['samsunggalaxy', 'samsungunpacked', '#galaxyunpacked', '#galaxyS20',
            '#galaxyS10', '#galaxyS9', '#galaxyS8', '#unpacked2020', '#galaxyzflip',
            '#galaxyfold']

# create lists of start and end dates to collect tweets at each point of the event
begin_date = [dt.date(2020,1,28), dt.date(2019,2,6), dt.date(2018,2,11),
              dt.date(2017,3,15)]
end_date = [dt.date(2020,2,25), dt.date(2019,3,6), dt.date(2018,3,11),
            dt.date(2017,4,12)]
limit = 10000
lang = 'english'

all_frames = []
for i, hashtag in enumerate(hashtags):
    frames = []
    for x, date in enumerate(begin_date):
        try:
            tweets = query_tweets(hashtag, begindate=begin_date[x],
                                  enddate=end_date[x], limit=limit, lang=lang)
            df = pd.DataFrame(t.__dict__ for t in tweets)
            frames.append(df)
        except:
            pass
    all_frames.append(pd.concat(frames))
    print(f'Completed {i + 1} of {len(hashtags)} iterations...')

tweets_df = pd.concat(all_frames)
tweets_df.to_pickle("old_hashtag_tweets.pkl")