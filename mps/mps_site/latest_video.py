import feedparser
import yt_dlp as youtube_dl

def get_latest_video_id(channel_url):
    # Fetch the channel's RSS feed
    feed = feedparser.parse(channel_url)

    # Extract the latest video ID from the feed
    if len(feed.entries) > 0:
        latest_video_url = feed.entries[0].link
        video_id = latest_video_url.split('=')[-1]  # Extract the video ID from the URL
        return video_id
    else:
        return None

# Example usage:
channel_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"
latest_video_id = get_latest_video_id(channel_url)
