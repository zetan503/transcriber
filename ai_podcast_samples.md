# AI Podcast Samples for Testing

Here are several AI podcast episodes on YouTube that you can use to test the podcast transcription tools:

## Lex Fridman Podcast (YouTube)

1. **Demis Hassabis: DeepMind - AI, Superintelligence & the Future of Humanity**
   - URL: https://www.youtube.com/watch?v=Gfr50f6ZBvo
   - Description: Interview with the CEO of DeepMind discussing artificial intelligence and its future

2. **Yann LeCun: Deep Learning, ConvNets, and Self-Supervised Learning**
   - URL: https://www.youtube.com/watch?v=SGSOCuByo24
   - Description: Facebook's Chief AI Scientist discusses deep learning techniques

3. **Andrew Ng: Deep Learning, Education, and Real-World AI**
   - URL: https://www.youtube.com/watch?v=0jspaMLxBig
   - Description: AI pioneer discusses the state and future of artificial intelligence

## TED Talks on AI (YouTube)

1. **How AI Could Compose a Personalized Soundtrack to Your Life | Pierre Barreau**
   - URL: https://www.youtube.com/watch?v=wYb3Wimn01s
   - Description: Short talk about AI in music composition (good for quick testing)

2. **Can AI Evolve in the Way That Humans Have? | Joanna Bryson**
   - URL: https://www.youtube.com/watch?v=CZuMBHOjgSw
   - Description: Discussion about AI evolution and ethics

## Example Usage

To transcribe and summarize one of these podcasts using the bash script:

```bash
./podcast-transcribe.sh https://www.youtube.com/watch?v=wYb3Wimn01s
```

To use the Python script with a larger model for better transcription quality:

```bash
./podcast_transcriber.py https://www.youtube.com/watch?v=wYb3Wimn01s --model medium --sentences 15
```

## Notes

- These YouTube links have been verified to work with yt-dlp
- The TED talks are shorter (5-15 minutes) and recommended for initial testing
- The Lex Fridman podcast episodes are longer (1-3 hours) and provide more comprehensive content for thorough testing
