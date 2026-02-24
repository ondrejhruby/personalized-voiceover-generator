# 🎙️ Voice Cloning for TikTok Voiceovers

A high-quality, open-source voice cloning system using **Coqui XTTS v2** to create realistic voiceovers for TikTok videos. Clone any voice from just 6-30 seconds of audio and generate natural-sounding speech from text.

## ✨ Features

- **🎯 High-Quality Voice Cloning**: State-of-the-art XTTS v2 model for realistic voice synthesis
- **⚡ Fast Generation**: Real-time or near real-time audio generation (with GPU)
- **🌍 Multi-lingual**: Supports 15+ languages including English, Spanish, French, German, and more
- **💰 100% Free & Open Source**: No API costs, runs entirely on your machine
- **🔒 Privacy-Friendly**: All processing happens locally
- **📦 Easy to Use**: Simple command-line interface with sensible defaults
- **🎚️ TikTok-Optimized**: Output audio is automatically optimized for TikTok

## 🎬 Perfect For

- TikTok voiceovers
- YouTube videos
- Podcasts
- Audiobooks
- Educational content
- Any content requiring consistent voice narration

## 📋 Requirements

### System Requirements

**Minimum:**
- Python 3.8 or higher
- 4GB RAM
- 2GB storage space
- CPU (Intel/AMD/Apple Silicon)

**Recommended:**
- Python 3.9+
- 8GB+ RAM
- NVIDIA GPU with 4GB+ VRAM (for faster generation)
- 5GB storage space

### Operating System
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux
- ✅ Windows 10/11

## 🚀 Installation

### 1. Clone or Download This Repository

```bash
cd /path/to/your/projects
# If you haven't already, you're in the right place!
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** On first run, the XTTS v2 model (~500MB) will be automatically downloaded.

### 3. (Optional) Install PyAudio for Recording

If you want to record voice samples directly:

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Windows:**
```bash
pip install pyaudio
```

If PyAudio installation fails, you can skip it and use existing audio files instead.

## 📖 Quick Start Guide

### Step 1: Prepare a Voice Sample

You need 6-30 seconds of clear audio of the voice you want to clone.

**Option A: Record a new sample**
```bash
python record_voice.py --output voices/my_voice.wav --duration 15
```

**Option B: Use an existing audio file**
```bash
python record_voice.py --input existing_audio.mp3 --output voices/my_voice.wav
```

**Tips for best quality:**
- 📏 **Duration**: 10-15 seconds is optimal
- 🗣️ **Content**: Speak in complete sentences
- 🎵 **Variation**: Include some emotional/tonal variation
- 🔇 **Environment**: Record in a quiet space
- 🎤 **Microphone**: Stay at consistent distance

### Step 2: Generate Voiceover

**From text:**
```bash
python voice_cloning.py "Hello! This is my cloned voice speaking." --voice my_voice
```

**From a text file:**
```bash
python voice_cloning.py --input script.txt --voice my_voice --output tiktok_voiceover.wav
```

**Batch process multiple files:**
```bash
python voice_cloning.py --batch texts_folder/ --voice my_voice
```

### Step 3: Use in Your TikTok Video

The generated audio file will be in the `output/` directory, ready to import into your video editor or directly into TikTok!

## 🎛️ Advanced Usage

### Generate in Different Languages

```bash
# Spanish
python voice_cloning.py "¡Hola mundo!" --voice my_voice --language es

# French
python voice_cloning.py "Bonjour le monde!" --voice my_voice --language fr

# German
python voice_cloning.py "Hallo Welt!" --voice my_voice --language de
```

**Supported languages:** en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko

### Adjust Generation Parameters

```bash
# Faster speech
python voice_cloning.py "Your text" --voice my_voice --speed 1.3

# More creative/varied output
python voice_cloning.py "Your text" --voice my_voice --temperature 0.9

# More consistent/robotic output
python voice_cloning.py "Your text" --voice my_voice --temperature 0.3
```

### Batch Processing

Create a folder with multiple `.txt` files:

```
texts/
  ├── intro.txt
  ├── main_content.txt
  └── outro.txt
```

Then process all at once:

```bash
python voice_cloning.py --batch texts/ --voice my_voice
```

Each file will generate a corresponding audio file in `output/`.

## ⚙️ Configuration

Edit `config.yaml` to customize default settings:

```yaml
voices:
  my_voice:
    sample_path: voices/my_voice.wav
    description: "My personal voice"
    language: en

model:
  temperature: 0.7  # 0.1-1.0 (higher = more varied)
  speed: 1.0        # Speech speed multiplier

output:
  format: wav       # 'wav' or 'mp3'
  sample_rate: 44100
  normalize: true   # Normalize volume
```

## 📁 Project Structure

```
VoiceCloning/
├── voice_cloning.py      # Main script for generating voiceovers
├── record_voice.py       # Script for recording/preprocessing voice samples
├── config.yaml           # Configuration file
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── voices/              # Store your voice samples here
│   └── my_voice.wav
└── output/              # Generated audio files appear here
    └── output_1.wav
```

## 🎯 Usage Examples

### Example 1: TikTok Product Review Voiceover

```bash
# Record your voice sample
python record_voice.py --output voices/review_voice.wav --duration 12

# Create voiceover from script
python voice_cloning.py --input product_review.txt --voice review_voice --output tiktok_review.wav
```

### Example 2: Multi-language Content

```bash
# English version
python voice_cloning.py --input script.txt --voice my_voice --language en --output video_en.wav

# Spanish version
python voice_cloning.py --input script_es.txt --voice my_voice --language es --output video_es.wav
```

### Example 3: Series of TikTok Videos

```bash
# Batch process all your scripts
python voice_cloning.py --batch tiktok_scripts/ --voice my_voice

# Output will be in output/ folder:
# - script1_voiceover.wav
# - script2_voiceover.wav
# - script3_voiceover.wav
```

## 🔧 Troubleshooting

### "Model download is slow"
The first time you run the script, it downloads ~500MB. This is normal. Subsequent runs will be fast.

### "CUDA out of memory" error
Your GPU doesn't have enough memory. The script will automatically fall back to CPU mode.

### "PyAudio installation failed"
You can skip PyAudio if you only want to process existing audio files. Use the `--input` flag with `record_voice.py`.

### Audio quality is poor
- Ensure your voice sample is clear with minimal background noise
- Try recording a longer sample (15-20 seconds)
- Make sure you're speaking naturally with some variation
- Check that your sample audio isn't clipped or distorted

### Generated voice doesn't sound like the sample
- Use a longer voice sample (10-15 seconds recommended)
- Ensure the sample has clear, varied speech
- Try adjusting temperature (0.6-0.8 works well for most voices)
- Make sure the sample is preprocessed with `record_voice.py`

### Voice sounds robotic
- Increase temperature: `--temperature 0.8`
- Ensure your voice sample has emotional variation
- Try a different section of your recording as the sample

## 🎨 Tips for Best Results

### Voice Sample Quality
1. **Record in a quiet environment** - Background noise will be cloned too
2. **Speak naturally** - Don't read in a monotone
3. **Use complete sentences** - Better than disconnected words
4. **Show emotion** - Varied tone produces better cloning
5. **Consistent distance** - Stay the same distance from mic

### Generation Quality
1. **Start with defaults** - They work well for most cases
2. **Adjust temperature** - Lower (0.5) for consistency, higher (0.8) for naturalness
3. **Shorter texts** - Break long scripts into paragraphs
4. **Proper punctuation** - Helps with pacing and pauses

### TikTok Optimization
1. **Use WAV format** - Better quality for editing
2. **Keep it short** - TikTok videos are typically 15-60 seconds
3. **Normalize volume** - Enabled by default in config
4. **Test before posting** - Listen to ensure quality

## 🆘 Getting Help

If you encounter issues:

1. Check this README's troubleshooting section
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Try running with `--help` flag for usage information:
   ```bash
   python voice_cloning.py --help
   python record_voice.py --help
   ```

## 📊 Performance

**Generation Speed (approximate):**
- With GPU (RTX 3060+): Real-time or faster (1-2s for a sentence)
- With CPU (modern): 5-10 seconds per sentence
- Apple Silicon (M1/M2): 3-6 seconds per sentence

**Quality:**
- Voice similarity: Excellent (with good sample)
- Naturalness: Very high
- Multi-lingual: Native-like pronunciation

## 🔐 Privacy & Ethics

This tool runs **100% locally** on your machine. No audio is uploaded to any servers.

**Ethical Usage:**
- ✅ Clone your own voice
- ✅ Clone voices with explicit permission
- ✅ Create content for education/entertainment
- ❌ Don't impersonate others without permission
- ❌ Don't create misleading content
- ❌ Don't violate platform terms of service

**Please use this tool responsibly and ethically.**

## 📜 License & Credits

This project uses open-source technologies:
- **Coqui TTS (XTTS v2)**: MPL 2.0 License
- **PyTorch**: BSD License
- Other dependencies: See requirements.txt

**Created for educational and creative purposes.**

## 🎓 Learn More

- [Coqui TTS Documentation](https://docs.coqui.ai/)
- [XTTS v2 Paper](https://arxiv.org/abs/2311.13490)
- [TikTok Audio Guidelines](https://www.tiktok.com/)

## 🚀 What's Next?

Now that you have voice cloning set up:

1. **Record your voice sample** (~10-15 seconds)
2. **Write your script** (save as `.txt` file)
3. **Generate voiceover** (takes seconds!)
4. **Add to your TikTok video**
5. **Share your content!** 🎉

Happy creating! 🎬✨

---

**Pro Tip:** Create multiple voice profiles for different types of content (professional, casual, energetic, etc.) and use them for different video themes!

