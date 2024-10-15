# Whisper Video Transcription Script

This script uses OpenAI's Whisper model to transcribe audio from video files. It can process either a single video file or a folder containing multiple video files.

## Prerequisites

- Python 3.7 or later
- CUDA-compatible GPU (optional, but recommended for faster processing)

## Installation

1. Clone this repository or download the script file.

2. Install the required Python packages:

   ```bash
   pip install openai-whisper moviepy torch
   ```

3. Make the script executable:

   ```bash
   chmod +x whisper_video_to_text.py
   ```

## Usage

To run the script, use the following command:

```bash
./whisper_video_to_text.py [INPUT_PATH] [OPTIONS]
```

### Arguments

- `INPUT_PATH`: Path to the video file or folder containing video files

### Options

- `--model`: Whisper model to use (default: base)
  - Choices: tiny, base, small, medium, large

### Examples

1. Transcribe a single video file using the default (base) model:

   ```bash
   ./whisper_video_to_text.py /path/to/your/video.mp4
   ```

2. Transcribe all videos in a folder using the large model:

   ```bash
   ./whisper_video_to_text.py /path/to/your/video/folder --model large
   ```

## Output

The script will create a text file for each processed video, with the same name as the video file and "_transcription.txt" appended. For example, "video.mp4" will produce "video_transcription.txt" in the same directory.

## Supported Video Formats

The script supports the following video formats:

- .mp4
- .avi
- .mov
- .mkv

## Notes

- The script automatically uses GPU acceleration if a CUDA-compatible GPU is available.
- Larger models (e.g., 'large') provide better accuracy but require more computational resources and time.
- The script extracts audio from the video, processes it, and then deletes the temporary audio file.
- If processing a folder, the script will attempt to process all supported video files in that folder.

## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are correctly installed.
2. Check that the input path is correct and accessible.
3. If using GPU acceleration, ensure your CUDA drivers are up to date.
4. For very large video files, ensure you have enough disk space for temporary audio files.

## License

This script is provided "as is", without warranty of any kind. Use at your own risk.

## Acknowledgments

This script uses the following open-source projects:

- [OpenAI Whisper](https://github.com/openai/whisper)
- [MoviePy](https://zulko.github.io/moviepy/)
- [PyTorch](https://pytorch.org/)

For more information on Whisper models and their capabilities, visit the [OpenAI Whisper GitHub repository](https://github.com/openai/whisper).
