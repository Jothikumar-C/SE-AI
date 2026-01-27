import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import logging
import os

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Audio to Text Converter",
    layout="centered"
)

st.title("🎙️ Audio to Text Converter")
st.write("Upload an audio file and convert speech into text.")

# --------------------------------------------------
# Helper Function: Convert Audio to WAV
# --------------------------------------------------
def convert_to_wav(uploaded_file):
    """
    Converts uploaded audio file (mp3/m4a/wav) to WAV format.
    Returns the path to the WAV file.
    """
    try:
        logging.info("Converting audio file to WAV format")

        audio = AudioSegment.from_file(uploaded_file)

        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(temp_wav.name, format="wav")

        logging.info("Audio conversion successful")
        return temp_wav.name

    except Exception as e:
        logging.error(f"Audio conversion failed: {e}")
        raise


# --------------------------------------------------
# Helper Function: Speech to Text
# --------------------------------------------------
def speech_to_text(wav_path):
    """
    Converts WAV audio file to text using SpeechRecognition.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_path) as source:
            logging.info("Reading audio file")
            audio_data = recognizer.record(source)

        logging.info("Converting speech to text")
        text = recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        logging.warning("Speech was unintelligible")
        return "Could not understand the audio."

    except sr.RequestError as e:
        logging.error(f"Speech recognition service error: {e}")
        return "Speech recognition service error."

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "An unexpected error occurred."


# --------------------------------------------------
# Streamlit UI: File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "m4a"]
)

# --------------------------------------------------
# Process Uploaded File
# --------------------------------------------------
if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Convert to Text"):
        with st.spinner("Processing audio..."):
            try:
                wav_path = convert_to_wav(uploaded_file)
                text_output = speech_to_text(wav_path)

                st.subheader("📝 Converted Text")
                st.text_area(
                    label="Speech to Text Output",
                    value=text_output,
                    height=200
                )

                os.remove(wav_path)
                logging.info("Temporary WAV file deleted")

            except Exception as e:
                st.error("Failed to process audio file.")
                logging.error(f"Processing failed: {e}")