def main_view(self):
        self.page.controls.clear()

        self.main_side_view = Container(
            content=IconButton(
                icon=Icons.ARROW_FORWARD,
                icon_size=30, 
                on_click=self.audio_list
            ),
            alignment=alignment.top_left,
        )
        self.main_record_button = Container(
            content=IconButton(
                icon=Icons.MULTITRACK_AUDIO_ROUNDED, 
                tooltip="Listen", 
                icon_size=300,
                visible=True, 
                on_click=self.record_button_action
            ),
            alignment=alignment.center,
            expand=True
        )
        self.main_popup_menu = Container(
            content=PopupMenuButton( 
                items=[ 
                    PopupMenuItem(
                        content=IconButton(
                            icon=Icons.CREATE, 
                            tooltip="Write lyrics",
                            on_click=self
                        )
                    ), 
                    PopupMenuItem(
                        content=IconButton(
                            icon=Icons.UPLOAD,
                            tooltip="Upload",
                            on_click=self
                        )
                    )
                ]
            ),
            alignment=alignment.top_right,
        )
        self.main_top_control = Container(
            content=Row(
                controls=[
                    self.main_side_view,
                    self.main_popup_menu
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                expand=True
            ),
            expand=True
        )      
        self.animated_switcher = AnimatedSwitcher( 
            content=self.main_record_button, 
            duration=ft.Duration(milliseconds=300), 
            transition=ft.AnimatedSwitcherTransition.FADE
        )       
        self.pause_record_button = ElevatedButton(text="Pause", visible=False, on_click=self.pause_action) 
        self.stop_record_button = ElevatedButton(text="Stop", visible=False, on_click=self.stop_action)
        self.next_button = ElevatedButton(text="Next", visible=False, on_click=self.next_prompt)

        self.feedback_text = Text(visible=False, color=Colors.GREEN, size=20) 
        self.prompt_text = Text(visible=False, color=Colors.BLUE, size=24)

        self.main_record_control = Container( 
            content=Column( 
                controls=[ 
                    Row( 
                        controls=[ 
                            self.pause_record_button, 
                            self.stop_record_button, 
                            self.next_button 
                        ], 
                        alignment=MainAxisAlignment.SPACE_EVENLY 
                    ), 
                    self.feedback_text,  
                    self.prompt_text  
                ] 
            ), 
            expand=True
        )

        self.main_background = Container(
            content=Column(
                controls=[
                    self.main_top_control,
                    self.animated_switcher,
                    self.main_record_control
                ]
            ),
            gradient=LinearGradient(
                colors=[Colors.BLACK, Colors.AMBER],
                begin=alignment.center_left, end=alignment.center_right
            ),
            expand=True
        )
        self.page.controls.append(self.main_background)
        self.page.update()

    def remove_overlay(self, e, content=None):
        if content in self.page.overlay:
            self.page.overlay.remove(content)
            self.page.update()

    def transform_button(self, e):
        pass

    def record_button_action(self, e): 
        self.animated_switcher.content = Container( 
            content=Row( 
                controls=[ 
                    ElevatedButton(text="Record Voice", on_click=self.start_action("record")), 
                    ElevatedButton(text="Clone Voice", on_click=self.start_action("clone"))
                ], 
                alignment=MainAxisAlignment.SPACE_BETWEEN, 
                spacing=10 
            ), 
            alignment=ft.alignment.center, 
            expand=True 
        ) 
        self.page.update()

    def start_action(self, mode):
        self.is_recording_or_cloning = True 
        self.is_paused = False
        self.current_mode = mode
        self.record_data = []

        self.record_wave_bars = [
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.RED),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.GREEN),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.BLUE),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.YELLOW),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.RED),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.GREEN),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.BLUE),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.YELLOW),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.RED),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.GREEN),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.BLUE),
            Container(width=10, height=random.randint(30, 80), bgcolor=Colors.YELLOW)
        ]

        self.record_wave = Container(
            content=Row(
                controls=self.record_wave_bars,
                alignment=MainAxisAlignment.CENTER,
                spacing=5
            ),
            width=150,
            height=70,
            alignment=alignment.center
        )
        self.animated_switcher.content = Container( 
            content=self.record_wave, 
            alignment=ft.alignment.center, 
            expand=True 
        )

        if mode == "record": 
            self.stream = sd.InputStream(callback=self.audio_callback, samplerate=self.sample_rate, channels=1) 
            self.stream.start() 
            self.pause_record_button.visible = True 
            self.stop_record_button.visible = True
            self.feedback_text.value = "Recording in progress..." 
            self.recording_thread = Thread(target=self.update_wave)
            self.recording_thread.start()
        
        elif mode == "clone": 
            self.stream = sd.InputStream(callback=self.audio_callback, samplerate=self.sample_rate, channels=1) 
            self.stream.start() 
            self.feedback_text.value = "Cloning initiated..." 
            self.prompt_text.value = self.text_prompts[self.current_prompt_index] ,
            self.pause_record_button.visible = True 
            self.stop_record_button.visible = True
            self.feedback_text.visible = True 
            self.prompt_text.visible = True
            self.recording_thread = Thread(target=self.update_wave)
            self.recording_thread.start()
        
        self.page.update()

def update_wave(self):
        while self.is_recording_or_cloning:
            if not self.is_paused:
                try:
                    for bar in self.record_wave_bars:
                        bar.height = random.randint(30, 80)
                    self.page.update()
                    time.sleep(0.1)
                except RuntimeError as e: 
                    if str(e) == 'Event loop is closed': 
                        break 
                    else: 
                        raise 
def pause_action(self, e):
        self.is_paused = not self.is_paused
        self.pause_record_button.text = "Continue" if self.is_paused else "Pause"
        self.feedback_text.value = "Paused" if self.is_paused else "Recording in progress..."
        self.page.update()

def stop_action(self, e):
        self.is_recording_or_cloning = False
        self.is_pause = False

        if self.current_mode == "record": 
            self.stream.stop() 
            self.save_audio() 
            
        elif self.current_mode == "clone": 
            self.stream.stop() 
            self.initialize_cloning()

        self.animated_switcher.content = self.main_record_button
        self.pause_record_button.visible = False
        self.pause_record_button.Text = "Pause"
        self.stop_record_button.visible = False
        self.feedback_text.visible = False 
        self.prompt_text.visible = False

        self.page.update()

    
