"""This file contains several functions to analyze subreddits and redditors"""

# library imports
import pandas as pd
import datetime as dt
import time
import praw
import config

# Utility functions used in the analyzing functions

def get_date(created):
    """takes a unix timestamp and converts it to date time"""
    return dt.datetime.fromtimestamp(created)

# function to convert dictionaries to dataframes for better readability
def dict_to_frame(red_dict):
    """takes a dictionary with a 'created' key and
    outpurs a datagframe with human readable time"""
    frame = pd.DataFrame(red_dict)
    if 'created' in red_dict:
        frame['created'] = frame['created'].apply(get_date)
    return frame

# a function that adds a timestamp to a string
def timestamper():
    """returns a string of a timestamp: year, month, day"""
    timestamp = dt.datetime.now()
    return str(dt.date(timestamp.year, timestamp.month, timestamp.day))

# Author analysis: all subreddit authors, most popular authors, author details¶

def author_comments(author):
    """takes a reddit user name and
    returns a dataframe of the 'new' the author's comments with score and creation date"""
    author_dict = {"body":[], "score":[], "created": []}
    for comment in reddit.redditor(author).comments.new(limit=None):
        author_dict['body'].append(comment.body),
        author_dict['score'].append(comment.score),
        author_dict['created'].append(comment.created)
    author_frame = pd.DataFrame(author_dict)
    author_frame['created'] = author_frame['created'].apply(get_date)
    return author_frame

# extracting all commentors of a 100 submission subset of a subreddit and their scores

def subreddit_authors(data_frame):
    """takes a dataframe of submissions (needs 'id') in a subreddit, iterates over all comments in all submission,
    outputs a dictionary of authors and their number of comment & their accumulated score"""
    author_dict = {}
    # iterating over all submission in a subreddit dataframe
    for sub in data_frame['id'][:1]:
        submission = reddit.submission(sub)
        # iterating over all comments within a submission
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if str(comment.author) in author_dict.keys():
                author_dict[str(comment.author)][0] += 1
                author_dict[str(comment.author)][1] += comment.score
            else:
                # creating a first entry if the author is not yet in the dict
                author_dict[str(comment.author)] = [1, comment.score]
    author_frame = pd.DataFrame(author_dict, index=['num_comments', 'sum_karma']).transpose()
    return author_frame

# a function to scrape the detailed data of the top 25 weekly redditors

def top_redditor_scraper(redditor_list):
    """Takes a list of usernames and outputs
    a dictionary with author key and cake day, link and comment karma"""
    detail_dict = {}
    for author in top_reds.index[:25]:
        try:
            created = get_date(reddit.redditor(author).created)
            link_karma = reddit.redditor(author).link_karma
            comment_karma = reddit.redditor(author).comment_karma
            detail_dict[author] = [created, link_karma, comment_karma]
        except:
            detail_dict[author] = [None, None, None]
    detail_frame = pd.DataFrame(detail_dict, index=['created', 'link_karma', 'comment_karma'])
    return detail_frame

# Subreddit & submission analysis: most popular submissions, all comments from an author

def subreddit_submissions(subreddit):
    """takes a subreddit and outputs a
    dataframe with the 100 hottest posts"""
    topics_dict = {"title":[], "author": [], "score":[], "id":[], "url":[], "comms_num": [], \
                "created": [], "body":[]}
    for submission in subreddit.hot(limit=100):
        topics_dict["title"].append(submission.title)
        topics_dict["author"].append(submission.author)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
    topic_frame = pd.DataFrame(topics_dict)
    return topic_frame

# creating a function that collects all comments from a submission

def submission_comments(submission):
    """takes a submission (reddit.submission) and outputs
    a dataframe of all comments in that submission"""
    comment_dict = {"body":[], "score":[], "author":[], "created": []}
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comment_dict['body'].append(comment.body),
        comment_dict['score'].append(comment.score),
        comment_dict['author'].append(comment.author),
        comment_dict['created'].append(comment.created)
    comment_frame = pd.DataFrame(comment_dict)
    comment_frame['created'] = comment_frame['created'].apply(get_date)
    comment_frame['author'] = comment_frame['author'].apply(lambda x: x.name)
    return comment_frame