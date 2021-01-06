import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse
import snscrape.modules.twitter as sntwitter
import pandas as pd

app = Flask(__name__)
api = Api(app)

# Request Parsing setup
parser = reqparse.RequestParser()
parser.add_argument('data', required=True, help="Need tweet data to perform sentiment analysis!")
parser.add_argument('num_tweets', required=True, help="Enter the number of tweets you need")


class TweetScrapSNS(Resource):
    def get(self):
        args = parser.parse_args()
        query_args = str(args['data'])
        tweet_count = int(args['num_tweets'])
        return self.get_tweets(query_args, tweet_count)

    def get_tweets(self, query, max_tweets):
        tweets_list = list()
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i > max_tweets:
                break
            tweets_list.append({'date': str(tweet.date), 'id': str(tweet.id), 'content': str(tweet.content),
                                'username': str(tweet.username), 'tweet_url': tweet.url})
        return tweets_list

    def get_json_from_pd(self, tweets):
        tweets_df = pd.DataFrame(tweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
        return tweets_df.to_json()

    def convert_datetime_str(self, json_obj):
        if isinstance(json_obj, datetime.datetime):
            return json_obj.__str__()


api.add_resource(TweetScrapSNS, '/snsScrape')

if __name__ == '__main__':
    app.run()
