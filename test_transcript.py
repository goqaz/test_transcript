import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
import re
import logging

# Configuration du logging
logging.basicConfig(level=logging.ERROR)

# Fonction pour extraire l'ID de la vidéo
def get_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None

st.title("Test Minimal de YouTubeTranscriptApi")
st.write("Bienvenue dans l'application de test de récupération de transcriptions.")

video_url = st.text_input("Entrez l'URL de la vidéo YouTube :", "https://www.youtube.com/watch?v=iCvmsMzlF7o")
st.write(f"URL saisie : {video_url}")

if st.button("Tester Transcription"):
    st.write("Bouton 'Tester Transcription' cliqué.")
    if not video_url:
        st.warning("Veuillez entrer une URL.")
    else:
        video_id = get_video_id(video_url)
        if not video_id:
            st.error("L'URL fournie n'est pas valide.")
        else:
            st.write(f"Vidéo ID extraite : {video_id}")
            try:
                st.write("Tentative de récupération de la transcription en français.")
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])
                transcript = " ".join([t['text'] for t in transcript_list])
                st.success("Transcription récupérée avec succès.")
                st.text_area("Transcription :", transcript, height=300)
            except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript) as e:
                st.warning(f"Transcription en français non disponible : {e}. Tentative en anglais.")
                try:
                    st.write("Tentative de récupération de la transcription en anglais.")
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    transcript = " ".join([t['text'] for t in transcript_list])
                    st.success("Transcription en anglais récupérée avec succès.")
                    st.text_area("Transcription :", transcript, height=300)
                except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript) as e:
                    st.error("Aucune transcription disponible pour cette vidéo.")
                    logging.error(f"Erreur lors de la récupération des transcriptions: {e}")
            except Exception as e:
                st.error(f"Erreur inattendue lors de la récupération de la transcription: {e}")
                logging.error(f"Erreur inattendue: {e}")
