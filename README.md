# Twitter Sentiment Analysis

**Problem statement**: Can we determine who will become a customer based on user behavior?

For this project, I analyzed ~100K tweets collected both from the the Twitter API and through scraping. The data collected from each source were combined into a single dataframe to perform topic modeling annd sentiment analysis. This data includes:

- `tweet_id` - unique identifier of the tweet.
- `created_at` - timestamp marking when the tweet was published.
- `screen_name` - the screen name of the author of the tweet.
- `favorite_count` - the number of favorites the tweet has.
- `retweet_count` - the number of retweets the tweet has.
- `text`- the tweet contents.

## Files

[tweets_api.py](https://github.com/bakabrooks/twitter-nlp-sentiment/blob/master/tweets_api.py) and [tweets_scrape.py](https://github.com/bakabrooks/twitter-nlp-sentiment/blob/master/tweets_scrape.py) contain the scripts to pull Tweets from the Twitter API and scrape Tweets directly frmo Twitter, respectively.



[modeling.ipynb](https://github.com/bakabrooks/customer-purchase-prediction/blob/master/modeling.ipynb) shows the process of training various supervised learning models, tuning the models and evaluating their effectiveness.



The slide deck for this project can be found [here](https://github.com/bakabrooks/twitter-nlp-sentiment/blob/master/project-04-slides.pdf).

