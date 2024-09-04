import json

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data):
        choix = [i[0] for i in data["choix"]]
        bonne_reponse = [i[0] for i in data["choix"] if i[1]]
        if len(bonne_reponse) != 1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser(self):
        print("QUESTION")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte

    def from_json_data(data):
        questionnaire_data = data["questions"]
        questions = [Question.from_json_data(i) for i in questionnaire_data]
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])

    def lancer(self):
        score = 0
        
        print("-------")
        print("Questionnaire : " + self.titre)
        print("Catégorie : " + self.categorie)
        print("Difficulté : " + self.difficulte)
        print("Nombre de question :", len(self.questions))
        print("-------")
        
        for question in self.questions:
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


f =  open("cinema_alien_debutant.json", "r")
data = json.load(f)
f.close()

Questionnaire.from_json_data(data).lancer()