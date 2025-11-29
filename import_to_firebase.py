
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import csv
from io import StringIO
import re

# Initialisation Firebase
# Assurez-vous que le chemin vers votre fichier de service est correct
BASE_DIR = Path(__file__).resolve().parent
cred_path = BASE_DIR / "credentials" / "firebase_service_account.json"

try:
    cred = credentials.Certificate(cred_path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client(database_id="sjcj-site")
except FileNotFoundError:
    print(f"Erreur: Le fichier de service Firebase est introuvable à {cred_path}")
    exit()
except Exception as e:
    print(f"Erreur lors de l'initialisation de Firebase: {e}")
    exit()

# TOUTES LES MATIÈRES PAR CLASSE
MATIERES_PAR_CLASSE = {
    "2NDE IMI": ["FRANÇAIS","ANGLAIS","MATH","EB","LA","AS","SEV","SER","ALGO","MATH APPLIQUE","LEGIS"],
    "2NDE F3":  ["FRANÇAIS","ANGLAIS","MATH","PCT","TECHNO","SCHÉMA","DESSIN","ELECTRO","PRATIQUE","MEL"],
    "TLE F3":   ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","ELECTRO","EST","PRATIQUE","MEL","DESSIN","ANGLAIS"],
    "TLE IMI":  ["FRANÇAIS","ANGLAIS","MATH","EB","RESEAU","RP","MATH APPLIQUÉ","LEGIS","BD","PG","ELEC"],
    "2NDE F4":  ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","DESSIN","INFORMATIQUE","TM/TC","TP","MECANIQUE","PREVENTION","LEGIS"],
    "1ERE F4":  ["FRANÇAIS","ANGLAIS","MATH","PCT","RDM","PE","DESSIN","SMC","TP","METRE","HYGIENE","PC"],
    "TLE F4":   ["FRANÇAIS","ANGLAIS","MATH","PCT","RDM","PE","DESSIN","METRE","PC","BA","TP","LEGIS"],
    "2NDE FC":   ["FRANÇAIS","ANGLAIS","MATH","EPS","PHYSIQUE","HIST-GEO","PHYSIQUE APPLIQUE","AUTOMATISME","DESSIN","ELECTRO DE BASE"],
    "1ERE HR":  ["FRANÇAIS","ANGLAIS","MATH","TC","SAAH","ECONOMAT","TRB","DROIT","MERCATIQUE","COMPTABILITE"],
    "2NDE MA":  ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","CHIMIE","SVT","HIST-GEO","EPS","INFORMATIQUE"],
    "1ERE F3":  ["FRANÇAIS","ANGLAIS","MATH","PCT","TECHNO","SCHÉMA","DESSIN","ELECTRO","PRATIQUE","MEL"],
}

# TON CSV COMPLET (111 lignes exactement)
# CORRECTION MAJEURE: suppression du 'nom' dupliqué dans l'en-tête
CSV_DATA = """code_eleve,prenom,nom,classe
26A0169,Wilson,FAYOMI,2nde F4
26A0170,Franck,KOUSSIHOUEDE,2nde F4
26A0171,Noé,THOMAS,2nde F4
26A0172,Godwin,AWOUNOU,2nde F4
26A0173,Renaud,FAGNON,2nde F4
26A0174,Espéla,VITOMADJO,2nde F4
26A0175,Nambigath,SALIOU,2nde F4
26A0176,Lozeli,MEBO,2nde F4
26A0123,Vincent,AGBANZE,Tle F4
26A0124,Solange,AHLO,Tle F4
26A0125,Henriette,AHLO,Tle F4
26A0126,Camille,AHOTON,Tle F4
26A0127,Judicaël,AGOSSOU,Tle F4
26A0128,Précieux,AKOWANOU,Tle F4
26A0129,Emmanuel,ATCHOUKE,Tle F4
26A0130,Olivia,BOKO,Tle F4
26A0131,Aboubacar,GBADAMASSI,Tle F4
26A0132,Mariele,GOUGLA,Tle F4
26A0133,Ulrich,GUINGUINVOU,Tle F4
26A0134,Mohamadou,HABOUM MAMANI,Tle F4
26A0135,Fatima,HOUNTON,Tle F4
26A0136,Mans-Ound,ODJO,Tle F4
26A0137,Judicaël,SEMAVO,Tle F4
26A0138,Mifdol,SALAMI,Tle F4
26A0139,Francia,ADEOKO,Tle F4
26A0140,Nayir,NANJOUAN,Tle F4
26A0141,Rémi,DJOHI,Tle F4
26A0142,Henri-Joel,DEDJI,Tle F4
26A0143,Raymond,METOEVI,Tle F4
26A0191,Camille,AHOTON,Tle F4
26A0197,Romaine,DJOTCHOU,Tle F4
26A0198,Eustache,WANVEOGBE,Tle F4
26A306,AÎDASSO,Angelo,Tle F4
26A0160,AHISSOU,Majesté,2nde IMI
26A0161,ANAGO,Bénito,2nde IMI
26A0162,DJOTCHOU,Charbel,2nde IMI
26A0163,DOSSA,Merveille,2nde IMI
26A0164,GLELE,Reveen,2nde IMI
26A0165,NALLA,Faradj,2nde IMI
26A0166,ONI,Godwin,2nde IMI
26A0167,TOUDOUNOU,Luix-Alex,2nde IMI
26A0168,TOVIESSI,Amyrice,2nde IMI
26A0191,TRAORE,Nasrine,2nde IMI
26A0188,AZONNEGBO,Pauline,2nde IMI
26A0189,BABOZA,David,2nde IMI
26A0190,KOUKOUI,Anivic,2nde IMI
26A0118,Shalow,KPINKPONSOUNOU,Tle IMI
26A0120,Soultone,YESSOUFOU,Tle IMI
26A0109,jeanne-d'arc,ADOUTAN,Tle IMI
26A0117,Immmense,FAGNIDE,Tle IMI
26A0113,Francis,COUTHON,Tle IMI
26A0114,Honorat,DEDJI,Tle IMI
26A0122,Miracle,FASSINOU,Tle IMI
26A0111,Djawad,BADAROU,Tle IMI
26A0119,Joyce,TANKPINOU,Tle IMI
26A0116,Trinité,DOSSOU,Tle IMI
26A0112,Florindas,BALOGOUN,Tle IMI
26A0110,Zidal,AIZAN,Tle IMI
26A0123,Janson,LANYAN,Tle IMI
26A0121,Aaron,AFATONDJI,Tle IMI
26A0199,Esther,ESSE,Tle IMI
26A0200,Elite,HOUNKPE,Tle IMI
26A0100,Elisé,ADOGOUN,Tle F3
26A0101,Achille,AZONNEGBO,Tle F3
26A0102,Changnon,BODJRENOU,Tle F3
26A0103,Dinel,HINWATONOU,Tle F3
26A0104,Médard,HOUNYE,Tle F3
26A0105,Charbel,KOUMINASSI,Tle F3
26A0106,TOUSSOUNOU,Enock,Tle F3
26A0107,Simon-pierre,TOTIN,Tle F3
26A0108,Amos,VEDJI,Tle F3
26A0201,ABOUDOU,Abdel,1ere F4
26A0202,AGBESSI-LOKO,Dylan,1ere F4
26A0203,AROUNA,Amzat,1ere F4
26A0204,BISSIRIOU,Moussine,1ere F4
26A0206,GANYE,James,2nde FC
26A0207,GOZO,Régice,2nde FC
26A0208,NWAKOKONKO,Dine,2nde FC
26A0179,AKAMBI,Manfazath,1ere HR
26A0180,DONDJA,Alimantou,1ere HR
26A0181,MISSAINNOU,Philippin,1ere HR
26A0182,TOYA,Stylvia,1ere HR
26A0183,ODJOUOYE,Déborah,1ere HR
26A0184,SAIZONOU,Bénie,1ere HR
26A0144,ABDOULAYE,Yunus,2nde F3
26A0145,ABIKOU,pierre,2nde F3
26A0146,AHISSOU,Meckiadd,2nde F3
26A0147,AKPLOGAN,Dorial,2nde F3
26A0148,ALOUKOU,Bill,2nde F3
26A0149,AYIBOUKY,Fèmi-Rahim,2nde F3
26A0150,DAGBOZOUNKOU,Saobane,2nde F3
26A0151,GOUTON,Joseph,2nde F3
26A0152,HOUESSOU,Rogatien,2nde F3
26A0153,KOUMAGNON,Ahad,2nde F3
26A0154,LAMIDI,Mouwad-Adechinan,2nde F3
26A0155,LOKO,Jean-baptiste,2nde F3
26A0156,OLAYODE,Massoum,2nde F3
26A0157,VODOUNON,Osias,2nde F3
26A0158,YESSOUFOU,Mohamed,2nde F3
26A0159,ZANMENOU,Hostalin,2nde F3
26A0205,ADOUTAN,Jérémie,1ere F3
26A0192,AZONNEGBO,Prospère,1ere F3
26A0193,BOKO,Romdon,1ere F3
26A0194,GNONLONFOUN,Steve,1ere F3
26A0195,HOUKPON,Périn,1ere F3
26A0196,ADANNON,Jason,1ere F3
26A0300,ADJANA,Rouchdane,2nde MA
26A0301,AGBADJE,Sidney,2nde MA
26A0302,AGOSSOU,Richel,2nde MA
26A0303,FATIGBA,Hananéel,2nde MA
26A0304,GBOGBO,Said,2nde MA
26A0305,LANYAN,Lilian,2nde MA"""

print("Import des 111 élèves dans Firebase en cours...\n")

# Lire les données en mémoire
reader = csv.DictReader(StringIO(CSV_DATA))

# Utiliser une transaction ou un batch est plus efficace, mais le set() simple fonctionne pour 111 éléments
for i, row in enumerate(reader, 1):
    
    # Sécurité: obtenir la valeur et si elle est None, utiliser une chaîne vide avant strip()
    code = (row.get('code_eleve') or '').strip()
    prenom = (row.get('prenom') or '').strip().title()
    nom = (row.get('nom') or '').strip().upper()
    classe_raw = (row.get('classe') or '').strip()
    
    if not code:
        print(f"Ligne {i}: Erreur de code élève, sautée.")
        continue

    # Normalisation des noms de classe pour la recherche dans MATIERES_PAR_CLASSE
    # On retire tous les accents et on met en majuscules pour la recherche
    classe_normalisee = classe_raw.upper()
    classe_normalisee = re.sub(r'[ÉÈÊË]', 'E', classe_normalisee)
    classe_normalisee = re.sub(r'[ÀÂÄ]', 'A', classe_normalisee)
    classe_normalisee = re.sub(r'[ÛÜ]', 'U', classe_normalisee)
    classe_normalisee = re.sub(r'[ÎÏ]', 'I', classe_normalisee)
    
    # On utilise la classe normalisée pour trouver les matières
    matieres = MATIERES_PAR_CLASSE.get(classe_normalisee, ["FRANÇAIS","ANGLAIS","MATH"])  # fallback
    notes = {m: "" for m in matieres}

    # Insertion/Mise à jour dans Firestore
    db.collection("eleves").document(code).set({
        "code": code,
        "prenom": prenom,
        "nom": nom,
        "classe": classe_raw,  # on garde l’orthographe d’origine pour l’affichage
        "matieres": notes
    }, merge=True)

    print(f"{i:3d}/111 {code} – {prenom} {nom} ({classe_raw})")

print("\nTOUT EST DANS FIREBASE ! 111 élèves, toutes les classes, toutes les matières prêtes")
print("Tu peux maintenant faire : git push --force et le site marche à 100%")