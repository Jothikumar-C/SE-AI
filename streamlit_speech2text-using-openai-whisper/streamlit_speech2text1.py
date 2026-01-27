
import streamlit as st
import whisper
import os
import logging
from datetime import datetime

# --- 1. LOGGING CONFIGURATION ---
# This helps us track errors in the terminal while the app runs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Audio Transcriber", page_icon="🎙️")

# --- 3. MODEL LOADING (CACHED) ---
# We use @st.cache_resource so the model stays in memory and doesn't reload every time you click a button
@st.cache_resource
def load_whisper_model():
    logging.info("Loading Whisper model... this may take a moment.")
    return whisper.load_model("base")  # 'base' is fast and accurate for local laptops

model = load_whisper_model()

# --- 4. APP UI ---
st.title("🎙️ AI Speech-to-Text Transcriber")
st.markdown("Upload an audio file and let the AI extract the text for you.")

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose an audio file", 
    type=["wav", "mp3", "m4a", "ogg", "flac"]
)

if uploaded_file is not None:
    # Display audio player so user can hear what they uploaded
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Transcribe Audio"):
        try:
            with st.spinner("🤖 AI is listening and processing..."):
                logging.info(f"Started processing file: {uploaded_file.name}")
                
                # Save uploaded file temporarily to disk (Whisper needs a file path)
                temp_filename = f"temp_{uploaded_file.name}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Perform transcription
                result = model.transcribe(temp_filename)
                transcription_text = result["text"]

                # --- 5. DISPLAY RESULTS ---
                st.success("Transcription Complete!")
                st.subheader("Extracted Text:")
                st.text_area(
                    label="Resulting Text",
                    value=transcription_text,
                    height=300
                )

                # Clean up: Delete the temporary file
                os.remove(temp_filename)
                logging.info(f"Successfully transcribed {uploaded_file.name}")

        except Exception as e:
            st.error(f"An error occurred during processing.")
            logging.error(f"Error processing audio: {str(e)}")

# --- 6. FOOTER ---
st.divider()
st.caption("Running locally on Streamlit with OpenAI Whisper (Base Model)")