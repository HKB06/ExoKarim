import openai
import random
import json
import time
import os
from dotenv import load_dotenv

# 🔐 Chargement de la clé API depuis le fichier .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("⚠️ Clé API OpenAI non définie ! Ajoute-la dans un fichier .env.")

# 🔹 Liste d'erreurs typiques pour simulation humaine
ERREURS_SUBTILES = [
    ("inflation", "inflattion"),
    ("croissance économique", "croissanse economique"),
    ("régulation", "regulation"),
    ("volatilité", "volatilitée"),
    ("analyse financière", "analize financiere"),
    ("investissement", "investicement"),
    ("liquidité", "liquidé"),
    ("politique monétaire", "politique monnaitaire"),
    ("évaluation", "évalutation"),
    ("risque systémique", "riske systémique"),
]

ERREURS_GRAMMATICALES = [
    ("Les entreprises investissent", "Les entreprise investisse"),
    ("Il y a un impact", "Il a un impact"),
    ("Les marchés financiers sont", "Les marché financier est"),
    ("Les réglementations évoluent", "Les régulations évolue"),
]

ERREURS_TYPOS = [
    ("l'économie", "l economis"),
    ("financier", "finacnier"),
    ("stratégique", "straétgique"),
    ("analyse", "anlyse"),
]

FORMULATIONS_MALADROITES = [
    ("En conclusion,", "Donc, ben, en fait,"),
    ("Il est essentiel de noter que", "Bon, faut quand même dire que"),
    ("Les résultats montrent que", "Si on regarde bien, on voit que"),
    ("D’un point de vue économique,", "En vrai, sur l'économie,"),
]

# 🔹 Fonction pour introduire des erreurs
def introduire_erreurs(texte):
    if random.random() < 0.4:  # 40% de chance d'introduire une faute d'orthographe
        erreur = random.choice(ERREURS_SUBTILES)
        texte = texte.replace(erreur[0], erreur[1], 1)

    if random.random() < 0.3:  # 30% de chance d'introduire une faute grammaticale
        erreur = random.choice(ERREURS_GRAMMATICALES)
        texte = texte.replace(erreur[0], erreur[1], 1)

    if random.random() < 0.3:  # 30% de chance d'introduire une faute typographique
        erreur = random.choice(ERREURS_TYPOS)
        texte = texte.replace(erreur[0], erreur[1], 1)

    if random.random() < 0.3:  # 30% de chance d'ajouter une formulation maladroite
        erreur = random.choice(FORMULATIONS_MALADROITES)
        texte = texte.replace(erreur[0], erreur[1], 1)

    return texte

# 🔹 Générer un jeu de données massif avec OpenAI
def generer_jeu_de_donnees(n_samples=1000, output_file="jeu_de_donnees_massif.json"):
    dataset = []
    
    for i in range(n_samples):
        print(f"⏳ Génération de l'exemple {i+1}/{n_samples}...")

        prompt = "Explique brièvement un concept économique simple (inflation, marché boursier, taux d'intérêt, volatilité, etc.)."
        
        try:
            response = openai.ChatCompletion.create(

                model="gpt-4",
                temperature=random.uniform(0.7, 1.0),
                messages=[
                    {"role": "system", "content": "Tu es un professeur d'économie qui explique des concepts de manière accessible."},
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            print(f"⚠️ Erreur lors de l'appel API : {e}")
            time.sleep(5)  # Pause en cas d'erreur
            continue

        texte_original = response.choices[0].message.content
        texte_avec_erreurs = introduire_erreurs(texte_original)

        dataset.append({
            "original": texte_original,
            "avec_erreurs": texte_avec_erreurs
        })

        # Pause pour éviter les restrictions API
        time.sleep(1)

    # 🔹 Sauvegarde en JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Fichier '{output_file}' généré avec succès avec {len(dataset)} entrées.")

# 🔹 Exécution
generer_jeu_de_donnees(n_samples=1000)
