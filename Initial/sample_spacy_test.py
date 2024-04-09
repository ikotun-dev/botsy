import spacy
import random


class ChatBot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.greetings = [
            "hello",
            "hi",
            "hey",
            "greetings",
            "morning",
            "afternoon",
            "evening",
        ]

    def is_greeting(self, user_input):
        doc = self.nlp(user_input)
        # Check if any token in the user's input is a greeting
        return any(token.text.lower() in self.greetings for token in doc)

    def get_response(self, user_input):
        if self.is_greeting(user_input):
            return "Hello! How can I assist you today?"
        else:
            return "I'm still learning. Could you please ask another question?"

    def chat(self):
        print("Hello! I'm your ChatBot. Ask me anything.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "goodbye"]:
                print("ChatBot: Goodbye!")
                break
            response = self.get_response(user_input)
            print(f"ChatBot: {response}")


# Example Usage
chatbot = ChatBot()
chatbot.chat()
