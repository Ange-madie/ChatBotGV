# Importation
from tkinter import *
from pickle import dump, load

class ChatBot(Tk):

    def __init__(self):
        super().__init__()
        self.data, self.mot = load(open("data.ia", "rb"))
        self.savem = {"tag": "", "rep": "", "nrep": ""}
        # self.mot = load(open("mot.ia", "rb"))
        self.ignorer = ["?", "-", ".", "!", "_", " ", ","]
        self.peu_point = ["Qui", "est", "C'est", "quoi"]
        self.reponse = ""
        #Fenetre Principale
        self.title("Nora GV 1")
        self.protocol("WM_DELETE_WINDOW", self.fin)
        # Widget de la fenêtre
        self.affiche_message = Text(self)
        self.envoyez = Button(self, text="Envoyez", bg="green", command=self.envoie)
        self.entre_message = Entry(self, width=100)
        self.entre_message.bind('<Return>', self.envoie)
        self.affiche_message.insert(END, "Posez une demande si vous ne voulez rien tapez '/'")
        self.affiche_message.config(fg="green", bg="black")


    def separateur_mot(self, phrase: str):
        """Fonction pour diviser une phrase en mots."""
        mots = []
        l = []
        for letter in phrase:
            if letter not in self.ignorer:
                l.append(letter)
            else:
                if l:
                    mots.append(''.join(l))
                l = []
        if l:
            mots.append(''.join(l))

        return tuple(mots)

    def test_in_tab(self, tab1: list | tuple, tab2: list | tuple):
        for value in tab1:
            if value in tab2:
                return True

        return False

    def all_test_in_tab(self, tab1: list | tuple, tab2: list | tuple):
        for value in tab1:
            if value not in tab2:
                return False

        return True
    
    def shower(self):
        self.affiche_message.grid(row=0, column=0, columnspan=2)
        self.envoyez.grid(row=1, column=1)
        self.entre_message.grid(row=1, column=0)

    def show_message(self, message):
        self.affiche_message.insert(END, "\n"+message)

    def save_in_data(self, step: str, another = ""):
        if step == "un":
            self.save_mot(self.reponse)
            self.show_message("User: " + self.reponse)
            self.show_message("Nora: Que dois-je répondre ?")
            self.savem["tag"] = "dmr"
            self.savem["rep"] = self.reponse
            self.data[self.reponse] = []
            self.data[self.reponse].append(self.separateur_mot(self.reponse))
            self.entre_message.delete(0, END)
        elif step == "un'":
            self.save_mot(another)
            self.show_message("Nora: Que dois-je répondre ?")
            self.savem["tag"] = "dmr"
            self.savem["rep"] = another
            self.data[another] = []
            self.data[another].append(self.separateur_mot(another))
            self.entre_message.delete(0, END)
        elif step == "deux":
            self.data[self.savem["rep"]].append(self.reponse)
            self.show_message("User: "+self.reponse)
            self.save_mot(self.reponse)
            self.show_message("Nora: D'accord, merci.")
            self.savem["tag"] = ""
            self.savem["rep"] = ""
            self.entre_message.delete(0, END)
        else:
            print("Bad parameter value for step.")


    def envoie(self, event=None):
        self.reponse = self.entre_message.get()
        if self.reponse == "/":
            self.fin()
        elif self.savem["tag"] == "dmr":
            self.save_in_data("deux")
        elif self.savem["tag"] == "dmc":
            if self.reponse == "oui":
                # Mise dans le fichier data de la nouvelle information après test de non appartenance au fichier data
                if not self.all_test_in_tab(self.separateur_mot(self.savem["rep"]), self.mot) or not self.test_in_tab(self.separateur_mot(self.savem["rep"]), self.mot):
                    self.save_mot(self.savem["rep"])
                    self.data[self.savem["rep"]] = []
                    self.data[self.savem["rep"]].append(self.separateur_mot(self.savem["rep"]))
                    self.data[self.savem["rep"]].append(self.savem["nrep"])
                    self.entre_message.delete(0, END)
                    self.show_message("Nora: Ok, User.")
                else:
                    self.entre_message.delete(0, END)
                    self.show_message("Nora: Ok.")
                self.savem["tag"] = ""
                self.savem["rep"] = ""
                self.savem["nrep"] = ""
            else:
                inter = self.savem["rep"]
                self.savem["tag"] = ""
                self.savem["rep"] = ""
                self.savem["nrep"] = ""
                self.save_in_data("un'", inter)
                self.save_mot(inter)
        elif not self.test_in_tab(self.separateur_mot(self.reponse), self.mot):
            self.save_mot(self.reponse)
            self.save_in_data("un")
        elif self.test_in_tab(self.separateur_mot(self.reponse), self.mot):
            botRep = self.evaluation()
            self.save_mot(self.reponse)
            self.show_message("User: "+self.reponse)
            self.show_message(f"Nora: {botRep}")
            self.show_message("Nora: Ai-je bien répondu ? (oui/non)")
            self.savem["tag"] = "dmc"
            self.savem["rep"] = self.reponse
            self.savem["nrep"] = botRep
            self.entre_message.delete(0, END)
        else:
            botRep = self.evaluation()
            self.show_message("User: "+self.reponse)
            self.show_message(f"Nora: {botRep}")
            self.show_message("Nora: Ai-je bien répondu ? (oui/non)")
            self.savem["tag"] = "dmc"
            self.savem["rep"] = self.reponse
            self.savem["nrep"] = botRep
            self.entre_message.delete(0, END)



    def save_mot(self, phrase: str):
        phrase = self.separateur_mot(phrase)
        for value in phrase:
            if value not in self.mot:
                self.mot.append(value)
            else:
                continue

    def evaluation(self) -> str:
        cpt = 0
        select = 0
        choisie = ""
        # self.save_mot(self.reponse)
        tab_reponse = self.separateur_mot(self.reponse)
        print(tab_reponse)
        for cle, valeur in self.data.items():
            for w in valeur[0]:
                if w in tab_reponse:
                    if w in self.peu_point:
                        cpt += 0.2
                    else:
                        cpt += 1
            self.data[cle].append(cpt)
            cpt = 0
        for cle, valeur in self.data.items():
            if valeur[2] > 0:
                if valeur[2] > select:
                    select = valeur[2]
        for cle in self.data.keys():
            if self.data[cle][2] == select:
                choisie = self.data[cle][1]
        for cle in self.data.keys():
            self.data[cle].pop()
        return choisie

    def fin(self):
        save = (self.data, self.mot)
        dump(save, open("data.ia", "wb"))
        # dump(self.mot, open("mot.ia", "wb"))
        self.destroy()


if __name__ == "__main__":
    test = ChatBot()
    test.shower()
    test.mainloop()


