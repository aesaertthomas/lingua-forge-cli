import requests
import json
from pyfiglet import Figlet

class LinguaForge:
    def __init__(self):
        self.source_lang = None
        self.target_lang = None
        self.base_url = "http://127.0.0.1:8000/translate/"

        self.command_handlers = {
            "/bye": self._handle_exit,
            "/change-lang": self._handle_change_lang,
            "/help": self._handle_help
        }

    def _print_banner(self):
        f = Figlet(font="drpepper")
        print(f.renderText("Welcome To LinguaForge"))

    def _get_user_input(self, prompt):
        return input(f"\n{prompt}\n----> ").strip()

    def _handle_help(self):
        self._show_command_guide()
        return True

    def _handle_exit(self):
        print("Goodbye!")
        return False  # Break loop

    def _handle_change_lang(self):
        self.source_lang = self._get_user_input("Enter source language")
        self.target_lang = self._get_user_input("Enter target language")
        print(f"\nLanguage pair updated: {self.source_lang} -> {self.target_lang}")
        return True

    def _show_command_guide(self):
        print("\nAvailable commands:")
        print("/bye          - Exit the program")
        print("/change-lang  - Change language pair")
        print("/help         - Show this help message")
        print("\nEnter text directly to translate")

    def _validate_languages(self):
        if not self.source_lang or not self.target_lang:
            print("Language pair not set! Using defaults (en -> es)")
            self.source_lang = "en"
            self.target_lang = "es"

    def _make_translation_request(self, text):
        """Handle translation with error checking and retries"""
        data = {
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "src_text": [text]
        }

        try:
            response = requests.post(self.base_url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()[0]
        except requests.exceptions.RequestException as e:
            print(f"\nTranslation error: {str(e)}")
            return None

    def _process_input(self, user_input):
        """Handle commands or dispatch for translation"""
        if user_input in self.command_handlers:
            return self.command_handlers[user_input]()

        # Handle translation
        translated = self._make_translation_request(user_input)
        if translated:
            print(f"\nTranslation: {translated}")
        return True

    def run(self):
        """Main application loop"""
        self._print_banner()
        self._validate_languages()
        self._show_command_guide()

        while True:
            user_input = self._get_user_input("Enter text or command")
            if not user_input:
                continue

            should_continue = self._process_input(user_input)
            if not should_continue:
                break





if __name__ == "__main__":
    try:
        app = LinguaForge()
        app.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nCritical error: {str(e)}")
