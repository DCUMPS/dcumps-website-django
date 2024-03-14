import yt_dlp as youtube_dl

def get_most_popular_video_ids(channel_url, n=9):
    ydl_opts = {
        'quiet': True,
        'force_generic_extractor': True,
        'skip_download': True,
        'extract_flat': True,
        'match_filter': youtube_dl.utils.match_filter_func('view_count>=1000000'),
        'playlistend': n,
        'sort': 'view_count'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        video_ids = [entry['id'] for entry in info['entries']]
        return video_ids

if __name__ == "__main__":
    #channel_url = input("Enter the URL of the YouTube channel: ")
    channel_url = "https://www.youtube.com/@dcumps"
    top_videos = get_most_popular_video_ids(channel_url)
    print("Most Popular Video IDs:")
    for idx, video_id in enumerate(top_videos, start=1):
        print(f"{idx}. {video_id}")