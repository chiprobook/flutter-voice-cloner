class VoiceFeatureExtractor:
    def __init__(self):
        self.tokenizer = Wav2Vec2CTCTokenizer.from_pretrained('facebook/wav2vec2-large-960h')
        self.model = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-large-960h')
        self.sample_rate = 44100
    
    def extract_features(self, audio_data):
        input_values = self.tokenizer(audio_data, return_tensors="pt", sampling_rate=self.sample_rate).input_values
        logits = self.model(input_values).logits
        return logits  # Extracted voice features

class VoiceSynthesizer:
    def __init__(self, cloned_features):
        self.tokenizer = AutoTokenizer.from_pretrained("t5-large")
        self.model = TFAutoModelForSpeechSeq2Seq.from_pretrained("t5-large")
        self.cloned_features = cloned_features  # Use the extracted features
    
    def synthesize_voice(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        outputs = self.model.generate(input_ids, num_beams=5, early_stopping=True, forced_eos_token_id=0, features=self.cloned_features)
        audio = outputs[0].numpy()
        sf.write("synthesized_voice.wav", audio, 16000)
        return audio

class Init_mode:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.horizontal_alignment=CrossAxisAlignment.CENTER
        self.page.update()
        self.is_recording_or_cloning = False
        self.is_paused = False
        self.current_mode = None

        self.record_data = [] 
        self.clone_data = []
        self.sample_rate = 44100

        self.voice_feature_extractor = VoiceFeatureExtractor()
        self.cloned_features = None
        self.text_prompts = ["Hello, how are you?", "The quick brown fox jumps over the lazy dog."] 
        self.current_prompt_index = 0
 
        self.audio_list_view = []
        self.audio_display_view = []

        self.main_view()


def initialize_cloning(self): 
        # AI Cloning logic using Wav2Vec2 model 
        try: 
            tokenizer = Wav2Vec2CTCTokenizer.from_pretrained('facebook/wav2vec2-large-960h') 
            model = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-large-960h') 
            
            # Convert recorded data to suitable format for the model       
            audio_np = np.array(self.record_data, dtype=np.float32)

            if audio_np.shape[0] != self.sample_rate: 
                print(f"Expected sample rate: {self.sample_rate}, got: {audio_np.shape[0]}") 
                    
            # Perform inference
            input_values = tokenizer(audio_np, return_tensors="pt", sampling_rate=self.sample_rate).input_values 
            logits = model(input_values).logits 
            predicted_ids = torch.argmax(logits, dim=-1) 
            
            # Decode predicted text 
            transcription = tokenizer.batch_decode(predicted_ids)[0] 
            
            if transcription.strip().lower() == self.text_prompts[self.current_prompt_index].strip().lower(): 
                self.feedback_text.value = "Correct, moving to next word." 
                self.current_prompt_index += 1 
                if self.current_prompt_index < len(self.text_prompts): 
                    self.prompt_text.value = self.text_prompts[self.current_prompt_index] 
                else: 
                    self.feedback_text.value = "All words recorded successfully." 
                    self.save_cloned_voice(transcription, audio_np)
                    self.stop_action(None) 
            else: 
                self.feedback_text.value = "Incorrect, please repeat."
            
            self.cloned_features = self.voice_feature_extractor.extract_features(audio_np)
        except Exception as e: 
            Messagebox(Text(f"Error in cloning process: {e}"), self.page) 
            
def next_prompt(self, e): 
        # Move to the next prompt manually (for testing or user control) 
        self.current_prompt_index += 1 
        if self.current_prompt_index < len(self.text_prompts): 
            self.prompt_text.value = self.text_prompts[self.current_prompt_index] 
            self.feedback_text.value = "Next prompt displayed." 
        else: 
            self.feedback_text.value = "All prompts completed." 
            self.stop_action(None) 
        self.page.update()

def synthesize_new_content(self, text):
        # Synthesize new content using the cloned voice features
        voice_synthesizer = VoiceSynthesizer(self.cloned_features)
        synthesized_audio = voice_synthesizer.synthesize_voice(text)
        return synthesized_audio

def play_audio(self, file_path):
        data, fs = sf.read(file_path)
        sd.play(data, fs)
        sd.wait()

def load_audio_playback(self, vocal_file):
        self.page.overlay.clear()
        self.load_playback_back = IconButton(icon=Icons.CANCEL, on_click=lambda e: self.remove_overlay(e, self.recorded_content))
        
        self.transform_playback = ElevatedButton(text="Transfrom", on_click=self)
        self.save_playback = ElevatedButton(text="Save", on_click=lambda e: self.prompt_to_save)
        
        self.playback_animation = Container(
            content=Text("Playback animation initializing......"),
            alignment=alignment.center_left,
            expand=True
        )

        self.top_playkback_control = Container(
            content=Row(
                controls=[
                    self.transform_playback,
                    self.save_playback
                ],
                alignment=MainAxisAlignment.END,
                expand=True
            ),
            expand=True
        )
        self.playback_pause = IconButton(icon=Icons.PAUSE, on_click=self) 
        self.playback_play = IconButton(icon=Icons.PLAY_CIRCLE, on_click=self.play_audio(vocal_file))
        self.playback_stop = IconButton(icon=Icons.STOP_CIRCLE, on_click=self)
        
        self.playack_controls = Container(
            content=Row(
                controls=[
                    self.playback_pause,
                    self.playback_play,
                    self.palyback_stop
                ],
                alignment=alignment.bottom_center,
                expand=True
            ),
            expand=True
        )
        self.load_playback = Container(
            content=Container(
                content=Column(
                    controls=[
                        self.top_playback_control,
                        self.playback_animation,
                        self.playback_controls
                    ],
                    alignment=CrossAxisAlignment.STRETCH
                )
            ),
            width=self.page.width * 0.9,
            height=self.page.height * 0.6,
            padding=20,
            border_radius=10,
            bgcolor=Colors.WHITE,
            shadow=BoxShadow(blur_radius=10, spread_radius=2, color=Colors.BLACK87)
        )
        self.page.overlay.append(self.load_playback)
        self.page.update()

if __name__ =="__main__":
    ft.app(target=Init_mode)

