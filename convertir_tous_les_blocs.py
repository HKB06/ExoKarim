import os
import re
import json
from docx import Document

DOSSIER = "."
PATTERN_BLOCS = re.compile(r"BLOC(\d+)\sDS\.docx", re.IGNORECASE)

def extraire_infos_depuis_docx(fichier_docx):
    doc = Document(fichier_docx)
    texte = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

    # 🧠 On utilise un découpage basé sur "Partie X"
    parties = re.split(r"(Partie\s+\d+ ?: .+?)\n", texte)
    devoir = {}

    for i in range(1, len(parties), 2):
        titre = parties[i].strip()
        contenu = parties[i+1].strip()

        # Extraction plus souple des sections
        contexte = re.search(r"Contexte\s*:?(.+?)(Objectif|Objectifs|Travail|Questions|Critères)", contenu, re.DOTALL)
        taches = re.search(r"(Objectif|Objectifs|Travail à faire)\s*:?(.+?)(Critères|Questions|Modalités)", contenu, re.DOTALL)
        criteres = re.search(r"(Critères|Critères de performance|Critères d’évaluation).*?:\s*(.+?)(Questions|Objectifs|Modalités|$)", contenu, re.DOTALL)
        questions = re.findall(r"\d[\.\)]\s+(.*)", contenu)

        devoir[titre] = {
            "contexte": contexte.group(1).strip() if contexte else "",
            "taches": taches.group(2).strip() if taches else "",
            "criteres": criteres.group(2).strip() if criteres else "",
            "questions": questions
        }

    return devoir

def sauvegarder_si_valide(donnees, nom_fichier_json):
    try:
        json_str = json.dumps(donnees, indent=4, ensure_ascii=False)
        json.loads(json_str)  # validation
        with open(nom_fichier_json, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"✅ JSON OK : {nom_fichier_json}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalide pour {nom_fichier_json} :", e)

def traiter_tous_les_blocs():
    for fichier in os.listdir(DOSSIER):
        match = PATTERN_BLOCS.match(fichier)
        if match:
            bloc_num = match.group(1)
            print(f"🔄 Traitement du {fichier}...")

            try:
                donnees = extraire_infos_depuis_docx(fichier)
                sortie = f"devoirs_bloc{bloc_num}.json"
                sauvegarder_si_valide(donnees, sortie)
            except Exception as e:
                print(f"⚠️ Erreur dans le traitement de {fichier} :", e)

if __name__ == "__main__":
    traiter_tous_les_blocs()
