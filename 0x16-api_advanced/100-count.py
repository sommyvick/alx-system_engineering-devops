#!/usr/bin/python3
"""Contains the count_words function"""
import requests
from collections import defaultdict


def count_words(subreddit, word_list, found_dict=defaultdict(int), after=None):
    '''Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        found_dict (obj): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
    '''
    user_agent = {'User-agent': 'test45'}
    url = 'http://www.reddit.com/r/{}/hot.json?limit=100'.format(subreddit)
    if after is not None:
        url += '&after={}'.format(after)
    with requests.get(url, headers=user_agent) as response:
        if response.status_code != 200:
            print('Error: {}'.format(response.status_code))
            return
        posts = response.json()['data']
        aft = posts['after']
        posts = posts['children']
        for post in posts:
            title = post['data']['title'].lower()
            for word in title.split(' '):
                if word in word_list:
                    found_dict[word.lower()] += 1
        if aft is not None:
            count_words(subreddit, word_list, found_dict, aft)
        else:
            for key, value in sorted(found_dict.items(), key=lambda item: item[1],
                                     reverse=True):
                print('{}: {}'.format(key, value))
