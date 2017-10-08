from __future__ import unicode_literals
import datetime
import prettyprint
import youtube_dl
import feedparser

python_wiki_rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=" \
                      "UC2eYFnH61tmytImy1mTYvhA"

def feed():
    return feedparser.parse(python_wiki_rss_url)

def format_time(published_time):
    return datetime.datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%S+00:00")
        
def grab_videos(feed):
    videos = []
    prevHalfHour = datetime.datetime.now() - datetime.timedelta(days=21)
    for x in range(0, len(feed)):
        if format_time(feed["entries"][x]["published"]) > prevHalfHour:
            videos.append(feed["entries"][x]["link"].encode("ascii"))
    return videos

def download_videos(videos):
    ydl_opts = {}
    for x in range(0, len(videos)):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(videos[x])
            ydl.download(videos)

download_videos(grab_videos(feed()))
