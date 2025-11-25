import csv
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_service_account.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# LES VRAIES MATIÈRES DU SJCI BÉNIN 2025 (tes noms exacts)
MATIERES_PAR_CLASSE = {
    "2NDE IMI": ["FRANÇAIS","ANGLAIS","MATH","EB","LA","AS","SEV","SER","ALGO","MATH APPLIQUE","LEGIS"],
    "2NDE F3":  ["FRANÇAIS","ANGLAIS","MATH","PCT","TECHNO","SCHÉMA","DESSIN","ELECTRO","PRATIQUE","MEL"],
    "TLE F3":   ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","ELECTRO","EST","PRATIQUE","MEL","DESSIN","ANGLAIS"],
    "TLE IMI":  ["FRANÇAIS","ANGLAIS","MATH","EB","RESEAU","RP","MATH APPLIQUÉ","LEGIS","BD","PG","ELEC"],
    "2NDE F4":  ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","DESSIN","INFORMATIQUE","TM/TC","TP","MECANIQUE","PREVENTION","LEGIS"],
    "1ERE F4":  ["FRANÇAIS","ANGLAIS","MATH","PCT","RDM","PE","DESSIN","SMC","TP","METRE","HYGIENE","PC"],
    "TLE F4":   ["FRANÇAIS","ANGLAIS","MATH","PCT","RDM","PE","DESSIN","METRE","PC","BA","TP","LEGIS"],
    "2NDE FC":  ["FRANÇAIS","ANGLAIS","MATH","EPS","PHYSIQUE","HIST-GEO","PHYSIQUE APPLIQUE","AUTOMATISME","DESSIN","ELECTRO DE BASE"],
    "1ERE HR":  ["FRANÇAIS","ANGLAIS","MATH","TC","SAAH","ECONOMAT","TRB","DROIT","MERCATIQUE","COMPTABILITE"],
}

def trouver_matieres(classe):
    classe = classe.upper().replace("È", "E").strip()
    for key in MATIERES_PAR_CLASSE:
        if key in classe or classe.startswith(key):   # ← CORRIGÉ ICI
            return MATIERES_PAR_CLASSE[key]
    print(f"Classe non reconnue → {classe} → matières par défaut")
    return ["FRANÇAIS","ANGLAIS","MATH"]

# Import complet depuis ton CSV
with open('eleves_import.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    total = 0
    for row in reader:
        code = row['code_eleve'].strip()
        classe = row['classe'].strip()
        matieres = trouver_matieres(classe)

        eleve = {
            "code_eleve": code,
            "prenom": row['prenom'].strip().title(),
            "nom": row['nom'].strip().upper(),
            "classe": classe,
            "matieres": matieres,
            "importe_le": firestore.SERVER_TIMESTAMP
        }

        # ID = code_eleve → pas de doublon
        db.collection("eleves").document(code).set(eleve, merge=True)
        print(f"OK → {eleve['prenom']} {eleve['nom']} – {classe} → {len(matieres)} matières")
        total += 1

print(f"\nFINI ! {total} élèves du SJCI importés avec LES VRAIES MATIÈRES !")
print("Tu peux maintenant faire les bulletins, les notes, tout ce que tu veux.")
input("\nAppuie sur Entrée pour fermer...")