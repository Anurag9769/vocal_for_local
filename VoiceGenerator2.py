from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import time

# Define the dialogues with timestamps and sentiments
dialogues = [
    {"timestamp": "10:42:01", "speaker": "Manoj", "text": "What a sad story!", "sentiment": "neutral"},
    {"timestamp": "10:42:30", "speaker": "Manisha", "text": "Indeed! tell me something nice", "sentiment": "neutral"},
    {"timestamp": "10:43:00", "speaker": "Manoj", "text": "Wow that's great news!", "sentiment": "sad"},
]


# Function to convert text to speech and play it
def speak_text(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("temp.mp3")
    audio = AudioSegment.from_mp3("temp.mp3")
    play(audio)


# Main loop to process dialogues based on timestamps
def speak_dialogue_on_time():
    for dialogue in dialogues:
        # Wait until the timestamp
        current_time = time.strftime("%H:%M:%S", time.localtime())
        while current_time < dialogue["timestamp"]:
            time.sleep(1)
            current_time = time.strftime("%H:%M:%S", time.localtime())

        # Speak the text
        print(f"{dialogue['timestamp']} - {dialogue['speaker']}: {dialogue['text']}")
        speak_text(dialogue["text"])

if __name__ == "__main__":
    speak_dialogue_on_time()
