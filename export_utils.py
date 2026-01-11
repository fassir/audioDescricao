import os
from gtts import gTTS
import tempfile
# Note: pydub requires ffmpeg/avlib. If not present, simple concatenation might work for some mp3s but is risky.
# We will try simple file concatenation first for standard gTTS mp3s which are usually robust for this.
# Or just ensure pydub is used if available.

def export_audiobook(paragraphs, output_file, progress_callback=None):
    """
    Export paragraphs to a single MP3 file.
    Uses simple concatenation of MP3 bytes which usually works for gTTS output.
    """
    total = len(paragraphs)
    
    try:
        with open(output_file, 'wb') as outfile:
            for i, p in enumerate(paragraphs):
                if not p.strip():
                    continue
                    
                if progress_callback:
                    progress_callback(i, total)
                
                # Generate chunk
                tts = gTTS(text=p, lang='pt')
                
                # Save to temp
                fd, path = tempfile.mkstemp(suffix='.mp3')
                os.close(fd)
                tts.save(path)
                
                # Append bytes
                with open(path, 'rb') as infile:
                    outfile.write(infile.read())
                
                os.remove(path)
                
        if progress_callback:
            progress_callback(total, total)
            
        return True, "Exportado com sucesso!"
        
    except Exception as e:
        return False, str(e)
