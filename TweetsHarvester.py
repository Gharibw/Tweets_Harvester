# -*- coding: utf-8 -*-
'''
MIT License

Copyright (c) 2018 Gharib Gharibi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import csv

# http://www.tweepy.org/
import tweepy

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# Authentication
auther = tweepy.OAuthHandler(consumer_key, consumer_secret)
auther.set_access_token(access_key, access_secret)
api = tweepy.API(auther)

# returns number_of_tweets tweets from username
def get_profile_tweets(username, number_of_tweets):
    if '@' not in username[0]:
        username = '@'+username

    # twitter currently allows retrieving max 200 tweets per request
    if number_of_tweets > 200:
        # fix the following two lines insude the loop
        tweets = api.user_timeline(screen_name=username, count=200)
        number_of_tweets -= 200
        for i in range (number_of_tweets//200):
            last_tweet_id = tweets[-1].id
            tweets.extend(api.user_timeline(screen_name=username, count=200,
                                       max_id=last_tweet_id))
        last_tweet_id = tweets[-1].id
        tweets.extend(api.user_timeline(screen_name=username, 
                                        count=number_of_tweets%200, 
                                        max_id= last_tweet_id))
    else:
        tweets = api.user_timeline(screen_name=username, count=number_of_tweets)
        print(f'Retrieved {number_of_tweets} Tweets from {username}...')
        
    return tweets
      
# returns number_of_tweets tweets from username
def get_hastag_tweets(hashtag, number_of_tweets):
    if '#' not in hashtag[0]:
        hashtag = '#' + hashtag 
    tweets = []
    cursor = tweepy.Cursor(api.search, q=hashtag).items(number_of_tweets)
    # append only original tweets. No RT or Response
    for tweet in cursor:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            tweets.append(tweet)
            #print(tweet.text)
    print(f'Retrieved {number_of_tweets} Tweets from {hashtag}...')

    return tweets  
 
# prints the tweets to a .txt file
def tweets_to_txt(tweets, filename='tweets'):
    if '.txt' not in filename:
        filename += '.txt'
    # write to a new text file from the array of tweets
    with open(f'User_{filename}' , 'w+') as f:
        for tweet in tweets:
            f.write(tweet.text+'\n')
            
# print tweets to a .csv file
def tweets_to_csv(tweets, filename='tweets'): 
    if '.csv' not in filename:
        filename += '.csv'
    username = tweets[-1].user.screen_name
    
    # create array of tweets: username, tweet id, date/time, text
    tweets2csv = [[username, tweet.id_str, tweet.created_at, tweet.text] 
                            for tweet in tweets]
    
    #write to a new csv file from the array of tweets
    with open(f'User_{filename}' , 'w+') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["User", "Tweet ID", "Time", "Text"])  # write header
        writer.writerows(tweets2csv)

# specify a text to be removed from the tweets
def clean_tweets(tweets, trash_txt=''):
    clean_tweets = []
    for tweet in tweets:
        if trash_txt in tweet.text:
            clean_tweets.append(str(tweet.text).replace(trash_txt, ''))
    return clean_tweets



twts = get_hastag_tweets('#UMKC', 100)
                         
my_tweets = get_profile_tweets('Gharib_Gharibi', 321)
                                                          
tweets_to_txt(my_tweets, 'Gharibi_tweets')

tweets_to_csv(twts, 'UMKC_tweets')
