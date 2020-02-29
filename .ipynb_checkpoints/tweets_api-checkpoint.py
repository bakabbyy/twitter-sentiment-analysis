import json
import tweepy
from twitter_creds import *

# pass credentials to authorize Twitter app
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,
                 parser=tweepy.parsers.JSONParser(),
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


def get_user_tweets(screen_name):
    """
    Returns ~3000 of the most recent tweets of a specific user and dumps into a
    JSON file.
    ---
    :param screen_name: User name of the Twitter account to fetch tweets
    :return: JSON file export of tweet contents and metadata
    """

    all_tweets = []

    # make initial request for most recent tweets
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1]['id'] - 1

    # continue where from the last id until there are no tweets left to collect
    while len(new_tweets) > 0:
        print(f'getting tweets before {oldest}s')

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1]['id'] - 1

        print(f'...{len(all_tweets)}s tweets downloaded so far')

    # extract necessary fields from tweet metadata
    user_tweets = [{'id_str': tweet['id_str'], 'created_at': tweet['created_at'],
                    'screen_name': tweet['user']['screen_name'],
                    'in_reply_to_status_id_str': tweet['in_reply_to_status_id_str'],
                    'in_reply_to_screen_name': tweet['in_reply_to_screen_name'],
                    'favorite_count': tweet['favorite_count'], 'retweet_count': tweet['retweet_count'],
                    'text': tweet['text']} for tweet in all_tweets]

    with open(f'data/user_tweets/{screen_name}s_tweets.json', 'w') as fout:
        json.dump(user_tweets, fout)


def get_hashtag_tweets(hashtag, date_since):
    """
    Returns ~3000 of the most recent tweets including the specified hashtag.
    ---
    :param hashtag: The hashtag to include in all returned tweets
    :return: JSON file export of tweet contents and metadata
    """

    all_tweets = []

    # make initial request for most recent tweets
    new_tweets = api.search(q=hashtag, lang="en", since=date_since, count=100)['statuses']

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1]['id'] - 1

    # continue where from the last id until there are no tweets left to collect
    while len(new_tweets) > 0:
        print(f'getting tweets before {oldest}s')

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.search(q=hashtag, lang="en", since=date_since,
                                count=200, max_id=oldest)['statuses']

        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1]['id'] - 1

        print(f'...{len(all_tweets)}s tweets downloaded so far')

    # extract necessary fields from tweet metadata
    hashtag_tweets = [{'id_str': tweet['id_str'], 'created_at': tweet['created_at'],
                       'screen_name': tweet['user']['screen_name'],
                       'in_reply_to_status_id_str': tweet['in_reply_to_status_id_str'],
                       'in_reply_to_screen_name': tweet['in_reply_to_screen_name'],
                       'favorite_count': tweet['favorite_count'], 'retweet_count': tweet['retweet_count'],
                       'text': tweet['text']} for tweet in all_tweets]

    with open(f'data/hashtag_tweets/{hashtag}_tweets.json', 'w') as fout:
        json.dump(hashtag_tweets, fout)


if __name__ == '__main__':
    # create a loop to get the tweets of all accounts
    # Apple does not have any tweets, do not include
    screen_names = ['SamsungMobile', 'UnboxTherapy', 'MKBHD',
                    'LinusTech', 'UrAvgConsumer', 'Jon4Lakers', 'tldtoday',
                    'iAm_erica', 'austinnotduncan', 'ijustine', 'CNET',
                    'DetroitBORG', 'SuperSaf', 'arstechnica', 'TechCrunch',
                    'engadget', 'thenextweb', 'wired', 'Gizmodo', 'VentureBeat',
                    'verge', 'ForbesTech']

    for screen_name in screen_names:
        get_user_tweets(screen_name)

    # create a loop to get the tweets of all hashtags
    hashtags = ['#unpacked', '#galaxyunpacked', '#galaxyS20', 'unpacked2020',
                '#galaxyzflip']

    for hashtag in hashtags:
        get_hashtag_tweets(hashtag + ' -filter:retweets', date_since='2020-02-01')