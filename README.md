# YouTube Video Summarizer + Q&A

Paste a YouTube link → get the transcript → receive detailed notes and ask
follow-up questions about the video, all powered by Google Gemini.

## Credits

This project is based on
[End-To-End-Youtube-Video-Transcribe-Summarizer-LLM-App-With-Google-Gemini-Pro](https://github.com/mdzaheerjk/End-To-End-Youtube-Video-Transcribe-Summarizer-LLM-App-With-Google-Gemini-Pro)
by **Mohd Zaheeruddin**, released under the **MIT License** (see `LICENSE`).

It was extended and is maintained by **Muhammad Huzaifa Aqeel**
([HuzaifaAqeel](https://github.com/HuzaifaAqeel)) — it was **not** built
from scratch.

## What it does

- Extracts the transcript of any YouTube video from its URL
  (via `youtube-transcript-api`)
- Generates concise, bullet-point "detailed notes" of the video with Gemini
- Lets you ask follow-up questions about the video in a Q&A section
- Falls back to a manual "paste transcript" box when a video has no
  captions or YouTube blocks automated fetching

## Tech stack

- [Streamlit](https://streamlit.io/) — web UI
- [Google Gemini](https://ai.google.dev/) (`gemini-2.5-flash`) — summarization and Q&A
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) — transcript fetching
- Python 3

## Run it

```bash
pip install -r requirements.txt

# set your Gemini API key (get one free at https://aistudio.google.com/)
export GOOGLE_API_KEY="your-key-here"

streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501), paste a
YouTube link, click **Get Detailed Notes**, and ask questions about the video.
