#!/home/spidey/.pyenv/shims/python

import os
import argparse
import whisper
import torch
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    print(f"Extracting audio from {video_path}...")
    video = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    video.audio.write_audiofile(audio_path, codec='pcm_s16le', verbose=False, logger=None)
    return audio_path

def transcribe_audio(audio_path, model):
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path)
    return result["text"]

def process_file(file_path, model):
    if not file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        print(f"Skipping {file_path}: not a supported video file.")
        return

    try:
        audio_path = extract_audio(file_path)
        transcription = transcribe_audio(audio_path, model)

        output_path = file_path.rsplit('.', 1)[0] + '_transcription.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcription)

        print(f"Transcription saved to {output_path}")

        # Clean up the temporary audio file
        os.remove(audio_path)
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def process_input(input_path, model_size):
    print(f"Using Whisper model: {model_size}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = whisper.load_model(model_size, device=device)

    if os.path.isfile(input_path):
        process_file(input_path, model)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path):
                process_file(file_path, model)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe video files using Whisper")
    parser.add_argument("input_path", help="Path to the video file or folder containing video files")
    parser.add_argument("--model", choices=['tiny', 'base', 'small', 'medium', 'large'], default='base', help="Whisper model to use (default: base)")
    args = parser.parse_args()

    print("Script started")
    process_input(args.input_path, args.model)
    print("Script finished")