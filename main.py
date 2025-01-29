import requests
import json
import warnings
import re

from pyfiglet import Figlet

f = Figlet(font="drpepper")
print(f.renderText("Welcome To LinguaForge"))



def make_translation_request(to_translate : dict):
    # Define the URL of the FastAPI endpoint
    url = "http://127.0.0.1:8000/translate/"

    # Send the POST request and parse the JSON response
    response = requests.post(url, json=to_translate)

    return response



def handle_translations():
    to_continue = True
    while to_continue:

        src_input = input("What do you wish to translate: \n----> ")
        if src_input == "/bye":
            to_continue = False
            return

        # Define the dictionary
        data = {
            "source_lang": "en",
            "target_lang": "de",
            "src_text": [src_input]
        }

        translated_response = make_translation_request(to_translate=data)

        translated_text = json.loads(translated_response.text)
        print(translated_text[0])
        print()



handle_translations()
