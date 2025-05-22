# Podcast Transcription and Summarization

This project provides tools to transcribe podcasts to text using speech-to-text technology and generate summaries of the content. It builds on existing YouTube summarization functionality but extends it to work with podcast audio.

## Requirements

- Python 3.6+
- yt-dlp (for downloading audio)
- OpenAI Whisper (for speech-to-text)
- Additional Python packages (installed automatically)

## Installation

1. Clone this repository
2. Install yt-dlp:
   ```
   pip install yt-dlp
   ```
3. The scripts will automatically install Whisper if it's not already installed

## Tools

### Bash Script: podcast-transcribe.sh

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
