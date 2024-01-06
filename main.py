"""
Nitter webhook bot
"""

import json
import pickle
from time import time, sleep
from httpx import get, post
from bs4 import BeautifulSoup
from config import hashtag_webhooks, FILE_NAME, TWEET_MEMORY_LIMIT, HASHTAG_SPAM_LIMIT, NITTER_INSTANCE, IGNORE_TAGS

NITTER_INSTANCE_SEARCH = f"https://{NITTER_INSTANCE}/search"
hashtags = set(hashtag_webhooks.keys())
COOKIES = {"replaceYouTube": "", "replaceReddit": "", "replaceTwitter": "twitter.com"}
IGNORE_SEARCH = " ".join(IGNORE_TAGS)
ART_SEARCH = " OR ".join(hashtags)
PARAMS = {
    "f": "tweets",
    "q": f"{IGNORE_SEARCH} {ART_SEARCH}",
    "f-media": "on",            # must include media
    "e-nativeretweets": "on",   # disable retweets
}
HEADERS = {
    "authority": NITTER_INSTANCE,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,id;q=0.8,ja;q=0.7",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def process(link=""):
    """
    Process link
    """
    api_url = f"https://api.fxtwitter.com{link}"
    req = get(url=api_url, headers=HEADERS)
    res = json.loads(req.text)
    tweet_body = res["tweet"]["text"]
    if tweet_body.count("\n #") > HASHTAG_SPAM_LIMIT:
        # skip spammer
        print(f"Likely spammer skipped: {res["tweet"]["author"]["screen_name"]}")
        return
    if "bilibilicomics" in tweet_body.lower():
        # skip bili spam
        print(f"Likely spammer skipped: {res["tweet"]["author"]["screen_name"]}")
        return
    print(f"Processing {res["tweet"]["id"]}")
    for hashtag in hashtags:
        if hashtag not in tweet_body.lower():
            continue
        if hashtag not in hashtag_webhooks:
            continue
        print(f"> Posting to server for {hashtag}")
        server_webhook_urls = hashtag_webhooks[hashtag]
        fx_url = res["tweet"]["url"].replace("//twitter.com", "//fxtwitter.com")
        webhook_data = {
            "content": fx_url,
        }
        for webhook_url in server_webhook_urls:
            req = post(webhook_url, data=json.dumps(webhook_data), headers={"Content-Type": "application/json"})
            ratelimit_remaining = int(req.headers.get("x-ratelimit-remaining"))
            ratelimited = ratelimit_remaining <= 1 # don't wait until 0
            if ratelimited:
                ratelimit_reset = float(req.headers.get("x-ratelimit-reset"))
                wait_seconds = ratelimit_reset - time() + 1
                print(f">> Out of quota: waiting {wait_seconds} seconds")
                sleep(wait_seconds)


def grab_tweets():
    """
    Grab the latest tweets
    """
    req = get(url=NITTER_INSTANCE_SEARCH, cookies=COOKIES, params=PARAMS, headers=HEADERS)
    soup = BeautifulSoup(req.text, "html.parser")

    found_new = False
    should_process = True
    links: dict[str, str] = {}

    try:
        with open(FILE_NAME, "rb") as file:
            links = pickle.load(file)
    except FileNotFoundError:
        # Either first run or data corrupted
        # Do _not_ spam the webhooks
        found_new = True
        should_process = False

    for link_tags in reversed(soup.find_all("a", "tweet-link")):
        link = link_tags.get("href").replace("#m", "")
        snowflake = link[link.rfind("/") + 1 :]
        if snowflake in links:
            print(f"Skipping old tweet {snowflake}")
        else:
            found_new = True
            links[snowflake] = link
            if should_process:
                process(link)

    snowflakes = sorted(links.keys())
    while len(snowflakes) > TWEET_MEMORY_LIMIT:
        snowflake_to_remove = snowflakes.pop(0)
        links.pop(snowflake_to_remove)

    if found_new:
        with open(FILE_NAME, "wb") as file:
            pickle.dump(links, file)


if __name__ == "__main__":
    grab_tweets()
