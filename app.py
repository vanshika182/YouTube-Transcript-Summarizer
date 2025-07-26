# from flask import Flask
# from youtube_transcript_api import YouTubeTranscriptApi
# import json

# app = Flask(__name__)

# def save_transcript_to_json(video_id):
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

#     with open("transcript.json", "w") as file:
#         json.dump(transcript_list, file, indent=4)

# def read_transcript_from_json():
#     with open("transcript.json", "r") as file:
#         data = json.load(file)
#         return data
# def extract_text_from_data(data):
#     return ' '.join([part['text'] for part in data])

# # Function to get transcript from a YouTube video
# # def get_transcript(video_id):
# #     try:
# #         # Step 1: Get the transcript (list of dictionaries)
# #         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

# #         # Step 2: Extract only the text parts
# #         text_parts = [part['text'] for part in transcript_list]

# #         # Step 3: Join the text into one string
# #         full_transcript = ' '.join(text_parts)

# #         return full_transcript
    
# #     except Exception as e:
# #         return f"Error: {str(e)}"
# # print(get_transcript("SLpUKAGnm-g"))
# # Optional: Test the function by calling it inside a route

# @app.route('/')
# def home():
#     return "Backend is working!"

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json
import re

app = Flask(__name__)
CORS(app)  # <-- Add this line

# Save transcript to a .json file
def save_transcript_to_json(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

    # Save to file
    with open("transcript.json", "w") as file:
        json.dump(transcript_list, file, indent=4)

# Read transcript from .json file
def read_transcript_from_json():
    with open("transcript.json", "r") as file:
        data = json.load(file)
        return data

# Extract text from data
def extract_text_from_data(data):
    return ' '.join([part['text'] for part in data])

@app.route('/save_transcript', methods=['GET'])
def save_transcript():
    video_id = request.args.get('video_id')  # Get video ID from URL parameter
    if video_id:
        save_transcript_to_json(video_id)  # Save transcript to JSON
        return f"Transcript saved for video {video_id}!"
    return "Error: No video ID provided."

@app.route('/read_transcript', methods=['GET'])
def read_transcript():
    try:
        data = read_transcript_from_json()  # Read data from the JSON file
        full_text = extract_text_from_data(data)  # Extract the text
        return f"Full Transcript: {full_text}"  # Return full transcript text
    except Exception as e:
        return f"Error: {str(e)}"
#  New function: Summarize transcript
def summarize_text(transcript):
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")

    # Add prefix required for T5 model
    input_text = "summarize: " + transcript

    # Tokenize the text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode and return summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.route('/summarize')
def summarize():
    data = read_transcript_from_json()
    full_transcript = extract_text_from_data(data)
    summary = summarize_text(full_transcript)
    return f"<h2>Summary:</h2><p>{summary}</p>"
@app.route('/api/summarize', methods=['GET'])
def summarize_api():
    youtube_url = request.args.get('youtube_url')

    if not youtube_url:
        return jsonify({"error": "youtube_url parameter is required"}), 400

    # Step 1: Extract video ID
    video_id = extract_video_id(youtube_url)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        # Step 2: Save transcript from YouTube
        save_transcript_to_json(video_id)

        # Step 3: Read transcript from saved JSON
        data = read_transcript_from_json()

        # Step 4: Extract full text
        full_transcript = extract_text_from_data(data)

        # Step 5: Summarize the transcript
        summary = summarize_text(full_transcript)

        # Step 6: Return summary as JSON
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_video_id(url):
    # Regex to extract YouTube video ID from various URL formats
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

@app.route('/')
def home():
    return "Backend is working! Visit /save_transcript?video_id=<video_id> to save the transcript."

if __name__ == '__main__':
    app.run(debug=True)

