"""
Mapping of hashtag to webhook URL
All lowercase hashtags
"""
hashtag_webhooks: dict[str, list[str]] = {
    "#hashtag": [
        # Server Name
        "https://discord.com/api/webhooks/server_id/webhook_id"
    ]
}

"""
Storage of tweet snowflakes/IDs
"""
FILE_NAME = "tweets.pickle"

"""
Max number of tweets to remember
"""
TWEET_MEMORY_LIMIT = 100

"""
Maximum number of hashtags before tweet is ignored
"""
HASHTAG_SPAM_LIMIT = 10

"""
Domain of nitter instance to use
"""
NITTER_INSTANCE = "nitter.net"

"""
Hashtags and cashtags to ignore
All lowercase, begin with -
"""
IGNORE_TAGS = [
    "-#bilibilicomics",
    "-#openseacollection",
    "-#openseanfts",
    "-#nftkid",
    "-#nftnews",
    "-#nftshills",
    "-#nft買います",
    "-#nftgiveaway",
    "-#nftgiveaways",
    "-#nftcommunity",
    "-#nftartists",
    "-#aiart",
    "-#nft",
    "-#crypto",
    "-#solana",
    "-#sol",
    "-#fidescoin",
    "-$fides",
]
