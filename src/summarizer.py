import os
from groq import Groq
from dotenv import load_dotenv

# This line loads the environment variables from .env file
load_dotenv()

def summarize_text(text_to_summarize: str) -> str | None:
    """
    Summarizes the given text using the Groq API.

    Args:
        text_to_summarize (str): The text to be summarized.

    Returns:
        str | None: The summarized text, or None if it fails.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Make sure it's in a .env file in the project root.")

        client = Groq(api_key=api_key)
        print("Summarization is starting...")

        chat_completion = client.chat.completions.create(
            # This is where the "prompt" is built for the AI
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes texts. Your summaries should be clear, concise, and presented in bullet points."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text:\n\n{text_to_summarize}"
                }
            ],
            model="llama-3.1-8b-instant",
        )

        summary = chat_completion.choices[0].message.content
        print("Summarization finished successfully...")
        return summary

    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None

# Testing Block
if __name__ == '__main__':
    sample_text = """
    Python is a high-level, interpreted, general-purpose programming language. 
    Its design philosophy emphasizes code readability with the use of significant indentation. 
    Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, 
    including structured (particularly procedural), object-oriented and functional programming. 
    It is often described as a "batteries included" language due to its comprehensive standard library. 
    Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming 
    language and first released it in 1991 as Python 0.9.0.
    """
    print(" Testing Summarizer")
    summary = summarize_text(sample_text)

    if summary:
        print("\n✅ Success! Summarization complete.")
        print("\n--- Summary ---")
        print(summary)
    else:
        print("\n❌ Failure. Summarization failed.")