import os

import json
import google.generativeai as genai
#from googletrans import Translator

# Configuring gemini-pro api key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

# Invoke the api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)


# Load gemini-pro model for chatbot
def load_gemini_pro_chatbot():
    gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro")
    return gemini_pro_model


# Load gemini-pro model for image captioning
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-pro")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result


# Function for calling the googletrans - translator library

'''def change_language(language):
    translator = Translator()
    translated_text = translator._translate(input_text, dest=language)
    return translated_text.text'''





