import streamlit as st
import librosa
import numpy as np
import tensorflow as tf
import time
import os
from pydub import AudioSegment
import io

def load_model():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_directory, "../Models/2d_model_48_nor_nadam.h5")
    return tf.keras.models.load_model(model_path)

classes = ['Fake', 'Real']

def mel_spectrogram(audio):
    audio, sample_rate = librosa.load(audio)
    mel_audio = librosa.feature.melspectrogram(y=audio, sr=sample_rate)
    num_segments = mel_audio.shape[1] // 128
    mel_spectrogram = librosa.power_to_db(np.abs(mel_audio)**2, ref=np.max)
    segments = []
    for i in range(num_segments):
        segment = mel_spectrogram[:, i * 128 : (i + 1) * 128]
        segments.append(segment)
    if mel_spectrogram.shape[1] % 128 != 0:
        last_segment = mel_spectrogram[:, -(mel_spectrogram.shape[1] % 128):]
        padded_segment = np.pad(last_segment, ((0, 0), (0, 128 - last_segment.shape[1])), mode='constant')
        segments.append(padded_segment)
    return segments

def predict(audio, model):
    segments = mel_spectrogram(audio)
    total_confidence = 0
    for segment in segments:
        prediction = model.predict(tf.expand_dims(segment, 0))
        predicted_class = classes[np.argmax(prediction)]
        confidence = np.max(prediction)
        if predicted_class == "fake":
            return predicted_class, confidence
        else:
            total_confidence += confidence
    return predicted_class, round(total_confidence / len(segments), 2)

def convertToWav(uploaded_audio):
    try:
        audio_data = uploaded_audio.read()
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
        wav_data = io.BytesIO()
        audio_segment.export(wav_data, format="wav")
        return wav_data
    except Exception as e:
        st.error("Uploaded file may be corrupted"+str(e))
        return None

def show():
    container = st.container(border=True)
    with container:
        st.title("Audio Classification")
        st.divider()
        cont1, cont2, cont3 = st.container(border=True), st.container(border=True), st.container(border=True)
        with cont1:
            uploaded_audio = st.file_uploader("**Upload an audio file...**", type=["aac", "aiff", "au", "flac", "m4a",  "mp3", "ogg", "wav", "wma"])
        if uploaded_audio is not None and uploaded_audio.type!="audio/wav":
            uploaded_audio = convertToWav(uploaded_audio)
        model = load_model()
        with cont2:
            st.write("**Audio player:**")
            st.audio(uploaded_audio, format='audio/wav', start_time=0)
        with cont3:
            _, col, _ = st.columns([2, 1, 2])
            with col:
                st.subheader("Prediction")
        _, col, _ = st.columns([3, 1, 3])
        predicted_class, confidence = '', ''
        with col:
            if st.button("Predict"):
                if uploaded_audio is None:
                    cont1.markdown("<p style='color:red'>**Please upload an audio file</p>", unsafe_allow_html=True)
                else:
                    with cont3:
                        _, col, _ = st.columns([2, 1, 2])
                        with col:
                            with st.spinner("Classifying.."):
                                predicted_class, confidence = predict(uploaded_audio, model)

        classification_color = "green" if predicted_class == "Real" else "red"
        confidence_color = "green" if confidence == '' or confidence > 0.7 else "orange" if float(confidence) < 0.7 and confidence > 0.5 else "red"
        if(confidence):
            confidence=str(confidence*100)+"%"
        st.markdown(f"<style>.classification {{color:{classification_color}}} .confidence{{color:{confidence_color}}}</style>",unsafe_allow_html=True)
        with cont3:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"<p style='text-align:center'><strong>Classification:</strong> <span class='classification'>{predicted_class}</span></p>",unsafe_allow_html=True)
            with col2:
                st.write(f"<p style='text-align:center'><strong>Confidence:</strong> <span class='confidence'>{confidence}</span></p>",unsafe_allow_html=True)
