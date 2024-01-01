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
        self.peuPoint = ["Qui", "est", "C'est", "quoi"]
        self.reponse = ""
        #Fenetre Principale
        self.title("Nora GV 1")
        self.protocol("WM_DELETE_WINDOW", self.fin)
        # Widget de la fenêtre
        self.afficheMessage = Text(self)
        self.envoyez = Button(self, text="Envoyez", bg="green", command=self.envoie)
        self.entreMessage = Entry(self, width=100)
        self.entreMessage.bind('<Return>', self.envoie)
        self.afficheMessage.insert(END, "Posez une demande si vous ne voulez rien tapez '/'")
        self.afficheMessage.config(fg="green", bg="black")

    # Fonction pour diviser une phrase en mot
    def separateurMot(self, phrase: str):
        mot = []
        l = ""
        for i in range(len(phrase)):
            if phrase[i] not in self.ignorer:
                l = l + phrase[i]
            else:
                if not l == '':
                    mot.append(l)
                l = ""
        if not l == '':
            mot.append(l)

        return tuple(mot)

    def testInTab(self, tab1: list | tuple, tab2: list | tuple):
        retour = False
        for value in tab1:
            if value in tab2:
                return True
            else:
                retour = False
        return retour

    def allTestInTab(self, tab1: list | tuple, tab2: list | tuple):
        test = False
        for value in tab1:
            if value in tab2:
                test = True
            else:
                test = False
        return test
    def shower(self):
        self.afficheMessage.grid(row=0, column=0, columnspan=2)
        self.envoyez.grid(row=1, column=1)
        self.entreMessage.grid(row=1, column=0)

    def showMessage(self, message):
        self.afficheMessage.insert(END, "\n"+message)

    def saveInData(self, step: str, another = ""):
        if step == "un":
            self.saveMot(self.reponse)
            self.showMessage("User: " + self.reponse)
            self.showMessage("Nora: Que dois-je répondre ?")
            self.savem["tag"] = "dmr"
            self.savem["rep"] = self.reponse
            self.data[self.reponse] = []
            self.data[self.reponse].append(self.separateurMot(self.reponse))
            self.entreMessage.delete(0, END)
        elif step == "un'":
            self.saveMot(another)
            self.showMessage("Nora: Que dois-je répondre ?")
            self.savem["tag"] = "dmr"
            self.savem["rep"] = another
            self.data[another] = []
            self.data[another].append(self.separateurMot(another))
            self.entreMessage.delete(0, END)
        elif step == "deux":
            self.data[self.savem["rep"]].append(self.reponse)
            self.showMessage("User: "+self.reponse)
            self.saveMot(self.reponse)
            self.showMessage("Nora: D'accord, merci.")
            self.savem["tag"] = ""
            self.savem["rep"] = ""
            self.entreMessage.delete(0, END)
        else:
            print("Bad parameter value for step.")


    def envoie(self, event=None):
        self.reponse = self.entreMessage.get()
        if self.reponse == "/":
            self.fin()
        elif self.savem["tag"] == "dmr":
            self.saveInData("deux")
        elif self.savem["tag"] == "dmc":
            if self.reponse == "oui":
                # Mise dans le fichier data de la nouvelle information après test de non appartenance au fichier data
                if not self.allTestInTab(self.separateurMot(self.savem["rep"]), self.mot) or not self.testInTab(self.separateurMot(self.savem["rep"]), self.mot):
                    self.saveMot(self.savem["rep"])
                    self.data[self.savem["rep"]] = []
                    self.data[self.savem["rep"]].append(self.separateurMot(self.savem["rep"]))
                    self.data[self.savem["rep"]].append(self.savem["nrep"])
                    self.entreMessage.delete(0, END)
                    self.showMessage("Nora: Ok, User.")
                else:
                    self.entreMessage.delete(0, END)
                    self.showMessage("Nora: Ok.")
                self.savem["tag"] = ""
                self.savem["rep"] = ""
                self.savem["nrep"] = ""
            else:
                inter = self.savem["rep"]
                self.savem["tag"] = ""
                self.savem["rep"] = ""
                self.savem["nrep"] = ""
                self.saveInData("un'", inter)
                self.saveMot(inter)
        elif not self.testInTab(self.separateurMot(self.reponse), self.mot):
            self.saveMot(self.reponse)
            self.saveInData("un")
        elif self.testInTab(self.separateurMot(self.reponse), self.mot):
            botRep = self.evaluation()
            self.saveMot(self.reponse)
            self.showMessage("User: "+self.reponse)
            self.showMessage(f"Nora: {botRep}")
            self.showMessage("Nora: Ai-je bien répondu ? (oui/non)")
            self.savem["tag"] = "dmc"
            self.savem["rep"] = self.reponse
            self.savem["nrep"] = botRep
            self.entreMessage.delete(0, END)
        else:
            botRep = self.evaluation()
            self.showMessage("User: "+self.reponse)
            self.showMessage(f"Nora: {botRep}")
            self.showMessage("Nora: Ai-je bien répondu ? (oui/non)")
            self.savem["tag"] = "dmc"
            self.savem["rep"] = self.reponse
            self.savem["nrep"] = botRep
            self.entreMessage.delete(0, END)



    def saveMot(self, phrase: str):
        phrase = self.separateurMot(phrase)
        for value in phrase:
            if value not in self.mot:
                self.mot.append(value)
            else:
                continue

    def evaluation(self) -> str:
        cpt = 0
        select = 0
        choisie = ""
        # self.saveMot(self.reponse)
        tabReponse = self.separateurMot(self.reponse)
        print(tabReponse)
        for cle, valeur in self.data.items():
            for w in valeur[0]:
                if w in tabReponse:
                    if w in self.peuPoint:
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


