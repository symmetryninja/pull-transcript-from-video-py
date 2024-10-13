import os
import argparse
import moviepy.editor as mp
from pocketsphinx import Pocketsphinx, get_model_path

def video_to_text(video_path, output_text_path):
    # Step 1: Extract audio from video
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path, verbose=False, logger=None)

    # Step 2: Convert audio to text using PocketSphinx
    model_path = get_model_path()
    config = {
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    ps = Pocketsphinx(**config)
    ps.decode(audio_file=audio_path)

    text = ps.hypothesis()

    # Step 3: Write text to file
    with open(output_text_path, "w") as text_file:
        text_file.write(text)

    # Clean up temporary audio file
    os.remove(audio_path)

    print(f"Text extracted and saved to {output_text_path}")

def process_input(input_path):
    if os.path.isfile(input_path):
        # Process single file
        if input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add more video formats if needed
            output_text_path = os.path.splitext(input_path)[0] + '.txt'
            print(f"Processing {input_path}...")
            video_to_text(input_path, output_text_path)
        else:
            print(f"Error: {input_path} is not a supported video file.")
    elif os.path.isdir(input_path):
        # Process folder
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                output_text_path = os.path.join(input_path, os.path.splitext(filename)[0] + '.txt')
                print(f"Processing {filename}...")
                video_to_text(file_path, output_text_path)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a video file or all videos in a folder using PocketSphinx")
    parser.add_argument("input_path", help="Path to the video file or folder containing video files")
    args = parser.parse_args()

    process_input(args.input_path)