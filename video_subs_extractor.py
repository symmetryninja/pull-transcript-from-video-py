#! /home/spidey/.pyenv/shims/python

import sys
import platform

print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")

try:
    import os
    print("Successfully imported os")
except ImportError as e:
    print(f"Error importing os: {str(e)}")

try:
    import argparse
    print("Successfully imported argparse")
except ImportError as e:
    print(f"Error importing argparse: {str(e)}")

try:
    import moviepy.editor as mp
    print("Successfully imported moviepy")
except ImportError as e:
    print(f"Error importing moviepy: {str(e)}")

try:
    from pocketsphinx import Pocketsphinx, get_model_path
    print("Successfully imported pocketsphinx")
except ImportError as e:
    print(f"Error importing pocketsphinx: {str(e)}")

def video_to_text(video_path, output_text_path):
    print(f"Starting process for video: {video_path}")

    # Step 1: Extract audio from video
    print("Step 1: Extracting audio from video...")
    try:
        video = mp.VideoFileClip(video_path)
        audio = video.audio
        audio_path = "temp_audio.wav"
        audio.write_audiofile(audio_path, verbose=False, logger=None)
        print(f"Audio extracted successfully: {audio_path}")
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return

    print("Step 2: Converting audio to text using PocketSphinx...")
    try:
        # Use system-wide paths for PocketSphinx models
        config = {
            'hmm': '/usr/local/share/pocketsphinx/model/en-us/en-us',
            'lm': '/usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin',
            'dict': '/usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict'
        }
        print("PocketSphinx configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
            if not os.path.exists(value):
                print(f"  Warning: {value} does not exist!")

        ps = Pocketsphinx(**config)
        print("PocketSphinx instance created")
        ps.decode(audio_file=audio_path)
        print("Audio decoding completed")

        text = ps.hypothesis()
        print("Text hypothesis generated")
    except Exception as e:
        print(f"Error in speech recognition: {str(e)}")
        return

    # Step 3: Write text to file
    print(f"Step 3: Writing text to file: {output_text_path}")
    try:
        with open(output_text_path, "w") as text_file:
            text_file.write(text)
        print("Text written to file successfully")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        return

    # Clean up temporary audio file
    print("Cleaning up temporary audio file...")
    try:
        os.remove(audio_path)
        print("Temporary audio file removed")
    except Exception as e:
        print(f"Error removing temporary file: {str(e)}")

    print(f"Process completed. Text extracted and saved to {output_text_path}")

def process_input(input_path):
    print(f"Processing input: {input_path}")
    if os.path.isfile(input_path):
        print("Input is a file")
        if input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            output_text_path = os.path.splitext(input_path)[0] + '.txt'
            print(f"Processing {input_path}...")
            video_to_text(input_path, output_text_path)
        else:
            print(f"Error: {input_path} is not a supported video file.")
    elif os.path.isdir(input_path):
        print("Input is a directory")
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                output_text_path = os.path.join(input_path, os.path.splitext(filename)[0] + '.txt')
                print(f"Processing {filename}...")
                video_to_text(file_path, output_text_path)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    print("Script started")
    
    parser = argparse.ArgumentParser(description="Extract text from a video file or all videos in a folder using PocketSphinx")
    parser.add_argument("input_path", help="Path to the video file or folder containing video files")
    args = parser.parse_args()

    process_input(args.input_path)
    print("Script finished")