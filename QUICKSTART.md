# 🚀 Quick Start Guide

Get started with voice cloning in 3 simple steps!

## Step 1: Install Dependencies ⚙️

```bash
pip install -r requirements.txt
```

**Note:** The first run will download the XTTS v2 model (~500MB). This is a one-time download.

## Step 2: Record Your Voice 🎤

Record a 10-15 second sample of clear speech:

```bash
python record_voice.py --output voices/my_voice.wav --duration 15
```

**Tips:**
- Speak naturally with complete sentences
- Record in a quiet environment
- Show some emotional variation in your speech

**Or use an existing audio file:**

```bash
python record_voice.py --input my_audio.mp3 --output voices/my_voice.wav
```

## Step 3: Generate Voiceover 🎬

Generate speech from your text:

```bash
python voice_cloning.py "Hello! This is my cloned voice." --voice my_voice
```

**Or from a text file:**

```bash
python voice_cloning.py --input script.txt --voice my_voice --output tiktok.wav
```

That's it! Your audio file will be in the `output/` folder. 🎉

---

## Common Commands

### Generate with Different Languages
```bash
# Spanish
python voice_cloning.py "Hola mundo" --voice my_voice --language es

# French  
python voice_cloning.py "Bonjour" --voice my_voice --language fr
```

### Adjust Speech Speed
```bash
# Faster
python voice_cloning.py "Your text" --voice my_voice --speed 1.3

# Slower
python voice_cloning.py "Your text" --voice my_voice --speed 0.8
```

### Batch Process Multiple Scripts
```bash
python voice_cloning.py --batch texts_folder/ --voice my_voice
```

---

## Need Help?

- **Full documentation:** See [README.md](README.md)
- **Examples:** Run `./example_usage.sh` to see all usage examples
- **Help commands:**
  ```bash
  python voice_cloning.py --help
  python record_voice.py --help
  ```

## Troubleshooting

**Model download is slow?** First run downloads ~500MB. Be patient! ☕

**Poor audio quality?** 
- Use a better voice sample (clearer, longer)
- Record in a quieter environment
- Use the `record_voice.py` script to preprocess audio

**Voice doesn't sound right?**
- Try adjusting temperature: `--temperature 0.7`
- Use a 10-15 second voice sample
- Ensure sample has emotional variation

---

**Ready to create amazing TikTok voiceovers?** Let's go! 🚀✨

