# hiodoshi

MIT Licensed VTuber art hashtag relay to discord webhook.
Coding style emphasizes clarity over "smart" python tricks whenever possible.
This is a python script which does the following:

1. Scrape a public nitter instance for the first 15 matches for any searched hashtag.
1. Checks if a specific tweet has already been processed and if not, prepare it for discord webhook send.
1. Checks the tweet contents against FxTwitter API.
1. Send to the matching hashtag-webhook pair.

No scheduling features are in place, it is expected to run this script via a cron job from the host environment.

Hashtags should be inserted in _all lowercase_.

## Configuration

A `config.py` file is expected. Copy from the `config.example.py` file and follow the instructions inside.
