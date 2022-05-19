import numpy as np
import os

import re
import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer, word_tokenize
from nltk import download
from collections import Counter
from textblob import TextBlob

# download('punkt')
# download('stopwords')

def process_movie_reviews(movie):
    stopwords_english = stopwords.words('english')
    movies_clean = []
    movie_tokens = word_tokenize(movie)

    for word in movie_tokens:
        if(word not in stopwords_english and 
            word not in string.punctuation):
                movies_clean.append(word)

    return movies_clean


def process_tweet(tweet):
    '''
    Input:
        tweet: a string containing a tweet
    Output:
        tweets_clean: a list of words containing the processed tweet

    '''
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)
    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and  # remove stopwords
            word not in string.punctuation):  # remove punctuation
            # tweets_clean.append(word)
            stem_word = stemmer.stem(word)  # stemming word
            tweets_clean.append(stem_word)

    tweets_eng = []
    for word in tweets_clean:
        flag = True
        for i in word:
            if ord(i) >= 256:
                flag = False
                break
        if flag:
            tweets_eng.append(word)
    return tweets_eng


def count_words(tweet:list, freqs:dict, wordToTweet:dict):
    for word in tweet:
        if word in freqs:
            freqs[word] += 1
            wordToTweet[word].append(tweet)
        else:
            freqs[word] = 1
            wordToTweet[word] = [tweet]
    return freqs

def normalize(v):
    norm = np.power(np.sum(np.power(v,2)), 0.5)
    if norm == 0:
        return 0
    return v / norm



def vectorize(tweet, alphabet):
    v = np.zeros(len(alphabet))
    for i in range(len(alphabet)):
        if alphabet[i] in tweet:
            v[i] += 1
    return v

def closestCluster(vector, centroids):
    closest = -1
    minDist = 2**30
    for key in centroids:
        dist = np.linalg.norm(centroids[key] - vector)
        if dist < minDist:
            minDist = dist
            closest = key
    return closest


def assignToCluster(clusters, vectors, centroids):
    for i in range(len(vectors)):
        c = closestCluster(vectors[i], centroids)
        clusters[c].append(i)
    return clusters


def len_counts(clusters):
    lens = [len(cluster) for cluster in clusters.values()]
    return dict(Counter(lens))


def display_unique_tweets(tweets, cluster):
    c_tweets = [tweets[i] for i in cluster]
    for i in range(len(c_tweets)):
        if not c_tweets[i] in c_tweets[:i]:
            print(c_tweets[i])