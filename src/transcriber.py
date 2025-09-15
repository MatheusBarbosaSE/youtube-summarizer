import whisper
import os


def transcribe_audio(audio_filepath: str) -> str | None:
    """
    Transcribes the given audio file to text using OpenAI's Whisper model.

    Args:
        audio_filepath (str): The path to the audio file (.mp3).

    Returns:
        str | None: The transcribed text, or None if transcription fails.
    """
    try:
        print ("Loading Whisper model...")
        model = whisper.load_model("base") # Load a whisper model

        print("Transcription is starting")
        result = model.transcribe(audio_filepath, fp16=False) # Transcribe an audio file

        transcribed_text = result ['text']

        # Clean up the audio file after transcription is complete
        print("Cleaning up audio file...")
        os.remove(audio_filepath)

        print("Transcription finished successfully.")
        return transcribed_text

    except Exception as e:
        print (f"An error occurred during the transcription: {e}")
        # If an error happens, also try to clean up the file if it exists
        if os.path.exists(audio_filepath):
            os.remove(audio_filepath)
        return None

# Testing block
if __name__ == "__main__":
    from audio_downloader import download_audio
    test_url = "https://youtu.be/x7X9w_GIm1s?si=Wvjb_a4niW8A364h"
    print ("Testing Transcriber")

    print("\n1. Download audio for test...")
    audio_file = download_audio(test_url)

    if audio_file:
        print("\n2. Transcribing audio...")
        transcribed_text = transcribe_audio(audio_file)
        if transcribed_text:
            print("\n✅ Success! Transcription complete.")
            print("\n--- Transcribed Text ---")
            print(transcribed_text[:200] + "...")
        else:
            print ("\n❌ Failure. Transcription failed.")
    else:
        print ("\n❌ Failure. Could not download audio to test transcription.")



