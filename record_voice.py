#!/usr/bin/env python3
"""
Voice Sample Recording and Preprocessing Script
Helps create high-quality voice samples for voice cloning.
"""

import argparse
import os
import sys
import wave
from pathlib import Path
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.effects import normalize
import librosa
import scipy.signal as signal


class VoiceRecorder:
    """Class for recording and preprocessing voice samples."""
    
    def __init__(self):
        """Initialize the voice recorder."""
        self.target_sample_rate = 22050  # Optimal for XTTS
        self.channels = 1  # Mono
        self.chunk_size = 1024
        
    def record_audio(self, duration=15, output_path="voices/recorded_voice.wav"):
        """Record audio from microphone."""
        try:
            import pyaudio
        except ImportError:
            print("Error: pyaudio not installed.")
            print("Install with: pip install pyaudio")
            print("\nAlternatively, use --input to preprocess an existing audio file.")
            sys.exit(1)
        
        print(f"\n=== Voice Recording ===")
        print(f"Duration: {duration} seconds")
        print(f"Sample rate: {self.target_sample_rate} Hz")
        print(f"Format: Mono WAV")
        print("\nTips for best quality:")
        print("  • Speak clearly and naturally")
        print("  • Use complete sentences")
        print("  • Avoid background noise")
        print("  • Stay close to the microphone (but not too close)")
        print("  • Express some emotion/variation in your speech")
        print("\nRecording will start in 3 seconds...")
        
        import time
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("🎤 RECORDING NOW - Speak naturally!")
        
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        # Open stream
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.target_sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        frames = []
        num_chunks = int(self.target_sample_rate / self.chunk_size * duration)
        
        # Record audio
        try:
            for i in range(num_chunks):
                data = stream.read(self.chunk_size)
                frames.append(data)
                
                # Progress indicator
                progress = (i + 1) / num_chunks * 100
                bars = '█' * int(progress / 2) + '░' * (50 - int(progress / 2))
                print(f"\r{bars} {progress:.0f}%", end='', flush=True)
            
            print("\n✓ Recording complete!")
            
        except KeyboardInterrupt:
            print("\n⚠ Recording interrupted")
        finally:
            # Clean up
            stream.stop_stream()
            stream.close()
            audio.terminate()
        
        # Save raw recording
        temp_path = output_path + ".temp.wav"
        wf = wave.open(temp_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.target_sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"Processing audio...")
        
        # Process the recording
        self.process_audio(temp_path, output_path)
        
        # Remove temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        print(f"✓ Voice sample saved: {output_path}")
        
        return output_path
    
    def process_audio(self, input_path, output_path):
        """Process and optimize audio for voice cloning."""
        print(f"\nProcessing audio file: {input_path}")
        
        # Load audio
        audio = AudioSegment.from_file(input_path)
        
        # Convert to mono if stereo
        if audio.channels > 1:
            print("  • Converting to mono...")
            audio = audio.set_channels(1)
        
        # Normalize audio
        print("  • Normalizing volume...")
        audio = normalize(audio)
        
        # Export to WAV at target sample rate
        temp_wav = output_path + ".processing.wav"
        audio.export(temp_wav, format='wav', parameters=['-ar', str(self.target_sample_rate)])
        
        # Load with librosa for advanced processing
        y, sr = librosa.load(temp_wav, sr=self.target_sample_rate)
        
        # Remove silence from beginning and end
        print("  • Trimming silence...")
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)
        
        # Apply gentle noise reduction
        print("  • Reducing noise...")
        y_denoised = self.reduce_noise(y_trimmed, sr)
        
        # Ensure audio is not too quiet or too loud
        y_normalized = librosa.util.normalize(y_denoised)
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save processed audio
        sf.write(output_path, y_normalized, sr)
        
        # Clean up temp file
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        
        # Validate the processed audio
        self.validate_audio(output_path)
    
    def reduce_noise(self, audio, sr):
        """Apply basic noise reduction to audio."""
        # Simple spectral gating noise reduction
        # Estimate noise from quietest parts
        noise_threshold = np.percentile(np.abs(audio), 10)
        
        # Apply soft threshold
        audio_denoised = np.where(
            np.abs(audio) > noise_threshold,
            audio,
            audio * 0.1  # Reduce but don't completely eliminate
        )
        
        return audio_denoised
    
    def validate_audio(self, audio_path):
        """Validate audio file meets requirements."""
        print("\n=== Audio Validation ===")
        
        # Load audio info
        audio = AudioSegment.from_file(audio_path)
        y, sr = librosa.load(audio_path)
        
        duration = len(audio) / 1000.0
        file_size = os.path.getsize(audio_path) / 1024  # KB
        
        print(f"Duration: {duration:.1f} seconds")
        print(f"Sample rate: {sr} Hz")
        print(f"Channels: {audio.channels}")
        print(f"File size: {file_size:.1f} KB")
        
        # Check duration
        if duration < 6:
            print(f"⚠ Warning: Audio is short ({duration:.1f}s). Recommended: 6-30s")
            print("  Shorter samples may result in lower quality cloning.")
        elif duration > 30:
            print(f"⚠ Warning: Audio is long ({duration:.1f}s). Will use first 30s.")
            print("  Longer samples don't necessarily improve quality.")
        else:
            print(f"✓ Duration is optimal!")
        
        # Check for clipping
        if np.max(np.abs(y)) > 0.99:
            print("⚠ Warning: Audio may be clipping (too loud)")
        else:
            print("✓ Audio levels are good")
        
        # Check signal-to-noise ratio estimate
        rms = librosa.feature.rms(y=y)[0]
        snr_estimate = 20 * np.log10(np.max(rms) / (np.mean(rms) + 1e-10))
        
        if snr_estimate < 10:
            print(f"⚠ Warning: Audio may have too much noise (SNR: {snr_estimate:.1f} dB)")
        else:
            print(f"✓ Audio quality is good (SNR estimate: {snr_estimate:.1f} dB)")
        
        print("\n✓ Validation complete!")
        return True
    
    def split_long_audio(self, input_path, max_duration=30):
        """Split long audio file into optimal chunks."""
        audio = AudioSegment.from_file(input_path)
        duration = len(audio) / 1000.0
        
        if duration <= max_duration:
            print(f"Audio is {duration:.1f}s - no splitting needed")
            return [input_path]
        
        print(f"Audio is {duration:.1f}s - splitting into {max_duration}s chunks...")
        
        # Calculate number of chunks
        num_chunks = int(np.ceil(duration / max_duration))
        chunk_duration_ms = int(max_duration * 1000)
        
        output_paths = []
        base_path = Path(input_path)
        
        for i in range(num_chunks):
            start_ms = i * chunk_duration_ms
            end_ms = min((i + 1) * chunk_duration_ms, len(audio))
            
            chunk = audio[start_ms:end_ms]
            
            # Create output path
            output_path = base_path.parent / f"{base_path.stem}_part{i+1}{base_path.suffix}"
            chunk.export(output_path, format='wav')
            
            output_paths.append(str(output_path))
            print(f"  ✓ Created: {output_path}")
        
        return output_paths


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Record or preprocess voice samples for voice cloning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record new voice sample (15 seconds)
  python record_voice.py --output voices/my_voice.wav
  
  # Record with custom duration
  python record_voice.py --output voices/my_voice.wav --duration 20
  
  # Preprocess existing audio file
  python record_voice.py --input my_recording.mp3 --output voices/my_voice.wav
  
  # Split long audio into optimal chunks
  python record_voice.py --input long_audio.wav --output voices/voice.wav --split

Tips for best results:
  • 10-15 seconds is the sweet spot for voice cloning
  • Speak naturally with some emotional variation
  • Record in a quiet environment
  • Use complete sentences
  • Keep consistent distance from microphone
        """
    )
    
    parser.add_argument('--input', '-i',
                       help='Input audio file to preprocess (instead of recording)')
    parser.add_argument('--output', '-o', required=True,
                       help='Output file path (e.g., voices/my_voice.wav)')
    parser.add_argument('--duration', '-d', type=int, default=15,
                       help='Recording duration in seconds (default: 15)')
    parser.add_argument('--split', action='store_true',
                       help='Split long audio into 30s chunks')
    
    args = parser.parse_args()
    
    # Create voices directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize recorder
    recorder = VoiceRecorder()
    
    try:
        if args.input:
            # Preprocess existing audio
            if not os.path.exists(args.input):
                print(f"Error: Input file not found: {args.input}")
                sys.exit(1)
            
            if args.split:
                # Split and process each chunk
                chunks = recorder.split_long_audio(args.input)
                for i, chunk in enumerate(chunks):
                    output = str(output_path.parent / f"{output_path.stem}_chunk{i+1}.wav")
                    recorder.process_audio(chunk, output)
                    print(f"✓ Processed chunk: {output}")
            else:
                # Process single file
                recorder.process_audio(args.input, args.output)
                print(f"\n✓ Success! Voice sample ready: {args.output}")
        else:
            # Record new audio
            recorder.record_audio(args.duration, args.output)
            print(f"\n✓ Success! Voice sample ready: {args.output}")
            print(f"\nYou can now use this voice with:")
            print(f'  python voice_cloning.py "Your text here" --voice {output_path.stem}')
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

