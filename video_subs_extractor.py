import os
import argparse
import moviepy.editor as mp
from pocketsphinx import LiveSpeech, get_model_path

def video_to_text(video_path, output_text_path):
    # Step 1: Extract audio from video
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path, verbose=False, logger=None)

    # Step 2: Convert audio to text using PocketSphinx
    model_path = get_model_path()
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'en-us'),
        lm=os.path.join(model_path, 'en-us.lm.bin'),
        dic=os.path.join(model_path, 'cmudict-en-us.dict')
    )

    text = ""
    for phrase in speech.listen(audio_path):
        text += str(phrase) + " "

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
    parser = argparse.ArgumentParser(description="Extract text from videos in a folder using PocketSphinx")
    parser.add_argument("input_folder", help="Path to the folder containing video files")
    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"Error: {args.input_folder} is not a valid directory")
    else:
        process_folder(args.input_folder)