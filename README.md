# Podcast Transcription and Summarization

This project provides tools to transcribe podcasts to text using speech-to-text technology and generate summaries of the content. It builds on existing YouTube summarization functionality but extends it to work with podcast audio.

## Requirements

- Python 3.6+
- CUDA-compatible GPU (optional, but recommended for faster transcription)
- FFmpeg (required for audio processing)
- All Python dependencies are listed in requirements.txt

## Installation

1. Clone this repository
2. Create a Python virtual environment (recommended):
   ```bash
   python3 -m venv whisper_env
   source whisper_env/bin/activate  # On Windows: whisper_env\Scripts\activate
   ```
3. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### GPU Acceleration

The installation above includes PyTorch with CUDA support, which will automatically use your GPU(s) for Whisper transcription if available. This can speed up transcription by 5-10x compared to CPU-only processing.

To verify GPU support is working:
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU count:', torch.cuda.device_count())"
```

This should output `CUDA available: True` if your GPU is properly detected.

## Tools

### YouTube Summarization Scripts

#### yt-summerize.sh

A bash script that downloads YouTube subtitles and generates a summary using the Fabric tool.

```bash
# Basic usage
./yt-summerize.sh <youtube-url>

# Example
./yt-summerize.sh https://www.youtube.com/watch?v=wYb3Wimn01s
```

The script will:
1. Download subtitles from the provided YouTube URL
2. Clean the subtitles (remove timestamps and indices)
3. Use Fabric to generate a summary
4. Display the summary and save it to summary.txt

#### fabric.sh

A script that uses the Fabric tool to process YouTube videos and generate summaries in markdown format.

```bash
# Basic usage
./fabric.sh <youtube-url>

# Example
./fabric.sh https://www.youtube.com/watch?v=wYb3Wimn01s
```

#### fabric2.sh

Similar to fabric.sh but uses the Llama 3 8B model for summarization.

```bash
# Basic usage
./fabric2.sh <youtube-url>

# Example
./fabric2.sh https://www.youtube.com/watch?v=wYb3Wimn01s
```

#### ytr.sh

A bash-only script that downloads YouTube subtitles and generates a summary without requiring external tools.

```bash
# Basic usage
./ytr.sh <youtube-url>

# Example
./ytr.sh https://www.youtube.com/watch?v=wYb3Wimn01s
```

### Podcast Transcription Scripts

#### podcast-transcribe.sh

A simple bash script that downloads podcast audio, transcribes it, and generates a summary.

```bash
# Basic usage
./podcast-transcribe.sh <podcast-url>

# Example
./podcast-transcribe.sh https://example.com/podcast-episode
```

The script will:
1. Download the audio from the provided URL
2. Transcribe the audio using Whisper (base model)
3. Generate a summary using one of three methods:
   - Fabric (if available)
   - Python summarizer
   - Simple bash-based summarization

All files are saved in the `podcast_output` directory.

### Python Script: podcast_transcriber.py

A more flexible Python script with additional options.

```bash
# Basic usage
./podcast_transcriber.py <podcast-url>

# With options
./podcast_transcriber.py <podcast-url> --output-dir custom_output --model medium --sentences 15
```

Options:
- `--output-dir`: Custom output directory (default: podcast_output)
- `--model`: Whisper model size (tiny, base, small, medium, large)
- `--sentences`: Number of sentences in the summary (default: 10)

The Python script provides:
- Better error handling
- More customization options
- Metadata tracking
- Higher quality transcription with larger models

## Output Files

Both scripts generate the following files:
- `podcast_audio.mp3`: The downloaded audio file
- `transcript.txt`: The full transcript of the podcast
- `summary.txt`: A summary of the podcast content

The Python script also generates:
- `metadata.json`: Information about the processing

## How It Works

1. **Download**: Uses yt-dlp to download audio from the provided URL
2. **Transcription**: Uses OpenAI's Whisper model to convert speech to text
3. **Summarization**: Uses extractive summarization to identify the most important sentences

## Troubleshooting

- If you encounter issues with downloading, make sure yt-dlp is installed and up to date
- For transcription issues, try using a smaller Whisper model (tiny or base)
- If summarization produces poor results, try adjusting the number of sentences
- If Whisper is running slowly, check GPU usage with `nvidia-smi` to ensure it's utilizing your GPU
- If your GPU is not being used:
  - Verify PyTorch is installed with CUDA support: `python -c "import torch; print(torch.cuda.is_available())"`
  - Ensure you have enough free GPU memory
  - Try reinstalling PyTorch with the correct CUDA version for your system from https://pytorch.org/get-started/locally/

### Fabric Tool Issues

- If you're using the Fabric-based scripts (`yt-summerize.sh`, `fabric.sh`, or `fabric2.sh`), make sure you have the Fabric CLI tool installed
- You can install Fabric using:
  ```bash
  pip install fabric-cli
  ```
- For more information about Fabric, visit the official documentation

## License

MIT

## Sample Podcasts

For testing purposes, we've provided a list of AI-focused podcast episodes in the [ai_podcast_samples.md](ai_podcast_samples.md) file. These samples include YouTube links to Lex Fridman Podcast episodes and TED Talks on AI that can be used to test the transcription and summarization tools.

Example:
```bash
# Using the bash script with a short TED Talk (recommended for initial testing)
./podcast-transcribe.sh https://www.youtube.com/watch?v=wYb3Wimn01s

# Using the Python script with a medium-sized model
./podcast_transcriber.py https://www.youtube.com/watch?v=wYb3Wimn01s --model medium
```

The sample podcasts include both short talks (5-15 minutes) for quick testing and longer episodes (1+ hours) for more comprehensive testing.
