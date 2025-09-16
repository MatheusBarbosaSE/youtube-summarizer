import os
import yt_dlp
import re


def _sanitize_filename(title: str) -> str:
    """
    Removes characters that are invalid for filenames.
    """
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
    sanitized_title = sanitized_title.replace(" ", "_")
    return sanitized_title


def download_audio(video_url: str, output_path: str = ".") -> str | None:
    """
    Downloads the audio from a YouTube video using yt-dlp.

    Args:
        video_url (str): The URL of the YouTube video.
        output_path (str): The directory where the file will be saved.

    Returns:
        str | None: The file path of the downloaded audio file, or None if it fails.
    """
    try:
        # yt-dlp Configuration
        # define a dictionary with all the download options.

        # First, get video info without downloading to create a clean filename
        with yt_dlp.YoutubeDL({'noplaylist': True, 'quiet': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'untitled_video')
            sanitized_title = _sanitize_filename(video_title)

        # The final filename we want, without extension
        output_filename = os.path.join(output_path, sanitized_title)

        ydl_opts = {
            'format': 'bestaudio/best',  # Select the best audio quality
            'outtmpl': f'{output_filename}.%(ext)s',  # Output template for the filename
            'noplaylist': True,  # Ensure only download a single video
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convert the audio to MP3
                'preferredquality': '192',
            }],
        }

        # Downloading
        print(f"Downloading and converting: {video_title}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # The final path will have the .mp3 extension after conversion
        final_filepath = f"{output_filename}.mp3"
        print(f"Download complete! File saved at: {final_filepath}")

        return final_filepath

    except Exception as e:
        print(f"An error occurred during download: {e}")
        return None

# Testing Block
if __name__ == '__main__':
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"Testing the download function with URL: {test_url}")

    downloaded_file = download_audio(test_url)

    if downloaded_file:
        print(f"\n✅ Success! The function returned the file path: {downloaded_file}")
    else:
        print("\n❌ Failure. The function returned None.")