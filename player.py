import os
import pygame
import threading
import time
from gtts import gTTS
import tempfile
import pyttsx3 # Added pyttsx3 import

class AudioPlayer:
    def __init__(self):
        self.queue = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.stop_event = threading.Event()
        
        # Audio Settings
        self.engine_type = "gtts" # or "pyttsx3"
        self.voice_id = None
        self.playback_speed = 1.0
        
        # Callback for UI updates
        self.on_paragraph_change = None 
        self.on_finished = None
        
        self._ensure_mixer()

    def _ensure_mixer(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except Exception as e:
                print(f"Mixer Init Error: {e}")

    def set_voice(self, voice_name, pyttsx3_voice_id=None):
        if "Google" in voice_name:
            self.engine_type = "gtts"
        else:
            self.engine_type = "pyttsx3"
            self.voice_id = pyttsx3_voice_id

    def load_text(self, text):
        """Splits text into paragraphs and prepares the queue."""
        self.stop_playing() 
        self.queue = [p.strip() for p in text.split('\n\n') if p.strip()]
        self.current_index = 0
        print(f"Loaded {len(self.queue)} paragraphs.")

    def play(self):
        """Starts playback in a separate thread."""
        if not self.queue:
            return
        
        self._ensure_mixer()
        self.stop_event.clear()
        self.is_playing = True
        self.is_paused = False
        
        threading.Thread(target=self._playback_loop, daemon=True).start()

    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume(self):
        if self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_playing(self):
        self.stop_event.set()
        try:
             pygame.mixer.music.stop()
        except:
             pass
        self.is_playing = False
        self.is_paused = False

    def next_paragraph(self):
        if self.current_index < len(self.queue) - 1:
            self.manual_skip = True
            self.current_index += 1
            pygame.mixer.music.stop() 

    def prev_paragraph(self):
        if self.current_index > 0:
            self.manual_skip = True
            self.current_index -= 1
            pygame.mixer.music.stop()
            
    def repeat_current(self):
        """Replays the current paragraph from start."""
        self.manual_skip = True
        pygame.mixer.music.stop()
        
    def set_speed(self, speed):
        self.playback_speed = speed

    def _generate_audio_pyttsx3(self, text, output_path):
        import pyttsx3
        try:
            # Re-init engine in this thread usually safest or use a global one cautiously
            # pyttsx3 init is cheap.
            engine = pyttsx3.init()
            if self.voice_id:
                engine.setProperty('voice', self.voice_id)
            
            # Speed mapping: 1.0 -> 200 (default), 1.5 -> 300 etc
            # Base rate is usually around 200
            rate = 200 * self.playback_speed
            engine.setProperty('rate', rate)
            
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"Pyttsx3 Gen Error: {e}")
            return False

    def _playback_loop(self):
        self.manual_skip = False
        
        # Ensure mixer
        self._ensure_mixer()

        while self.current_index < len(self.queue) and not self.stop_event.is_set():
            if self.on_paragraph_change:
                self.on_paragraph_change(self.current_index, self.queue[self.current_index])

            text_chunk = self.queue[self.current_index]
            print(f"Generating audio for p{self.current_index} ({self.engine_type})...")
            
            try:
                fd, path = tempfile.mkstemp(suffix='.mp3')
                os.close(fd)
                
                success = False
                
                if self.engine_type == "gtts":
                    tts = gTTS(text=text_chunk, lang='pt')
                    tts.save(path)
                    success = True
                else:
                    # Pyttsx3
                    # It saves wav usually, but we named it mp3 placeholder. 
                    # Pygame mixer plays wav fine.
                    # We should use .wav suffix for pyttsx3 to be safe.
                    os.remove(path)
                    fd, path = tempfile.mkstemp(suffix='.wav')
                    os.close(fd)
                    success = self._generate_audio_pyttsx3(text_chunk, path)
                
                if success:
                    # Frequency hack for gTTS (since pyttsx3 handles speed natively)
                    if self.engine_type == "gtts" and self.playback_speed != 1.0:
                         # Implement frequency capability if desired, skipping for now
                         pass

                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                    
                    self.manual_skip = False 
                    
                    while pygame.mixer.music.get_busy() or self.is_paused:
                        if self.stop_event.is_set():
                            pygame.mixer.music.stop()
                            break
                        if self.manual_skip:
                             break
                        time.sleep(0.1)
                
                # Cleanup
                try:
                    # Wait a tiny bit to ensure release
                    time.sleep(0.1)
                    os.remove(path)
                except:
                    pass
                
                if self.stop_event.is_set():
                    break
                
                if not self.manual_skip:
                     self.current_index += 1
                     
            except Exception as e:
                print(f"Error playing chunk: {e}")
                time.sleep(1) 

        self.is_playing = False
        if self.on_finished:
            self.on_finished()
