# YouTube-Transcript-Summarizer
## Overview

Developed a Python-based tool designed to enhance content accessibility and save time by providing quick, meaningful overviews of YouTube videos. This project extracts transcripts and generates concise summaries of long video content.

## Features

* **Transcript Extraction:** Efficiently fetches full transcripts from public YouTube video URLs using the `youtube-transcript-api` library.
* **State-of-the-Art Summarization:** Employs a **T5 (Text-to-Text Transfer Transformer)** model from the Hugging Face `transformers` library for text summarization.
* **Web API Endpoint:** Built with Flask and Flask-CORS to provide a robust RESTful API, allowing for easy integration with other applications.

## Technologies Used

* **Python 3.10.9**
* **youtube-transcript-api**: For transcript extraction.
* **NLP (TextRank Algorithm)**: For text summarization.

## Setup

Follow these steps to set up the project on your local machine.

1.  **Clone this repository:**
2.  **Create and activate a virtual environment (highly recommended):**
3.  **Install dependencies:**
    With your virtual environment activated, install all required Python packages by using the following command:
    
    pip install -r requirements.txt

## Usage

This project provides a RESTful API for interacting with the YouTube Transcript Summarizer.

1.Run the API application:

  python app.py
  
This will start the development server, typically accessible at http://127.0.0.1:5000/.

2.Workflow Steps:

Open your browser and navigate to the Home Page:

http://127.0.0.1:5000/

2.a Save the Transcript (Required First Step):

In your browser, go to: http://127.0.0.1:5000/save_transcript?video_id=YOUR_YOUTUBE_VIDEO_ID

Example: http://127.0.0.1:5000/save_transcript?video_id=SLpUKAGnm-g&t=1s

This will fetch and save the transcript. You should see a confirmation message in your browser.

2.b Summarize the Transcript:

In your browser, go to: http://127.0.0.1:5000/summarize

This will generates a summary for a previously saved YouTube video transcript.

