from src.audio_downloader import download_audio
from src.transcriber import transcribe_audio
from src.summarizer import summarize_text


def main():
    """
    Main function to run the video summarization pipeline.
    """
    video_url = input("Enter the URL of the video you want to summarize: ")
    if not video_url:
        print("The video URL cannot be empty.")
        return

    print("\nStarting the summarization process...")

    # Step 1: Download Audio
    audio_file = download_audio(video_url)
    if not audio_file:
        print("Failed to download audio. Halting process.")
        return

    # Step 2: Transcribe Audio
    transcribed_text = transcribe_audio(audio_file)
    if not transcribed_text:
        print("Failed to transcribe audio. Halting process.")
        return

    # Step 3: Summarize Text
    summary = summarize_text(transcribed_text)

    # Final Step: Display the Result
    if summary:
        print("\n" + "=" * 20)
        print("--- VIDEO SUMMARY ---")
        print("=" * 20 + "\n")
        print(summary)
    else:
        print("Failed to generate summary.")


if __name__ == "__main__":
    main()