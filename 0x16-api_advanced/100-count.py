#!/usr/bin/python3
"""
Function to count words in all hot posts of a given Reddit subreddit.
"""
import requests


def count_words(subreddit, word_list, instances=None, after=None, count=0):
    """
    Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (dict): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
        count (int): The parameter of results matched thus far.
    """
    if instances is None:
        instances = {}
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return
    results = response.json()["data"]
    after = results.get("after")
    count += results.get("dist")
    for child in results.get("children"):
        title = child.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title and not any(ch in word for ch in [".", "!", "_"]):
                instances[word] = instances.get(word, 0) + title.count(word.lower())
    if not after:
        instances = sorted(instances.items(), key=lambda item: (-item[1], item[0]))
        for word, count in instances:
            print(f"{word}: {count}")
    else:
        count_words(subreddit, word_list, instances, after, count)
