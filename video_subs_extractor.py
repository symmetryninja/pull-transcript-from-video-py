#!/home/spidey/.pyenv/shims/python

import os
import argparse
import json
import wave
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.effects import normalize
from vosk import Model, KaldiRecognizer, SetLogLevel

def convert_to_mono_wav(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    audio = audio.set_channels(1)  # Convert to mono
    audio = audio.set_frame_rate(16000)  # Set frame rate to 16kHz
    audio = audio.set_sample_width(2)  # Set sample width to 2 bytes (16 bit)
    
    converted_path = audio_path.replace('.wav', '_mono.wav')
    audio.export(converted_path, format="wav")
    return converted_path

def enhance_audio(audio_path):
    print("Enhancing audio quality...")
    audio = AudioSegment.from_wav(audio_path)
    
    # Normalize audio
    audio = normalize(audio)
    
    # Apply compression
    audio = audio.compress_dynamic_range(threshold=-15.0, ratio=2.0, attack=5.0, release=50.0)
    
    # Increase volume by 3 dB
    audio = audio + 3
    
    # Apply a high-pass filter to reduce low-frequency noise
    audio = audio.high_pass_filter(100)
    
    # Apply a low-pass filter to reduce high-frequency noise
    audio = audio.low_pass_filter(7500)
    
    # Export enhanced audio
    base_name = os.path.splitext(audio_path)[0]
    enhanced_path = f"{base_name}_enhanced.wav"
    audio.export(enhanced_path, format="wav")
    return enhanced_path

def process_audio_chunk(rec, chunk):
    if rec.AcceptWaveform(chunk):
        result = json.loads(rec.Result())
        return result.get('text', '')
    return ''

def video_to_text(video_path, output_text_path, model_path):
    print(f"\nProcessing video: {video_path}")

    # Step 1: Extract audio from video
    print("Extracting audio...")
    video = mp.VideoFileClip(video_path)
    base_name = os.path.splitext(video_path)[0]
    audio_path = f"{base_name}_extracted.wav"
    video.audio.write_audiofile(audio_path, fps=16000, nbytes=2, verbose=False, logger=None)

    # Step 2: Convert audio to mono WAV
    print("Converting audio to mono WAV...")
    mono_audio_path = convert_to_mono_wav(audio_path)

    # Step 3: Enhance audio
    enhanced_audio_path = enhance_audio(mono_audio_path)

    # Step 4: Perform speech recognition
    print("Performing speech recognition...")
    SetLogLevel(0)
    
    if not os.path.exists(model_path):
        print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
        return

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    # Set some parameters that might help with accent recognition
    rec.SetWords(True)
    rec.SetPartialWords(True)

    wf = wave.open(enhanced_audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Error: Audio file is not in correct format. Please check the conversion step.")
        return

    chunk_duration_ms = 30000  # 30 seconds
    wav_audio = AudioSegment.from_wav(enhanced_audio_path)
    chunks = [wav_audio[i:i+chunk_duration_ms] for i in range(0, len(wav_audio), chunk_duration_ms)]

    results = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1} of {len(chunks)}...")
        chunk_path = f"temp_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        
        chunk_wf = wave.open(chunk_path, "rb")
        chunk_data = chunk_wf.readframes(chunk_wf.getnframes())
        
        text = process_audio_chunk(rec, chunk_data)
        results.append(text)
        
        chunk_wf.close()
        os.remove(chunk_path)

    # Combine all recognized text
    text = " ".join(results)

    # Step 5: Write text to file
    with open(output_text_path, "w") as text_file:
        text_file.write(text)
    print(f"Text saved to: {output_text_path}")

    # Clean up
    os.remove(audio_path)
    os.remove(mono_audio_path)
    print(f"Enhanced audio saved to: {enhanced_audio_path}")

    return text

def process_input(input_path, model_path):
    if os.path.isfile(input_path):
        if input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            output_text_path = os.path.splitext(input_path)[0] + '.txt'
            text = video_to_text(input_path, output_text_path, model_path)
            print(f"Recognized text (first 100 characters): {text[:100]}...")
        else:
            print(f"Error: {input_path} is not a supported video file.")
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                output_text_path = os.path.join(input_path, os.path.splitext(filename)[0] + '.txt')
                text = video_to_text(file_path, output_text_path, model_path)
                print(f"Recognized text for {filename} (first 100 characters): {text[:100]}...")
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a video file or all videos in a folder")
    parser.add_argument("input_path", help="Path to the video file or folder containing video files")
    parser.add_argument("model_path", help="Path to the Vosk model directory")
    args = parser.parse_args()

    print("Script started")
    process_input(args.input_path, args.model_path)
    print("Script finished")