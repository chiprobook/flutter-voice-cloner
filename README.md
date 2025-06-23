🚀 Features
Voice Feature Extraction Uses Facebook’s Wav2Vec2 model to extract deep speech features from raw audio.

AI Voice Cloning Guides you through a text-prompted recording flow, verifies transcription accuracy, then generates a feature vector representing your voice.

Text-to-Speech & Singing Synthesis Leverages a T5-derived seq2seq speech model to generate new audio in your cloned voice—supports plain speech and singing.

Interactive Flet UI Cross-platform desktop UI for recording, cloning, playback, and saving audio files.

Session-driven Prompt Flow Multi-step recording prompts with live feedback: “Correct, moving to next word” or “Incorrect, please repeat.”

Create & activate a virtual environment

bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate.bat   # Windows
Install dependencies

bash
pip install -r requirements.txt
requirements.txt should include:

flet
torch
transformers
soundfile
sounddevice
numpy
🎬 Usage
Run the app:

bash
python app.py
The UI will launch. Follow on-screen prompts to:

Record yourself reading predefined sentences.

Get real-time feedback on transcription accuracy.

Auto-clone your voice once all prompts are correct.

Enter any text to synthesize new speech or singing in your cloned voice.

Play back, transform, or save the generated audio.

🛠 Key Components
VoiceFeatureExtractor
python
from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2ForCTC

extractor = VoiceFeatureExtractor()
logits = extractor.extract_features(audio_numpy_array)
VoiceSynthesizer
python
from transformers import AutoTokenizer, TFAutoModelForSpeechSeq2Seq

synth = VoiceSynthesizer(cloned_features)
wav = synth.synthesize_voice("Hello, world!")
Init_mode (Flet UI)
Manages recording sessions, transcription checks, cloning, and playback overlays.

Core methods:

initialize_cloning()

next_prompt()

synthesize_new_content(text)

play_audio(file_path)

load_audio_playback(vocal_file)
