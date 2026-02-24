#!/usr/bin/env python3
"""
Voice Cloning Script using Coqui XTTS v2
Generates realistic voiceovers from text using a cloned voice.
"""

import argparse
import os
import sys
from pathlib import Path
import yaml
import torch
import torchaudio
from TTS.api import TTS
from pydub import AudioSegment
import soundfile as sf
import numpy as np
from tqdm import tqdm


class VoiceCloner:
    """Main class for voice cloning and TTS generation."""
    
    def __init__(self, config_path="config.yaml"):
        """Initialize the voice cloner with configuration."""
        self.config = self.load_config(config_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = None
        print(f"Using device: {self.device}")
        
    def load_config(self, config_path):
        """Load configuration from YAML file."""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                # Handle case where YAML file is empty or returns None
                if config is None:
                    config = {}
        else:
            config = {}
        
        # Ensure we have default structure
        if not isinstance(config, dict):
            config = {}
        
        # Set defaults if missing
        defaults = {
            'voices': {},
            'model': {
                'name': 'tts_models/multilingual/multi-dataset/xtts_v2',
                'temperature': 0.7,
                'speed': 1.0
            },
            'output': {
                'format': 'wav',
                'sample_rate': 44100,
                'normalize': True
            }
        }
        
        # Merge defaults with loaded config
        for key, value in defaults.items():
            if key not in config:
                config[key] = value
            elif isinstance(value, dict) and isinstance(config[key], dict):
                # Deep merge for nested dicts
                for subkey, subvalue in value.items():
                    if subkey not in config[key]:
                        config[key][subkey] = subvalue
        
        return config
    
    def initialize_model(self):
        """Initialize the XTTS v2 model."""
        if self.tts is None:
            print("Loading XTTS v2 model... (This may take a while on first run)")
            model_name = self.config['model']['name']
            self.tts = TTS(model_name).to(self.device)
            print("Model loaded successfully!")
    
    def get_voice_sample_path(self, voice_name):
        """Get the path to a voice sample."""
        # Ensure config is a dict
        if not isinstance(self.config, dict):
            self.config = {}
        
        # Check if voice is in config
        voices = self.config.get('voices', {})
        if isinstance(voices, dict) and voice_name in voices:
            return voices[voice_name].get('sample_path')
        
        # Check in voices directory
        voices_dir = Path('voices')
        for ext in ['.wav', '.mp3', '.flac']:
            voice_path = voices_dir / f"{voice_name}{ext}"
            if voice_path.exists():
                return str(voice_path)
        
        raise FileNotFoundError(f"Voice sample '{voice_name}' not found. "
                            f"Please add it to voices/ directory or config.yaml")
    
    def validate_voice_sample(self, audio_path):
        """Validate voice sample meets requirements."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load audio to check duration
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000.0  # Convert to seconds
        
        if duration < 3:
            print(f"Warning: Voice sample is {duration:.1f}s. Recommended: 6-30s for best results.")
        elif duration < 6:
            print(f"Voice sample is {duration:.1f}s. Acceptable, but 10-15s is optimal.")
        elif duration > 30:
            print(f"Voice sample is {duration:.1f}s. Will use first 30 seconds.")
        else:
            print(f"Voice sample duration: {duration:.1f}s - Good!")
        
        return True
    
    def generate_speech(self, text, voice_sample_path, output_path=None, 
                       language="en", temperature=None, speed=None):
        """Generate speech from text using voice cloning."""
        self.initialize_model()
        
        # Validate voice sample
        self.validate_voice_sample(voice_sample_path)
        
        # Use config values if not specified
        if temperature is None:
            temperature = self.config['model'].get('temperature', 0.7)
        if speed is None:
            speed = self.config['model'].get('speed', 1.0)
        
        # Generate output path if not specified
        if output_path is None:
            output_dir = Path('output')
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"output_{len(list(output_dir.glob('*'))) + 1}.wav"
        
        print(f"\nGenerating speech...")
        print(f"Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"Voice sample: {voice_sample_path}")
        print(f"Language: {language}")
        
        try:
            # Generate speech with XTTS v2
            wav = self.tts.tts(
                text=text,
                speaker_wav=voice_sample_path,
                language=language,
                speed=speed
            )
            
            # Convert to numpy array if needed
            if isinstance(wav, torch.Tensor):
                wav = wav.cpu().numpy()
            
            # Get sample rate from the model
            sample_rate = self.tts.synthesizer.output_sample_rate
            
            # Save initial audio
            temp_path = str(output_path) + ".temp.wav"
            sf.write(temp_path, wav, sample_rate)
            
            # Post-process audio
            self.post_process_audio(temp_path, output_path)
            
            # Remove temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            print(f"✓ Audio generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            raise
    
    def post_process_audio(self, input_path, output_path):
        """Post-process audio for TikTok optimization."""
        audio = AudioSegment.from_wav(input_path)
        
        # Normalize volume if configured
        if self.config['output'].get('normalize', True):
            audio = self.normalize_audio(audio)
        
        # Resample to target sample rate
        target_rate = self.config['output'].get('sample_rate', 44100)
        if audio.frame_rate != target_rate:
            audio = audio.set_frame_rate(target_rate)
        
        # Export in desired format
        output_format = self.config['output'].get('format', 'wav')
        if output_format == 'mp3':
            output_path = str(output_path).replace('.wav', '.mp3')
            audio.export(output_path, format='mp3', bitrate='192k')
        else:
            audio.export(output_path, format='wav')
    
    def normalize_audio(self, audio):
        """Normalize audio volume."""
        # Target loudness in dBFS (TikTok optimized)
        target_dBFS = -14.0
        change_in_dBFS = target_dBFS - audio.dBFS
        return audio.apply_gain(change_in_dBFS)
    
    def batch_generate(self, input_dir, voice_name, language="en"):
        """Generate speech for multiple text files."""
        input_path = Path(input_dir)
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_dir}")
        
        # Get voice sample path
        voice_sample_path = self.get_voice_sample_path(voice_name)
        
        # Find all text files
        text_files = list(input_path.glob('*.txt'))
        if not text_files:
            print(f"No .txt files found in {input_dir}")
            return
        
        print(f"Found {len(text_files)} text files to process")
        
        # Process each file
        for text_file in tqdm(text_files, desc="Processing files"):
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            if not text:
                print(f"Skipping empty file: {text_file}")
                continue
            
            # Generate output filename
            output_filename = text_file.stem + '_voiceover.wav'
            output_path = Path('output') / output_filename
            
            try:
                self.generate_speech(text, voice_sample_path, output_path, language)
            except Exception as e:
                print(f"Error processing {text_file}: {e}")
                continue


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate voiceovers using voice cloning (XTTS v2)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from text argument
  python voice_cloning.py "Hello world!" --voice my_voice
  
  # Generate from text file
  python voice_cloning.py --input script.txt --voice my_voice --output output.wav
  
  # Batch process multiple files
  python voice_cloning.py --batch texts/ --voice my_voice --language en
  
  # Specify language
  python voice_cloning.py "Bonjour!" --voice my_voice --language fr
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('text', nargs='?', help='Text to convert to speech')
    input_group.add_argument('--input', '-i', help='Input text file path')
    input_group.add_argument('--batch', '-b', help='Process all .txt files in directory')
    
    # Voice options
    parser.add_argument('--voice', '-v', required=True, 
                       help='Voice name (from config.yaml or voices/ directory)')
    parser.add_argument('--language', '-l', default='en',
                       choices=['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 
                               'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'ja', 'hu', 'ko'],
                       help='Language code (default: en)')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output file path (for single file mode)')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Configuration file path (default: config.yaml)')
    
    # Generation options
    parser.add_argument('--temperature', '-t', type=float,
                       help='Generation temperature (0.1-1.0, default from config)')
    parser.add_argument('--speed', '-s', type=float,
                       help='Speech speed multiplier (default from config)')
    
    args = parser.parse_args()
    
    # Initialize voice cloner
    try:
        cloner = VoiceCloner(args.config)
    except Exception as e:
        print(f"Error initializing voice cloner: {e}")
        sys.exit(1)
    
    # Get voice sample path
    try:
        voice_sample_path = cloner.get_voice_sample_path(args.voice)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Process based on input mode
    try:
        if args.batch:
            # Batch mode
            cloner.batch_generate(args.batch, args.voice, args.language)
        else:
            # Single file mode
            if args.text:
                text = args.text
            else:
                # Read from file
                with open(args.input, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
            
            if not text:
                print("Error: Text is empty")
                sys.exit(1)
            
            output_path = cloner.generate_speech(
                text=text,
                voice_sample_path=voice_sample_path,
                output_path=args.output,
                language=args.language,
                temperature=args.temperature,
                speed=args.speed
            )
            
            print(f"\n✓ Success! Audio saved to: {output_path}")
            print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

