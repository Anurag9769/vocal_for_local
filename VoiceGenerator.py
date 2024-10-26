import pyttsx3
from gtts import gTTS
from textblob import TextBlob
import os

# Function to analyze sentiment
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Range from -1 to 1
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'

# Function to convert text to speech
def text_to_speech(text, sentiment):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice: {voice.name} | ID: {voice.id}")
    if sentiment == 'positive':
        engine.setProperty('rate', 150)  # Slower speed for positive tone
        engine.setProperty('volume', 1.0)  # Higher volume
        engine.setProperty('voice', 'english+f1')  # Feminine voice
    elif sentiment == 'negative':
        engine.setProperty('rate', 90)  # Slower and deeper tone
        engine.setProperty('volume', 0.8)
        engine.setProperty('voice', 'english+m3')  # Masculine voice
    else:
        engine.setProperty('rate', 120)  # Neutral voice
        engine.setProperty('volume', 0.9)

    engine.say(text)
    engine.runAndWait()

# Main function to process text and convert to speech
def process_text_to_speech(text):
    sentiment = get_sentiment(text)
    print(f"Sentiment: {sentiment}")
    text_to_speech(text, sentiment)

# Example usage
if __name__ == "__main__":
    text = input("Enter text to analyze and convert to speech: ")
    process_text_to_speech(text)
