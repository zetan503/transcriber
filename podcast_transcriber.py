#!/usr/bin/env python3
"""
Podcast Transcriber - A tool to transcribe podcasts and generate summaries.

This script downloads audio from a podcast URL, transcribes it using Whisper,
and generates a summary of the content.
"""

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
import re

def ensure_whisper_installed():
    """Check if Whisper is installed and install if needed."""
    try:
        import whisper
        return True
    except ImportError:
        print("Whisper is not installed. Installing now...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "openai-whisper"], check=True)
        return True

def download_podcast(url, output_path):
    """Download podcast audio using yt-dlp."""
    print(f"Downloading podcast audio from: {url}")

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Download audio
    try:
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", output_path,
            url
        ], check=True)

        if os.path.exists(output_path):
            print(f"Download complete: {output_path}")
            return True
        else:
            print("Download failed: File not found")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Download failed: {e}")
        return False
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install it with 'pip install yt-dlp'")
        return False

def transcribe_audio(audio_path, output_dir, model_size="base"):
    """Transcribe audio using Whisper."""
    print(f"Transcribing audio with Whisper (model: {model_size})...")

    # Ensure Whisper is installed
    if not ensure_whisper_installed():
        return None

    # Import here to ensure it's installed
    import whisper

    try:
        # Load the model
        model = whisper.load_model(model_size)

        # Transcribe
        result = model.transcribe(audio_path)

        # Save transcript
        transcript_path = os.path.join(output_dir, "transcript.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"Transcription complete. Saved to: {transcript_path}")
        return transcript_path
    except Exception as e:
        print(f"Transcription failed: {e}")
        return None

def clean_text(text):
    """Clean transcript text."""
    # Remove timestamps and indices
    lines = text.split('\n')
    content = []
    for line in lines:
        if not re.match(r'^\d+$|^\d{2}:\d{2}:', line.strip()):
            content.append(line.strip())

    # Join and clean
    text = ' '.join(content)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\b(um|uh|ah|er|like)\b', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_sentences(text):
    """Split text into sentences."""
    sentences = re.split(r'[.!?]+\s+', text)
    return [s.strip() for s in sentences if len(s.split()) > 5]

def score_sentence(sentence, word_freq):
    """Score a sentence based on word frequency."""
    words = sentence.lower().split()
    return sum(word_freq.get(word, 0) for word in words) / len(words)

def summarize_text(text, num_sentences=10):
    """Summarize text using extractive summarization."""
    # Clean text
    cleaned = clean_text(text)

    # Get sentences
    sentences = get_sentences(cleaned)
    if not sentences:
        return ""

    # Calculate word frequencies
    words = cleaned.lower().split()
    word_freq = Counter(words)

    # Score sentences
    scored = [(score_sentence(s, word_freq), s) for s in sentences]
    top_sentences = sorted(scored, reverse=True)[:num_sentences]

    # Return summary
    return ". ".join(s[1] for s in top_sentences) + "."

def summarize_transcript(transcript_path, output_path, num_sentences=10):
    """Generate summary from transcript."""
    print(f"Generating summary (top {num_sentences} sentences)...")

    try:
        # Read transcript
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        # Generate summary
        summary = summarize_text(transcript, num_sentences)

        # Save summary
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"Summary saved to: {output_path}")
        return summary
    except Exception as e:
        print(f"Summarization failed: {e}")
        return None

def save_metadata(url, audio_path, transcript_path, summary_path, output_path):
    """Save metadata about the podcast."""
    metadata = {
        "url": url,
        "audio_file": audio_path,
        "transcript_file": transcript_path,
        "summary_file": summary_path,
        "processed_date": subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"]).decode().strip()
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to: {output_path}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Transcribe and summarize podcasts")
    parser.add_argument("url", help="URL of the podcast to process")
    parser.add_argument("--output-dir", default="podcast_output", help="Output directory")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (larger = better quality but slower)")
    parser.add_argument("--sentences", type=int, default=10, help="Number of sentences in summary")
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Define file paths
    audio_path = os.path.join(args.output_dir, "podcast_audio.mp3")
    transcript_path = os.path.join(args.output_dir, "transcript.txt")
    summary_path = os.path.join(args.output_dir, "summary.txt")
    metadata_path = os.path.join(args.output_dir, "metadata.json")

    # Step 1: Download podcast
    if not download_podcast(args.url, audio_path):
        return 1

    # Step 2: Transcribe audio
    transcript_path = transcribe_audio(audio_path, args.output_dir, args.model)
    if not transcript_path:
        return 1

    # Step 3: Summarize transcript
    summary = summarize_transcript(transcript_path, summary_path, args.sentences)
    if not summary:
        return 1

    # Step 4: Save metadata
    save_metadata(args.url, audio_path, transcript_path, summary_path, metadata_path)

    # Print summary
    print("\nSummary:")
    print("=========")
    print(summary)

    print("\nFiles saved:")
    print(f"- Full transcript: {transcript_path}")
    print(f"- Summary: {summary_path}")
    print(f"- Audio: {audio_path}")
    print(f"- Metadata: {metadata_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
