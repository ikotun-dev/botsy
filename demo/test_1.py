import re
import random
from possible_greetings import greetings


class ChatBot:
    def __init__(self):
        self.greetings = [greeting.lower() for greeting in greetings]
        self.responses = {
            "microservices_advantages": [
                "Microservice architecture offers scalability, allowing independent scaling of services.",
                "Maintainability is improved as services can be updated independently without affecting the entire application.",
                "Flexibility is achieved by allowing different technologies for each service based on its requirements.",
                "Fault isolation ensures high availability by preventing the failure of one service from affecting the entire system.",
                "Faster development is possible with smaller, focused teams working independently on specific services.",
                "Continuous deployment is supported, allowing services to be deployed individually without impacting other components.",
            ],
            "fallback": [
                "I'm sorry, I don't understand that. Can you ask something else?",
                "I'm still learning. Could you please ask another question?",
                "I didn't catch that. Feel free to rephrase your question.",
            ],
        }

    def greet(self):
        print("Hello! I'm your ChatBot. Ask me anything.")
        user_input = input("You : ")
        if user_input in self.greetings:
            print(f"{random.choice(self.greetings)}")
        print("What do you wanna ask me : ")

    def chat(self):
        user_input = input("You: ")
        while user_input.lower() not in ["exit", "quit", "goodbye"]:
            response = self.get_response(user_input)
            print(f"Chatbot: {response}")
            user_input = input("You: ")

    def get_response(self, user_input):
        for intent, patterns in self.responses.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return random.choice(self.responses[intent])
        return random.choice(self.responses["fallback"])


# Example Usage
chatbot = ChatBot()
print(chatbot.greetings)
chatbot.greet()
chatbot.chat()
