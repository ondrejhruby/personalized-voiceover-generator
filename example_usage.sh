#!/bin/bash
# Example Usage Script for Voice Cloning
# This script demonstrates common use cases

echo "=== Voice Cloning Examples ==="
echo ""

# Example 1: Record a voice sample
echo "Example 1: Record a 15-second voice sample"
echo "Command: python record_voice.py --output voices/my_voice.wav --duration 15"
echo ""

# Example 2: Preprocess existing audio
echo "Example 2: Preprocess an existing audio file"
echo "Command: python record_voice.py --input existing_audio.mp3 --output voices/my_voice.wav"
echo ""

# Example 3: Generate from text argument
echo "Example 3: Generate voiceover from text"
echo "Command: python voice_cloning.py \"Hello! This is a test of voice cloning.\" --voice my_voice"
echo ""

# Example 4: Generate from text file
echo "Example 4: Generate from a text file"
echo "Command: python voice_cloning.py --input script.txt --voice my_voice --output tiktok_vo.wav"
echo ""

# Example 5: Different language
echo "Example 5: Generate in Spanish"
echo "Command: python voice_cloning.py \"¡Hola! ¿Cómo estás?\" --voice my_voice --language es"
echo ""

# Example 6: Batch processing
echo "Example 6: Batch process multiple text files"
echo "Command: python voice_cloning.py --batch texts/ --voice my_voice"
echo ""

# Example 7: Adjust parameters
echo "Example 7: Faster speech with more variation"
echo "Command: python voice_cloning.py \"Your text here\" --voice my_voice --speed 1.3 --temperature 0.8"
echo ""

echo "=== Quick Start ==="
echo "1. First, record or prepare your voice sample:"
echo "   python record_voice.py --output voices/my_voice.wav"
echo ""
echo "2. Then generate a voiceover:"
echo "   python voice_cloning.py \"Your text here\" --voice my_voice"
echo ""
echo "3. Check the output/ folder for your generated audio!"
echo ""

