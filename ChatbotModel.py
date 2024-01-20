from pickle import dump, load
from include import *

class ChatbotModel:
    def __init__(self):
        self.message = ""
        self.data = {}
        self.mots = []
        self.synonyme = {}
        self.ignorer = ["?", "-", ".", "!", "_", " ", ","]
        self.peu_point = ["Qui", "est", "C'est", "quoi", "es", "Qu'est", "que", "ce"]
        self.event = {"name": "none", "content": ""}

    def traitement_message(self, message):
        rep = ""
        if test_in_tab(separateur_mot(message), self.mots):
            rep = self.evaluation(separateur_mot(message))
        else:
            self.event["name"] = "QDR"
            self.event["content"] = message
            rep = (self.event, "Que dois-je répondre ?")
        return rep

    def load_data(self, filepath):
        self.data, self.mots, self.synonyme = load(open(filepath, "rb"))

    def save_mot(self, phrase: str):
        phrase = separateur_mot(phrase)
        for value in phrase:
            if value not in self.mots:
                self.mots.append(value)
            else:
                continue

    def save_in_data(self, step: str, value, rep: str):
        if step == "un":
            self.data[value["content"]] = []
            self.data[value["content"]].append(separateur_mot(value["content"]))
            self.data[value["content"]].append(rep)
            self.save_mot(value["content"])

    def evaluation(self, tab: tuple) -> str:
        cpt = 0
        select = 0
        choisie = ""
        # self.save_mot(self.reponse)
        tab_reponse = tab
        print(tab_reponse)
        for cle, valeur in self.data.items():
            for w in valeur[0]:
                if w in tab_reponse:
                    if w in self.peu_point:
                        cpt += 0.2
                    else:
                        cpt += 1
                else:
                    if w in self.synonyme.keys():
                        if self.synonyme[w] in tab_reponse:
                            cpt += 1
            self.data[cle].append(cpt)
            cpt = 0
        for cle, valeur in self.data.items():
            if valeur[2] > 0:
                if valeur[2] > select:
                    select = valeur[2]
        print(select)
        for cle in self.data.keys():
            if self.data[cle][2] == select:
                choisie = self.data[cle][1]
        for cle in self.data.keys():
            self.data[cle].pop()
        return choisie

