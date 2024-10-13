#! /home/spidey/.pyenv/shims/python

import os
import argparse
import moviepy.editor as mp
import speech_recognition as sr

def video_to_text(video_path, output_text_path):
    # Step 1: Extract audio from video
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path, verbose=False, logger=None)

    # Step 2: Convert audio to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            text = f"Could not request results from Speech Recognition service; {e}"

    # Step 3: Write text to file
    with open(output_text_path, "w") as text_file:
        text_file.write(text)

    # Clean up temporary audio file
    os.remove(audio_path)

    print(f"Text extracted and saved to {output_text_path}")

def process_folder(input_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add more video formats if needed
            video_path = os.path.join(input_folder, filename)
            output_text_path = os.path.join(input_folder, os.path.splitext(filename)[0] + '.txt')
            print(f"Processing {filename}...")
            video_to_text(video_path, output_text_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from videos in a folder")
    parser.add_argument("input_folder", help="Path to the folder containing video files")
    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"Error: {args.input_folder} is not a valid directory")
    else:
        process_folder(args.input_folder)