#!/bin/bash

# Check if URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <podcast-url>"
    exit 1
fi

PODCAST_URL="$1"
OUTPUT_DIR="podcast_output"
AUDIO_FILE="$OUTPUT_DIR/podcast_audio.mp3"
TRANSCRIPT_FILE="$OUTPUT_DIR/transcript.txt"
SUMMARY_FILE="$OUTPUT_DIR/summary.txt"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Step 1: Download podcast audio using yt-dlp
echo "Downloading podcast audio from: $PODCAST_URL"
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "$AUDIO_FILE" "$PODCAST_URL"

# Check if download was successful
if [ ! -f "$AUDIO_FILE" ]; then
    echo "Failed to download podcast audio"
    exit 1
fi

# Step 2: Transcribe audio using Whisper
echo "Transcribing audio with Whisper..."
# Check if whisper is installed
if ! command -v whisper &> /dev/null; then
    echo "Whisper is not installed. Installing now..."
    pip install -U openai-whisper
fi

# Run transcription
whisper "$AUDIO_FILE" --model base --output_dir "$OUTPUT_DIR" --output_format txt

# The output file will be named the same as the input but with .txt extension
WHISPER_OUTPUT="${AUDIO_FILE%.*}.txt"

if [ ! -f "$WHISPER_OUTPUT" ]; then
    echo "Failed to transcribe audio"
    exit 1
fi

# Move the transcript to a standard location
mv "$WHISPER_OUTPUT" "$TRANSCRIPT_FILE"

echo "Transcription complete. Saved to: $TRANSCRIPT_FILE"

# Step 3: Summarize the transcript
echo "Generating summary..."

# Option 1: Use fabric if available
if command -v fabric &> /dev/null; then
    fabric --summarize "$TRANSCRIPT_FILE" > "$SUMMARY_FILE"
# Option 2: Use the Python summarizer
elif [ -f "summarizer/summarize.py" ]; then
    python3 summarizer/summarize.py "$TRANSCRIPT_FILE" > "$SUMMARY_FILE.json"
    # Extract summary from JSON
    python3 -c "import json; print(json.load(open('$SUMMARY_FILE.json'))['summary'])" > "$SUMMARY_FILE"
    rm "$SUMMARY_FILE.json"
# Option 3: Use a simple bash-based summarizer
else
    # Count words in transcript
    TOTAL_WORDS=$(wc -w < "$TRANSCRIPT_FILE")
    # Take first sentence of each paragraph (similar to ytr.sh)
    cat "$TRANSCRIPT_FILE" |
    awk 'BEGIN{RS="\n\n";ORS="\n"}{print $0}' |
    sed 's/\([.!?]\) /\1\n/g' |
    awk 'NR==1 {print; next} /^[A-Z]/ {print}' |
    # Limit to ~20% of original word count
    head -n $(($TOTAL_WORDS / 5)) > "$SUMMARY_FILE"
fi

# Print summary
echo -e "\nSummary:"
echo "========="
cat "$SUMMARY_FILE"

echo -e "\nFiles saved:"
echo "- Full transcript: $TRANSCRIPT_FILE"
echo "- Summary: $SUMMARY_FILE"
echo "- Audio: $AUDIO_FILE"
