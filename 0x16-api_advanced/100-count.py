#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after=None, word_counts=None):
    """
    Queries the Reddit API recursively, parses the title of all hot articles,
    and prints a sorted count of given keywords.

    Args:
    subreddit (str): the subreddit to search in
    word_list (list): a list of keywords to count
    after (str): the id of the last post seen in the previous page of results
    word_counts (dict): a dictionary containing the counts of each keyword

    Returns:
    None
    """
    if word_counts is None:
        word_counts = {}

    if not word_list:
        # base case: nothing else to count
        sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print("{}: {}".format(word, count))
        return

    # get the next page of results from the Reddit API
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 100}
    if after:
        params["after"] = after
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        # if successful response, parse the results and update the word counts
        data = response.json()
        after = data["data"]["after"]
        for post in data["data"]["children"]:
            title = post["data"]["title"].lower()
            for word in word_list:
                count = title.count(word)
                if count > 0:
                    word_counts[word] = word_counts.get(word, 0) + count

        # call the function recursively with the remaining words and the next page of results
        count_words(subreddit, word_list[1:], after=after, word_counts=word_counts)
    else:
        # if unsuccessful response, print an error message and stop
        print("Error: subreddit not found or API error.")
        count_words("python", ["python", "java", "javascript", "ruby"])

