from coqui_tts.utils.audio import AudioProcessor
from coqui_tts.models.tacotron2 import Tacotron2
from coqui_tts.models.vits import VITS
from pydub import AudioSegment

# 1. Voice cloning

# Load audio and preprocess
audio_path = "input_audio.wav"
ap = AudioProcessor(sample_rate=22050)
wav = ap.load_wav(audio_path)

# Train or fine-tune Tacotron model
model = Tacotron2()
model.train(wav, text="Your sample text")

# Save voice model
model.save("cloned_voice_model.pt")

# 2. Text to Speech 


# Load voice model
model = VITS.load("cloned_voice_model.pt")

# Generate speech
text = "Hello, this is a test."
audio = model.synthesize(text)

# Save audio
with open("output_audio.wav", "wb") as f:
    f.write(audio)

# 3. Export to mp3

# Load WAV and convert to MP3
wav_audio = AudioSegment.from_file("output_audio.wav", format="wav")
wav_audio.export("output_audio.mp3", format="mp3")
