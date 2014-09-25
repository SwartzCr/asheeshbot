from twython import Twython
import json

def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def load():
    with open("queue.json", 'r') as f:
        queue = json.load(f)
    with open("info.json", 'r') as fi:
        info = json.load(fi)
    return queue, info

def dump(queue, info):
    with open("queue.json", 'w') as f:
        json.dump(queue, f)
    with open("info.json", 'w') as fi:
        json.dump(info, fi)

def respond(twitter, top_tweet):
    name = top_tweet["user"]["screen_name"]
    twitter.update_status(status="@%s Oh, I can believe it!" %(name), in_reply_to_status_id=top_tweet["id"])


def main():
    twitter = auth()
    queue, info = load()
    tweets = twitter.search(q="I can't believe", result_type="recent", since_id=info["sinceid"], count='100')
    info["sinceid"] = tweets["search_metadata"]["max_id"]
    triggers = ("Can't believe", "can't believe", "I can't believe")
    to_add = [tweet for tweet in tweets["statuses"] if not tweet["retweeted"] and not tweet.has_key("retweeted_status")]
    to_add = [tweet for tweet in to_add if tweet["text"].startswith(triggers) or tweet["text"].split(" ",1)[1].startswith(triggers)]
    queue = queue + to_add
    mx = max(len(to_add), 20)
    if len(queue) > mx:
        queue = queue[-mx:]
    if len(queue) > 0:
        respond(twitter, queue.pop())
    dump(queue, info)

#run on cron every minute
if __name__ == "__main__":
    main()
