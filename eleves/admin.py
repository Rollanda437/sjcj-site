from django.contrib import admin
from .models import Eleves, Matiere, Semestre, Note

@admin.register(Eleves)
class ElevesAdmin(admin.ModelAdmin):
    list_display = ('code_eleve', 'nom', 'prenom', 'classe')
    search_fields = ('code_eleve', 'nom', 'prenom')
    list_filter = ('classe',)

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient')
    search_fields = ('nom',)

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee_scolaire')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'semestre', 'moyenne_semestre', 'appreciation')
    list_filter = ('semestre', 'matiere')
    search_fields = ('eleve__nom', 'eleve__prenom', 'eleve__code_eleve')