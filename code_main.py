#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas

#Twitter API credentials
from credentials import * #Import twitter app access credentials


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(Consumer_API_Key, Consumer_API_Secret_Key)
	auth.set_access_token(Access_Token, Access_Token_Secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	#Getting list (indexed from 0) from https://twitter.com/screen_name/with_replies
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name=screen_name, count=200)
	
	print (new_tweets[11].id_str)
	print (new_tweets[11].created_at)
	print (new_tweets[11].text.encode("utf-8"))

	#EARLY TERMINATION FOR DEBUGGING
	return
	#Discoveries:
	# 1. Re-tweets begin with "b'RT "
	# 2. Emojiis come out as hex code
	# 3. Links seem to always be at the end
	# 4. All links start with "https://t.co/"
	#

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		#print ("getting tweets before " + oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		#print ("..."+ len(alltweets) +" tweets downloaded so far")
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#print (outtweets[1])

	tweetsDF = pandas.DataFrame({"id":[], "created_at":[], "text":[]})
	for tweet in outtweets:
		tweetsDF = tweetsDF.append(
			{"id": outtweets[1],
			"created_at": outtweets[2], 
			"text": outtweets[3],
			}, ignore_index=True
		) 


	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
		
	tweetsDF.to_csv ('%s_tweets.csv' % screen_name, index = None, header=True) 
	


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("subboyjj")