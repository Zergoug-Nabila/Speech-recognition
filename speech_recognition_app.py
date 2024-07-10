import streamlit as st
import speech_recognition as sr

def transcribe_speech(api, language):
    # Initialize recognizer class
    r = sr.Recognizer()
    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("Speak now...")
        # listen for speech and store in audio_text variable
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            # Using selected Speech Recognition API
            if api == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                text = "Unsupported API"
            return text
        except sr.RequestError:
            return "API unavailable or unresponsive"
        except sr.UnknownValueError:
            return "Sorry, I did not get that. Please try again."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

def main():
    st.title("Enhanced Speech Recognition App")
    
    st.write("Choose the Speech Recognition API:")
    api = st.selectbox("API", ["Google", "Sphinx"])

    st.write("Choose the language:")
    language = st.selectbox("Language", ["en-US", "es-ES", "fr-FR", "de-DE", "zh-CN"])

    st.write("Click on the microphone to start speaking:")

    # Initialize session state to hold the transcription text
    if 'text' not in st.session_state:
        st.session_state.text = ""

    # Add a button to trigger speech recognition
    if st.button("Start Recording"):
        st.session_state.text = transcribe_speech(api, language)
        st.write("Transcription: ", st.session_state.text)

    # Display transcription and save button only if there's text
    if st.session_state.text:
        if st.button("Save Transcription"):
            with open("transcription.txt", "w") as f:
                f.write(st.session_state.text)
            st.success("Transcription saved to transcription.txt")

if __name__ == "__main__":
    main()
