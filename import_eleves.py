import os
import django
import csv
# Assurez-vous d'avoir le bon chemin ici
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings') 
django.setup()
from eleves.models import Eleves, Classe 
# --- ÉTAPE DE SUPPRESSION AJOUTÉE ---
print("Suppression des anciennes données...")
Eleves.objects.all().delete()
Classe.objects.all().delete() # Facultatif, si vous voulez remettre les classes à zéro

# --- Votre code d'importation ---
nombre_eleves_traites = 0 
# ... le reste du code de votre script ...

with open('eleves_import.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Récupère ou crée l'objet Classe
        classe_obj, created = Classe.objects.get_or_create(nom=row['classe'])
        
        # Met à jour ou crée l'objet Eleves
        Eleves.objects.update_or_create(
            code_eleve=row['code_eleve'],
            defaults={
                'prenom': row['prenom'],
                'nom': row['nom'],
                'classe': classe_obj # Utiliser l'objet Classe récupéré/créé
            }
        )
        nombre_eleves_traites += 1

print(f"{nombre_eleves_traites} élèves importés ou mis à jour !")