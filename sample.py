# -*- coding: utf-8 -*-

import tweepy  # https://github.com/tweepy/tweepy
import json
import csv
import sys

# Twitter API credentials
consumer_key = "efsvkx52FjyFz9MgWQiJZ5YPs"
consumer_secret = "Kk2HlFUxekwU8aMFwRGP4GYgMaFdC3tU0iMOMvg1ZT51Wy8WQ4"
access_token = "982280284807843840-zkDknv8Dr0h7HoaGKy19xMjYxqKRFti"
access_secret = "di9eucNcbD37R432DAD2SHtE0fuQPEnogEqXUkrEMYVlK"

# Converts to Tweepy Status object to JSON and add that as json attribute
# Quick monkeypatch https://gist.github.com/misja/1183424
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # Writing into file
    out_file = open('%s_tweets.csv' % screen_name, 'wb')
    writer = csv.DictWriter(out_file, fieldnames=["id", "created_at", "text"], extrasaction='ignore',
                            delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writeheader()
    for tweet in new_tweets:
        t = json.loads(tweet.json)
        if "text" in t:
            t["text"] = t["text"].encode("utf-8")
        writer.writerow(t)

    # save the id of the oldest tweet less one
    oldest = new_tweets[-1].id - 1
    no_of_tweets = len(new_tweets)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("\t getting tweets before "+oldest) 

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        if new_tweets is None or len(new_tweets) == 0:
            continue

        # update the id of the oldest tweet less one
        oldest = new_tweets[-1].id - 1
        no_of_tweets += len(new_tweets)

        # Writing into file
        for tweet in new_tweets:
            t = json.loads(tweet.json)
            if "text" in t:
                t["text"] = t["text"].encode("utf-8")
            writer.writerow(t)

        print "\t ...%s tweets downloaded so far" % no_of_tweets


def usage():
    print "Usage :"
    print """\t python %s @twitter_handle""" % sys.argv[0]
    print "\t OR"
    print """\t python %s '["@twitter_handle","twitter_handle1", "@twitter_handle2"]'""" % sys.argv[0]

if __name__ == '__main__':
    # pass in the username or list of the account you want to download
    # Array of handles get from xpath in chrome $x("//span[contains(@class,'username js-action-profile-name')]/text()")
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    given_value = sys.argv[1]
    try:
        _handles_ = json.loads(given_value)
        for twitter_handle in _handles_:
            twitter_handle = twitter_handle.replace("@", "")
            print "Downloading Tweets of %s" % twitter_handle
            try:
                get_all_tweets(twitter_handle)
            except Exception, e:
                print "Error in Downloading %s, %s" % (twitter_handle, e)
                continue
    except Exception, e:
        # If not a JSON document
        print "Its not an JSON array. So trying ordinary way."
        given_value = given_value.replace("@", "")
        print "Downloading Tweets of %s" % given_value
        get_all_tweets(given_value)
    print Done
