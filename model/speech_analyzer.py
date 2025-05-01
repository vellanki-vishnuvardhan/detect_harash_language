import speech_recognition as sr
from textblob import TextBlob
from pydub import AudioSegment
import io
import mimetypes

# List of offensive words to detect
offensive_words = [
    'stupid', 'idiot', 'moron', 'dumb', 'loser', 'dork', 'geek', 'nerd',
    'lame', 'fool', 'useless', 'weak', 'worthless', 'crappy', 'ugly', 
    'fat', 'skinny', 'lazy', 'pathetic', 'annoying', 'bitchy', 'crybaby',
    'whiny', 'coward', 'wimp', 'boring', 'gross', 'disgusting', 'jerk',
    'selfish', 'spoiled', 'snob', 'arrogant', 'cheater', 'liar', 'backstabber',
    'traitor', 'two-faced', 'manipulator', 'egotistical', 'shallow', 'clueless',
    'douchebag', 'brat', 'baby', 'dumbass', 'messed up', 'nasty', 'stubborn',
    'bossy', 'rude', 'impolite', 'cruel', 'mean', 'unfriendly', 'unhelpful', 'silly',
    'immature', 'vulgar', 'offensive', 'irritating', 'petty', 'annoying', 'disrespectful',
    'clumsy', 'awkward', 'weird', 'picky', 'high-maintenance', 'demanding', 'complicated',
    'moody', 'whiny', 'shy', 'needy', 'overdramatic', 'overbearing', 'difficult', 'snobby',
    'pushy', 'inconsiderate', 'impulsive', 'loud', 'too sensitive', 'judgmental', 'sassy',
    'nagging', 'gossiper', 'gullible', 'shameful', 'untrustworthy', 'unreliable', 'greedy',
    'ungrateful', 'unworthy', 'insecure', 'naive', 'lazy', 'defensive', 'pessimistic'
]


def detect_violence_or_harsh_language(text):
    """Detects violent or harsh language in the transcribed text."""
    if not text:
        return "No text found"

    text_lower = text.lower()

    # Check if any offensive words are in the text
    for word in offensive_words:
        if word in text_lower:
            return "⚠️ Warning: Detected violent or harsh conversation (Offensive language)"

    # Sentiment analysis with TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    # Adjust threshold for stronger negative sentiment detection
    if sentiment < -0.5:
        return "⚠️ Warning: Detected violent or harsh conversation (Negative sentiment)"
    
    return "✅ No violent or harsh language detected."

def transcribe_speech_from_mic():
    """Transcribes speech from the microphone using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Speech Recognition request failed; {e}"

def transcribe_audio_file(uploaded_file):
    """Transcribes an uploaded audio file (convert MP3 to WAV if needed)."""
    recognizer = sr.Recognizer()

    # Determine file type from MIME type directly
    try:
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)  # This line assumes uploaded_file has a 'name' attribute
    except AttributeError:
        # Handle case when 'name' attribute is missing (e.g., when working with BytesIO)
        mime_type = None

    try:
        # If uploaded_file is a BytesIO object, we need to handle it accordingly
        if isinstance(uploaded_file, io.BytesIO):
            audio_bytes = uploaded_file.read()

            # If the MIME type is 'audio/mpeg' (MP3), convert to WAV format
            if mime_type == "audio/mpeg":  # MP3 files have MIME type 'audio/mpeg'
                audio = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
                with io.BytesIO() as wav_io:
                    audio.export(wav_io, format="wav")
                    wav_io.seek(0)  # Rewind the file to the beginning
                    audio_bytes = wav_io.read()  # Update the audio bytes with WAV format
                    audio_io = io.BytesIO(audio_bytes)
            else:
                audio_io = io.BytesIO(audio_bytes)  # Process as is (WAV, FLAC, etc.)

            # Use the audio file from memory (WAV format) for transcription
            with sr.AudioFile(audio_io) as source:
                audio = recognizer.record(source)

            # Return the transcribed text
            return recognizer.recognize_google(audio)

    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Speech Recognition request failed; {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
