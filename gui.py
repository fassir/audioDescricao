import customtkinter as ctk
import threading
import os
import time
from tkinter import filedialog
from bot import ConversationBot
from player import AudioPlayer
from document_utils import extract_text_from_file
from audio_utils import record_audio

import json

# Configuration
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
BOOKMARK_FILE = "bookmarks.json"

class AudioDescApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AudioDesc Pro - Leitor Inteligente")
        self.geometry("900x700")
        
        self.bookmarks = self.load_bookmarks()
        
        # Layout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AudioDesc", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_load = ctk.CTkButton(self.sidebar_frame, text="Abrir PDF/Txt", command=self.load_document)
        self.btn_load.grid(row=1, column=0, padx=20, pady=10)

        self.model_var = ctk.StringVar(value="llama3")
        self.model_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["llama3", "mistral", "gemma"], variable=self.model_var)
        self.model_menu.grid(row=2, column=0, padx=20, pady=10)

        # Accessibility Controls
        self.lbl_access = ctk.CTkLabel(self.sidebar_frame, text="Acessibilidade", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_access.grid(row=3, column=0, padx=20, pady=(20, 10))

        self.font_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.font_frame.grid(row=4, column=0, padx=20, pady=5)
        
        self.btn_font_dec = ctk.CTkButton(self.font_frame, text="A-", width=40, command=self.decrease_font)
        self.btn_font_dec.pack(side="left", padx=5)
        
        self.btn_font_inc = ctk.CTkButton(self.font_frame, text="A+", width=40, command=self.increase_font)
        self.btn_font_inc.pack(side="left", padx=5)

        self.theme_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"], command=self.change_theme)
        self.theme_menu.set("System")
        self.theme_menu.grid(row=5, column=0, padx=20, pady=10)

        # Main Content
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1) 
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Text Display Area (Reading View)
        self.font_size = 16
        self.text_display = ctk.CTkTextbox(self.main_frame, width=600, font=("Arial", self.font_size))
        self.text_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Controls Area
        self.controls_frame = ctk.CTkFrame(self.main_frame, height=100)
        self.controls_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.btn_prev = ctk.CTkButton(self.controls_frame, text="⏮ Anterior", width=80, command=self.prev_paragraph)
        self.btn_prev.pack(side="left", padx=20, pady=20)
        
        self.btn_play = ctk.CTkButton(self.controls_frame, text="▶ Ler", width=80, fg_color="green", command=self.toggle_play)
        self.btn_play.pack(side="left", padx=10, pady=20)
        
        self.btn_next = ctk.CTkButton(self.controls_frame, text="Próximo ⏭", width=80, command=self.next_paragraph)
        self.btn_next.pack(side="left", padx=20, pady=20)

        # Speed Control
        self.speed_label = ctk.CTkLabel(self.controls_frame, text="Velocidade:")
        self.speed_label.pack(side="left", padx=5)
        self.speed_var = ctk.StringVar(value="1.0x")
        self.speed_menu = ctk.CTkOptionMenu(self.controls_frame, values=["1.0x", "1.25x", "1.5x", "2.0x"], variable=self.speed_var, width=80, command=self.change_speed)
        self.speed_menu.pack(side="left", padx=5)

        self.btn_voice = ctk.CTkButton(self.controls_frame, text="🎤 Comando de Voz", fg_color="#D32F2F", hover_color="#B71C1C", command=self.start_voice_command)
        self.btn_voice.pack(side="right", padx=20, pady=20)

        self.btn_export = ctk.CTkButton(self.controls_frame, text="💾 MP3", width=60, fg_color="#0097A7", hover_color="#006064", command=self.start_export)
        self.btn_export.pack(side="right", padx=10, pady=20)

        # Custom Key Bindings
        self.bind("<Left>", lambda e: self.prev_paragraph())
        self.bind("<Right>", lambda e: self.next_paragraph())
        self.bind("<space>", lambda e: self.toggle_play())
        self.bind("<r>", lambda e: self.player.repeat_current()) # 'r' for repeat current if needed

        # Rótulo de Status
        self.status_label = ctk.CTkLabel(self, text="Pronto.", anchor="w")
        self.status_label.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        # Logic Components
        self.bot = None
        self.player = AudioPlayer()
        self.player.on_paragraph_change = self.on_paragraph_update
        self.player.on_finished = self.on_playback_finished
        
        # State
        self.is_playing = False
        self.current_pdf_text = ""
        self.current_filename = None
        
        threading.Thread(target=self.init_bot, daemon=True).start()

    def load_bookmarks(self):
        if os.path.exists(BOOKMARK_FILE):
            try:
                with open(BOOKMARK_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_bookmark(self, filename, index):
        if not filename: return
        self.bookmarks[filename] = index
        try:
            with open(BOOKMARK_FILE, 'w') as f:
                json.dump(self.bookmarks, f)
        except:
            pass
            
    def change_speed(self, choice):
        speed = float(choice.replace("x", ""))
        self.player.set_speed(speed)
        self.update_status(f"Velocidade: {speed}x")

    def start_export(self):
        if not self.player.queue:
            self.update_status("Nada para exportar.")
            return
            
        filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Audio", "*.mp3")])
        if filename:
            self.update_status("Exportando... (Isso pode demorar)")
            threading.Thread(target=self.run_export, args=(filename,), daemon=True).start()

    def run_export(self, filename):
        from export_utils import export_audiobook
        def progress(done, total):
            self.update_status(f"Exportando: {done}/{total} parágrafos...")
        
        success, msg = export_audiobook(self.player.queue, filename, progress)
        self.update_status(msg if success else f"Erro: {msg}")

    def increase_font(self):
        if self.font_size < 40:
            self.font_size += 2
            self.text_display.configure(font=("Arial", self.font_size))

    def decrease_font(self):
        if self.font_size > 10:
            self.font_size -= 2
            self.text_display.configure(font=("Arial", self.font_size))

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)
    
    def init_bot(self):
        self.update_status("Inicializando IA Local (Ollama)...")
        try:
            self.bot = ConversationBot(model_name=self.model_var.get())
            self.update_status("IA Pronta.")
        except Exception as e:
            self.update_status(f"Erro IA: {e}")

    def load_document(self):
        filename = filedialog.askopenfilename(filetypes=[("Documentos", "*.pdf *.txt")])
        if filename:
            threading.Thread(target=self.process_document, args=(filename,), daemon=True).start()

    def process_document(self, filename):
        self.update_status(f"Lendo {os.path.basename(filename)}...")
        text = extract_text_from_file(filename)
        if text:
            self.current_filename = filename
            self.current_pdf_text = text
            self.player.load_text(text)
            
            # Load full text into display and map indices
            self.map_paragraphs_to_display(self.player.queue)
            
            # Check Bookmark
            if filename in self.bookmarks:
                saved_idx = self.bookmarks[filename]
                self.player.current_index = saved_idx
                self.on_paragraph_update(saved_idx, self.player.queue[saved_idx]) # Manual update UI
                self.update_status(f"Retomado do parágrafo {saved_idx+1}.")
            else:
                self.update_status("Documento carregado. Pressione Ler.")
        else:
            self.update_status("Erro ao ler arquivo.")

    def toggle_play(self):
        if self.is_playing:
            self.player.pause()
            self.btn_play.configure(text="▶ Continuar", fg_color="green")
            self.is_playing = False
            self.update_status("Pausado.")
        else:
            if self.player.is_paused:
                self.player.resume()
            else:
                self.player.play()
            
            self.btn_play.configure(text="⏸ Pausar", fg_color="#F57C00")
            self.is_playing = True
            self.update_status("Lendo...")

    def next_paragraph(self):
        self.player.next_paragraph()
        self.update_status("Avançando parágrafo...")

    def prev_paragraph(self):
        self.player.prev_paragraph()
        self.update_status("Voltando parágrafo...")

    def map_paragraphs_to_display(self, paragraphs):
        """Inserts text and stores start/end indices for each paragraph."""
        self.text_display.configure(state="normal")
        self.text_display.delete("0.0", "end")
        
        self.paragraph_indices = []
        
        # Configure highlight tag
        # Note: CTkTextbox uses implicit tags sometimes, but we access the underlying tkinter widget for tags if needed.
        # CTkTextbox does expose 'tag_config' in newer versions. If not, we use self.text_display._textbox.
        
        # Using a bright color for the dark theme
        try:
            self.text_display.tag_config("highlight", background="#1B5E20", foreground="white")
        except:
            # Fallback if method missing, try direct access (usually strictly private but common workaround)
            pass

        current_line = 1
        
        for p in paragraphs:
            # We insert paragraph + double newline
            text_to_insert = p + "\n\n"
            
            # Calculate indices
            # Tkinter text indices are "line.char"
            start_idx = f"{current_line}.0"
            
            # Count lines in this paragraph
            # We can rely on 'insert' moving the cursor? No, we calculate.
            lines_in_p = text_to_insert.count('\n') 
            
            self.text_display.insert("end", text_to_insert)
            
            end_line = current_line + lines_in_p
            # The paragraph text ends before the last newlines potentially, but highlighting the block is fine.
            # Actually, let's be precise.
            end_idx = f"{end_line}.0" 
            
            self.paragraph_indices.append((start_idx, end_idx))
            current_line = end_line

        self.text_display.configure(state="disabled")

    def on_paragraph_update(self, index, text):
        # Save Bookmark
        if self.current_filename:
            self.save_bookmark(self.current_filename, index)

        if hasattr(self, 'paragraph_indices') and index < len(self.paragraph_indices):
            start, end = self.paragraph_indices[index]
            
            self.text_display.configure(state="normal")
            # Remove old highlights
            self.text_display.tag_remove("highlight", "0.0", "end")
            
            # Add new highlight
            self.text_display.tag_add("highlight", start, end)
            
            # Scroll to make it visible
            self.text_display.see(start)
            self.text_display.configure(state="disabled")
        else:
             # Fallback if no mapping (e.g. error)
             pass

    def on_playback_finished(self):
        self.is_playing = False
        self.btn_play.configure(text="▶ Ler", fg_color="green")
        self.update_status("Leitura concluída.")

    def start_voice_command(self):
        if self.is_playing:
            self.player.pause() # Pause to listen
        
        self.btn_voice.configure(state="disabled", text="Ouvindo...")
        threading.Thread(target=self.process_voice, daemon=True).start()

    def process_voice(self):
        audio_file = "cmd.wav"
        try:
            record_audio(audio_file, duration=4)
            self.update_status("Processando comando...")
            
            if self.bot:
                text = self.bot.transcribe_audio(audio_file)
                self.update_status(f"Comando ouvido: {text}")
                
                intent = self.bot.analyze_intent(text)
                self.execute_intent(intent)
            else:
                self.update_status("IA não disponível.")
                
        except Exception as e:
            self.update_status(f"Erro voz: {e}")
        
        self.btn_voice.configure(state="normal", text="🎤 Comando de Voz")
        # If we didn't resume in execute_intent, we might leave it paused?
        # User might have said "Pause", so we stay paused.
        # If he said "Next", we might want to auto-resume is play was active?
        # Let's handle in execute_intent.

    def execute_intent(self, intent):
        print(f"Executing Intent: {intent}")
        if intent == "PAUSE":
            self.player.pause()
            self.is_playing = False
            self.btn_play.configure(text="▶ Continuar", fg_color="green")
            self.update_status("Pausado por voz.")
            
        elif intent == "RESUME" or intent == "READ":
            self.player.resume()
            self.is_playing = True
            self.btn_play.configure(text="⏸ Pausar", fg_color="#F57C00")
            self.update_status("Resumindo...")
            
        elif intent == "NEXT":
            self.player.next_paragraph()
            self.player.resume() # Ensure we play
            self.is_playing = True
            self.btn_play.configure(text="⏸ Pausar")
            
        elif intent == "PREVIOUS":
            self.player.prev_paragraph()
            self.player.resume()
            self.is_playing = True
            self.btn_play.configure(text="⏸ Pausar")
            
        elif intent == "STOP":
            self.player.stop_playing()
            self.is_playing = False
            self.btn_play.configure(text="▶ Ler", fg_color="green")
            self.update_status("Parado.")
            
        else: # CHAT or Unknown
            self.update_status("Comando não reconhecido.")

    def update_status(self, text):
        self.status_label.configure(text=text)

if __name__ == "__main__":
    app = AudioDescApp()
    app.mainloop()
