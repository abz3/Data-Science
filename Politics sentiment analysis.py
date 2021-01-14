import praw
import pandas as pd
import datetime as dt
from textblob import TextBlob
import nltk
from newspaper import Article
from newspaper import Config
import matplotlib.pyplot as plt

# All the neccesary data collection and setup
reddit = praw.Reddit(client_id='RyRae4TokF6AeQ', \
                     client_secret='I0mM_Y-lQT2lHihwvvOit_nCNto', \
                     user_agent='wsb', \
                     username='BuffaloExisting', \
                     password='JustinPfister2')

politics = reddit.subreddit('politics')

for submission in politics.hot(limit=1):
    print(submission.title, submission.id)

topics_dict = {"title": [], "score": [], "id": [], "url": [], "created": [], "body": []}

for submission in politics.hot(limit=100):
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)
print(topics_data)

nltk.download('punkt')

actual_list = []
for index, row in topics_data.iterrows():
    if 'reddit' not in row['url']:
        actual_list.append(index)


def subjectivity():
    """
    Graphs the posts based on the relationship between subjectivity and popularity
    :return: a graph with the x axis being the subjectivity value, and y axis being upvotes
    """
    scores = []
    for index, row in topics_data.iterrows():
        if index in actual_list:
            scores.append(row['score'])

    subs = []
    for index, row in topics_data.iterrows():
        if index in actual_list:
            url = row['url']
        if 'newsweek' or 'democracynow' in url:
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            config = Config()
            config.browser_user_agent = user_agent
            article = Article(url, config=config)
        else:
            article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text = article.summary
        obj = TextBlob(text)
        subjectivity = obj.sentiment.subjectivity
        subs.append(subjectivity)

        plt.figure(figsize=(50, 10))
        plt.scatter(subs, scores)
        plt.xlabel('Subjectivity')
        plt.ylabel('Score')
        plt.title('Posts in r/politics')
        plt.show()


def sentiment():
    """
    Graphs the posts based on the relationship between sentiment and popularity
    :return: a graph with the x axis being the sentiment value, and y axis being upvotes
    """
    scores = []
    for index, row in topics_data.iterrows():
        if index in actual_list:
            scores.append(row['score'])

    sentiments = []
    for index, row in topics_data.iterrows():
        if index in actual_list:
            url = row['url']
        if 'newsweek' or 'democracynow' in url:
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            config = Config()
            config.browser_user_agent = user_agent
            article = Article(url, config=config)
        else:
            article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text = article.summary
        obj = TextBlob(text)
        subjectivity = obj.sentiment.subjectivity
        sentiment = obj.sentiment.polarity
        sentiments.append(sentiment)

        plt.figure(figsize=(50, 10))
        plt.scatter(sentiments, scores)
        plt.xlabel('Sentiments')
        plt.ylabel('Score')
        plt.title('Posts in r/politics')
        plt.show()


def averages():
    """
    Finds the average sentiment & subjectivity values of the articles
    """
    totalsubs = 0
    for sub in subs:
        totalsubs += sub
    avgsubs = totalsubs / len(subs)

    totalsent = 0
    for sent in sentiments:
        totalsent += sent
    avgsent = totalsent / len(sentiments)
    print('The average subjectivity is: ' + str(avgsubs))
    print('The average sentiment is: ' + str(avgsent))
