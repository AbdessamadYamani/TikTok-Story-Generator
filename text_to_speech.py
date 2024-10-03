import requests
import base64
from typing import List, Optional
from LLM import StoryProcessor

class TextToSpeech:
    def __init__(self, voice: str = "en_us_002", max_chunk_size: int = 300):
        self.voice = voice
        self.max_chunk_size = max_chunk_size
        self.url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
        self.story_processor = StoryProcessor()

    def _process_chunk(self, chunk: str) -> Optional[bytes]:
        try:
            response = requests.post(
                self.url,
                json={"text": chunk, "voice": self.voice},
                timeout=10
            )
            response.raise_for_status()
            audio_base64 = response.json()['data']
            return base64.b64decode(audio_base64)
        except requests.RequestException as e:
            print(f"Error processing chunk: {str(e)}")
            return None

    def _split_into_chunks(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(" ".join(current_chunk + [word])) <= self.max_chunk_size:
                current_chunk.append(word)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

    def generate_audio(self, input_text: str, output_path: str = "output.mp3") -> bool:
        try:
            text = self.story_processor.get_llm_response(input_text)
            chunks = self._split_into_chunks(text)
            
            audio_parts = []
            for i, chunk in enumerate(chunks, 1):
                print(f"Processing chunk {i}/{len(chunks)}")
                if audio_part := self._process_chunk(chunk):
                    audio_parts.append(audio_part)

            if not audio_parts:
                raise ValueError("Failed to generate any audio chunks")

            combined_audio = b"".join(audio_parts)
            with open(output_path, "wb") as f:
                f.write(combined_audio)
            
            return True

        except Exception as e:
            print(f"Failed to generate audio: {str(e)}")
            return False
        

        ########