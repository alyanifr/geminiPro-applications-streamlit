import os
import tempfile

from gtts import gTTS
from playsound import playsound
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from deep_translator import GoogleTranslator


from gemini_utils import (load_gemini_pro_chatbot, gemini_pro_vision_response)

# Setting up the streamlit page configuration
st.set_page_config(
    page_title="Assistant.ai",
    page_icon="🧠",
    layout="wide"
)

# Creating sidebar menu
with st.sidebar:
    selected = option_menu(menu_title="Get Assistant",
                           options=["Chatbot",
                                    "Caption Generator",
                                    "Translator"],
                           menu_icon="robot",
                           icons=["chat-dots-fill",
                                  "camera-fill",
                                  "translate"],
                           default_index=0)


# Translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Building streamlit page for chatbot
if selected == "Chatbot":
    model = load_gemini_pro_chatbot()

    # Initialize chat session in streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit page title
    st.title("Chatbot")

    # Displaying chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Talk with GenPro")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Displaying gemini-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Building streamlit page for caption generator
if selected == "Caption Generator":

    # Streamlit page title
    st.title("Caption Generator")

    # Image uploader
    upload_image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if st.button("Generate"):
        image = Image.open(upload_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)
            default_prompt = "Write a brief caption for this image."

            # Getting the response from gemini-pro
            caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)


# Building streamlit page for text translation
if selected == "Translator":

    # Streamlit page title
    st.title("Translator")

    # Streamlit page layout
    col1, col2 = st.columns(2)

    with col1:
        # input_language_list = ["English", "French", "Japanese", "Korean", "Latin", "Malay", "Spanish", "Thai"]
        input_language_list = GoogleTranslator().get_supported_languages()
        input_language = st.selectbox(label="Input Language", options=input_language_list, index=27)

    with col2:
        output_language_list = [x for x in input_language_list if x != input_language]
        output_language = st.selectbox(label="Output Language", options=output_language_list)

    input_text = st.text_area("Type the text to be translated.")

    # Generating translate button and display the response
    if st.button("Translate"):
        # translated = change_language(output_language)
        translated = GoogleTranslator(source=input_language, target=output_language).translate(input_text)
        st.success(translated)

        # Generating text to speech button (need some work)
        def text_to_speech(text):
            tts = gTTS(text)
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tts.save(temp_file.name)
            file_url = "file://" + os.path.abspath(temp_file.name)
            return file_url

        file_path = text_to_speech(translated)
        playsound(file_path)
        #os.remove(file_path)
