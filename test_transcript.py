import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript, CouldNotDecodeTranscript
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
                st.write("Liste des transcriptions disponibles :")
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcripts_info = []
                for transcript in transcript_list:
                    transcript_type = "Manuel" if not transcript.is_generated else "Généré automatiquement"
                    transcripts_info.append(f"Langue : {transcript.language} ({transcript.language_code}), Type : {transcript_type}")
                st.write("\n".join(transcripts_info))

                # Tenter de récupérer la transcription en français
                st.write("Tentative de récupération de la transcription en français.")
                transcript = transcript_list.find_transcript(['fr'])
                transcript_text = " ".join([t['text'] for t in transcript.fetch()])
                st.success("Transcription en français récupérée avec succès.")
                st.text_area("Transcription :", transcript_text, height=300)

            except NoTranscriptFound:
                st.warning("Aucune transcription trouvée pour cette vidéo.")
            except TranscriptsDisabled:
                st.warning("Les sous-titres sont désactivés pour cette vidéo.")
            except CouldNotRetrieveTranscript as e:
                st.warning(f"Erreur lors de la récupération de la transcription : {e}")
            except Exception as e:
                st.error(f"Erreur inattendue : {e}")
                logging.error(f"Erreur inattendue : {e}")

