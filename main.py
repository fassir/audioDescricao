import os
import time
from bot import ConversationBot
from audio_utils import record_audio, play_audio, record_audio_interactive
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    print(Fore.CYAN + "=== Voice Conversation Bot with OpenAI & Whisper ===")
    
    # Check for API Key
    if not os.getenv("OPENAI_API_KEY"):
        print(Fore.RED + "Error: OPENAI_API_KEY not found. Please set it in a .env file.")
        return

    bot = ConversationBot()
    
    while True:
        print(Fore.YELLOW + "\nOptions: [R]ecord Audio | [T]ype Text | [Q]uit")
        choice = input("Select an option: ").strip().lower()
        
        user_input_text = ""
        
        if choice == 'q':
            print("Exiting...")
            break
            
        elif choice == 'r':
            # Audio workflow
            audio_file = "user_input.wav"
            # We use a fixed duration for simplicity in this basic version, 
            # or the interactive one if soundfile/block logic works well on user's machine.
            # Let's use the interactive one with Ctrl+C for better UX if possible, 
            # but safe fallback is fixed duration.
            print("Press Ctrl+C in terminal to stop recording (or wait if fixed duration).")
            try:
                # record_audio is fixed duration, record_audio_interactive is indefinite
                record_audio_interactive(audio_file)
            except Exception as e:
                print(Fore.RED + f"Recording error: {e}")
                continue

            print(Fore.GREEN + "Processing audio...")
            try:
                user_input_text = bot.transcribe_audio(audio_file)
            except Exception as e:
                print(Fore.RED + f"Transcription error: {e}")
                continue
                
        elif choice == 't':
            # Text workflow
            user_input_text = input("You: ")
            
        else:
            print("Invalid option.")
            continue
            
        if not user_input_text.strip():
            print("Empty input.")
            continue
            
        print(Fore.BLUE + f"User: {user_input_text}")
        
        # Get AI Response
        print("Waiting for ChatGPT...")
        try:
            response_text = bot.get_gpt_response(user_input_text)
            print(Fore.MAGENTA + f"Bot: {response_text}")
            
            # Text to Speech
            output_audio = "bot_response.mp3"
            bot.text_to_speech(response_text, output_audio)
            
            # Play Audio
            print("Playing response...")
            play_audio(output_audio)
            
        except Exception as e:
            print(Fore.RED + f"Error during processing: {e}")

if __name__ == "__main__":
    main()
