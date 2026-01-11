import os
import ollama
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConversationBot:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.conversation_history = []
        # Check if ollama is reachable? We'll assume yes or handle error in calls.
        print(f"Bot initialized with model: {self.model_name}")

    def transcribe_audio(self, audio_path):
        """
        Transcribes audio using a local STT tool. 
        Since we removed openai-whisper in favor of local options if possible,
        we can still use 'whisper' library if installed, or 'speech_recognition'.
        Re-using the previous logic if whisper is still desired, 
        or switching to a ligher weight one if preferred.
        For now, let's keep using 'whisper' as it was in requirements.
        """
        try:
            import whisper
            # Load model only when needed to save RAM or keep it loaded if frequent?
            # Better to load once.
            if not hasattr(self, 'whisper_model'):
                print("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
            
            print("Transcribing audio...")
            result = self.whisper_model.transcribe(audio_path)
            text = result["text"]
            print(f"Transcription: {text}")
            return text
        except Exception as e:
            print(f"Transcription Error: {e}")
            return ""

    def analyze_intent(self, text):
        """
        Determines if the text is a command for the audio player.
        Returns: 'PAUSE', 'RESUME', 'NEXT', 'PREVIOUS', 'STOP', 'READ', or 'CHAT'
        """
        prompt = f"""
        Classify the following text into one of these commands: 
        PAUSE, RESUME, NEXT, PREVIOUS, STOP, READ.
        If it's not a command, return CHAT.
        
        Text: "{text}"
        
        Answer only with the category name.
        """
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': prompt},
            ])
            intent = response['message']['content'].strip().upper()
            # Cleanup in case of verbose model
            for cmd in ['PAUSE', 'RESUME', 'NEXT', 'PREVIOUS', 'STOP', 'READ', 'CHAT']:
                if cmd in intent:
                    return cmd
            return 'CHAT'
        except Exception as e:
            print(f"Ollama Intent Error: {e}")
            return 'CHAT'

    def get_response(self, text, context=""):
        """Sends text to Ollama and gets response."""
        messages = []
        if context:
             messages.append({"role": "system", "content": context})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": text})
        
        try:
            response = ollama.chat(model=self.model_name, messages=messages)
            reply = response['message']['content']
            
            self.conversation_history.append({"role": "user", "content": text})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            return reply
        except Exception as e:
            return f"Error contacting Ollama: {e}"

    def text_to_speech(self, text, output_file="response.mp3"):
        """Converts text to speech using gTTS."""
        try:
            print(f"Generating audio for: {text[:50]}...")
            tts = gTTS(text=text, lang='pt') 
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"TTS Error: {e}")
            return None

