from ChatbotView import ChatbotView
from ChatbotModel import ChatbotModel
from pickle import dump, load
from tkinter import END


class ChatbotCrontroller:
    def __init__(self):
        self.vue = ChatbotView()
        try:
            file = open("model.ngv2", "rb")
            self.model = load(file)
            file.close()
        except FileNotFoundError:
            self.model = ChatbotModel()
            self.model.load_data("data.ia")
        self.vue.enter_message.bind('<Return>', self.processus)
        self.vue.protocol("WM_DELETE_WINDOW", self.fin)
        self.event = {"name": "none", "content": ""}

    def processus(self, event=None):
        msg_user = self.vue.get_input()
        if msg_user == "Aurevoir":
            self.fin()
        elif self.event["name"] == "none":
            msg_bot = self.model.traitement_message(msg_user)
            if type(msg_bot) is str:
                self.vue.display_message("User: " + msg_user)
                self.vue.display_message("Nora: " + msg_bot)
                self.vue.display_message("Nora: Ai-je bien répondu ? (oui/non)")
                self.event = {"name": "ABR", "content": msg_user}
            elif type(msg_bot) is tuple:
                self.event = msg_bot[0]
                self.vue.display_message("User: " + msg_user)
                self.vue.display_message("Nora: "+msg_bot[1])
        elif self.event["name"] == "ABR":
            if msg_user == "oui":
                self.vue.display_message("User: " + msg_user)
                self.vue.display_message("Nora: Ok.")
                self.event = {"name": "none", "content": ""}
            else:
                self.event["name"] = "QDR"
                self.vue.display_message("User: " + msg_user)
                self.vue.display_message("Nora: " + "Que dois-je répondre ?")
        elif self.event["name"] == "QDR":
            self.model.save_in_data("un", self.event, msg_user)
            self.event = {"name": "none", "content": ""}
            self.vue.display_message(f"User: {msg_user}")
            self.vue.display_message("Nora: "+"D'accord, merci.")
        self.vue.enter_message.delete(0, END)

    def fin(self):
        dump(self.model, open("model.ngv2", "wb"))
        self.vue.quit()

    def start(self):
        self.vue.show_widget()
        self.vue.mainloop()
