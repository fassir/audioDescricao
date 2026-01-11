import base64
import os

def audio_to_base64(file_path):
    """
    Reads an audio file and converts it to a base64 encoded string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
        
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
    return encoded_string

def base64_to_audio(base64_string, output_path):
    """
    Decodes a base64 string and saves it as an audio file.
    """
    decoded_data = base64.b64decode(base64_string)
    with open(output_path, "wb") as audio_file:
        audio_file.write(decoded_data)
    return output_path
