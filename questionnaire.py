import json
import sys

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data):
        #transforme les donnéees choix tuple (titre, bool 'bonne reponse') -> [choix1, choix2, ...]
        choix = [i[0] for i in data["choix"]]
        #trouve le bon choix en fonction du bool 'bonne réponse'
        bonne_reponse = [i[0] for i in data["choix"] if i[1]]
        #si aucune bonne reponse ou plusieurs obnnes réponses -> anomalies dans les données
        if len(bonne_reponse) != 1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser(self, numero_question, nbr_questions):
        print(f"QUESTION n°{numero_question + 1}/{nbr_questions}")
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
        #suprrime les questions "none" sans recréer un objet
        questions = [i for i in questions if i]
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])
    
    def from_json_file(filename):
        try:
            f =  open(filename, "r")
            data = json.load(f)
            f.close()
        except:
            print("Exception lors de l'ouverture ou de la lecture du fichier")
            return None
        return Questionnaire.from_json_data(data)

    def lancer(self):
        score = 0
        nbr_questions = len(self.questions)

        print("-------")
        print("Questionnaire : " + self.titre)
        print("Catégorie : " + self.categorie)
        print("Difficulté : " + self.difficulte)
        print("Nombre de question :", nbr_questions)
        print("-------")
        
        for numero_question in range(nbr_questions):
            question = self.questions[numero_question]
            if question.poser(numero_question, nbr_questions):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


    if len(sys.argv) < 2:
        print("Erreur vous devez spécifier le nom du fichier json à charger")
        exit(0)

json_filename = sys.argv[1]

questionnaire = Questionnaire.from_json_file(json_filename)

if questionnaire != None:
    questionnaire.lancer()