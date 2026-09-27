"""YouTube Video Summarizer + Q&A.

Paste a YouTube link -> fetch the transcript -> get detailed notes and
ask follow-up questions about the video, all powered by Google Gemini.

Original project: https://github.com/mdzaheerjk/End-To-End-Youtube-Video-Transcribe-Summarizer-LLM-App-With-Google-Gemini-Pro
by Mohd Zaheeruddin (MIT License). Extended and maintained by
Muhammad Huzaifa Aqeel (https://github.com/HuzaifaAqeel).
"""

import os

import streamlit as st
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi


st.sidebar.title("Settings")
api_key = os.environ.get("GOOGLE_API_KEY") or st.sidebar.text_input(
    "Gemini API key (or set the GOOGLE_API_KEY env var)",
    type="password",
)


summary_prompt = """
You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:
"""

qa_prompt = """
You are a helpful assistant answering questions about a YouTube video.
Answer the question below concisely and accurately, using ONLY the
transcript provided. If the transcript does not contain the answer, say so.

Transcript:
"""


def extract_transcription_details(youtube_video_url):
    """Fetch the transcript of a YouTube video URL.

    Returns the transcript as a single string, or None if it fails.
    """
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]

        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        transcript_text = " ".join(snippet.text for snippet in transcript)
        return transcript_text

    except Exception as e:
        st.error(e)
        return None


def generate_gemini_content(transcript_text, prompt):
    """Send a prompt + transcript to Gemini and return the text response."""
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt + transcript_text,
    )

    return response.text


st.title("YouTube Transcript Summarizer + Q&A")

youtube_link = st.text_input("Enter YouTube video link:")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1].split("&")[0]
        st.image(
            f"https://img.youtube.com/vi/{video_id}/0.jpg",
            use_container_width=True,
        )
    except IndexError:
        st.warning("That doesn't look like a YouTube watch URL.")

pasted_transcript = st.text_area(
    "No transcript available? Paste it here instead (optional):",
    height=150,
)

if st.button("Get Detailed Notes"):
    transcript_text = None
    if pasted_transcript.strip():
        transcript_text = pasted_transcript.strip()
    elif youtube_link:
        transcript_text = extract_transcription_details(youtube_link)

    if transcript_text:
        st.session_state["transcript_text"] = transcript_text
        with st.spinner("Generating notes with Gemini..."):
            summary = generate_gemini_content(transcript_text, summary_prompt)
        st.session_state["summary"] = summary
        st.markdown("## Detailed Notes:")
        st.write(summary)
    else:
        st.warning("Enter a YouTube link or paste a transcript to continue.")

if st.session_state.get("summary"):
    st.markdown("## Ask about this video")
    question = st.text_input("Your question:")
    if st.button("Ask") and question.strip():
        with st.spinner("Thinking..."):
            answer = generate_gemini_content(
                st.session_state["transcript_text"],
                qa_prompt + "\n\nQuestion: " + question.strip(),
            )
        st.write(answer)
