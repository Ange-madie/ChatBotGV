from tkinter import *

class ChatbotView(Tk):

    def __init__(self):
        super().__init__()
        # Fenetre
        self.title("Nora GV 2")
        self.geometry("648x410")

        # Widget
        self.show_message = Text(self, bg="black", fg="green")
        self.enter_message = Entry(self, width=107)

    def show_widget(self):
        self.show_message.grid(row=0, column=0, columnspan=2)
        self.enter_message.grid(row=1, column=0, columnspan=2)
        self.show_message.insert(END, "Nora: Je suis un Chatbot IA de test, suite de Nora GV 1, utilisant une architecture MVC. Si tu veut quitter tape 'Aurevoir'.")

    def get_input(self):
        r = self.enter_message.get()
        return r

    def display_message(self, message):
        self.show_message.insert(END, "\n"+message)
