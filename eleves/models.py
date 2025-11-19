from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from firebase_config import db

class Eleves(models.Model):
    code_eleve = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    classe = models.CharField(max_length=20)
    nb_retard = models.IntegerField(default=0)
    nb_absence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.code_eleve})"

    def to_dict(self):
        return {
            'code_eleve': self.code_eleve,
            'nom': self.nom,
            'prenom': self.prenom,
            'classe': self.classe,
            'nb_retard': self.nb_retard,
            'nb_absence': self.nb_absence,
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.code_eleve = data['code_eleve']
        obj.nom = data['nom']
        obj.prenom = data['prenom']
        obj.classe = data['classe']
        obj.nb_retard = data.get('nb_retard', 0)
        obj.nb_absence = data.get('nb_absence', 0)
        return obj

    @classmethod
    def from_firestore(cls, doc):
        data = doc.to_dict()
        obj = cls()
        obj.pk = doc.id
        obj.code_eleve = data['code_eleve']
        obj.nom = data['nom']
        obj.prenom = data['prenom']
        obj.classe = data['classe']
        obj.nb_retard = data.get('nb_retard', 0)
        obj.nb_absence = data.get('nb_absence', 0)
        return obj

    def save_to_firestore(self):
        db.collection('eleves').document(self.code_eleve).set(self.to_dict())

    @classmethod
    def get_all_from_firestore(cls):
        docs = db.collection('eleves').stream()
        return [cls.from_firestore(doc) for doc in docs]


class Note(models.Model):
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE)
    matiere = models.CharField(max_length=100)
    semestre = models.CharField(max_length=2)
    inter1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    inter2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    inter3 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    inter4 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    devoir1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    devoir2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    appreciation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.eleve} - {self.matiere}"

    def moyenne_inter(self):
        notes = [n for n in [self.inter1, self.inter2, self.inter3, self.inter4] if n]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_devoir(self):
        notes = [n for n in [self.devoir1, self.devoir2] if n]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_semestre(self):
        inter = self.moyenne_inter() or 0
        devoir = self.moyenne_devoir() or 0
        return round((inter + 2*devoir)/3, 2)