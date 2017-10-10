from __future__ import unicode_literals
import datetime
import prettyprint
import youtube_dl
import feedparser
import json

def grabChannelUrls(file):
    channel_urls = []
    channel = file["main"]["outline"]
    for x in range(len(channel)):
       channel_urls.append(channel[x]["_xmlUrl"])
    return channel_urls

def subscriptions():
    file = json.loads(open("subman.json", "r").read())
    return grabChannelUrls(file)

def rss_feed(channel):
    print(channel)
    return feedparser.parse(channel)

def format_time(published_time):
    return datetime.datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%S+00:00")
        
def grab_videos(feed):
    videos = []
    prevHalfHour = datetime.datetime.now() - datetime.timedelta(minutes=30)
    for x in range(0, 5):
        try:
            if format_time(feed["entries"][x]["published"]) > prevHalfHour:
                videos.append(feed["entries"][x]["link"].encode("ascii"))
        except:
            print("failure")
    return videos

def download_videos(videos):
    ydl_opts = {}
    for x in range(0, len(videos)):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(videos[x])
            ydl.download(videos)


for channel in subscriptions():
    download_videos(
        grab_videos(
            rss_feed(
                channel)))


