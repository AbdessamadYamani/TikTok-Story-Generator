import requests
import base64
import json

def get_available_voices():
    url = "https://tiktok-tts.weilnet.workers.dev/api/voices"
    response = requests.get(url)
    if response.status_code == 200:
        voices = response.json()
        return voices
    else:
        print(f"Error fetching voices: {response.status_code}")
        return None

def print_voices():
    voices = get_available_voices()
    if voices:
        print("Available voices:")
        for category, voice_list in voices.items():
            print(f"\n{category}:")
            for voice in voice_list:
                print(f"  - {voice}")
    else:
        print("Failed to fetch voices")

print_voices()