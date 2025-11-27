from django.contrib import admin
from .models import Eleves, Note, Matiere, Classe, Semestre

class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = (
        'matiere',
        'semestre',
        'inter1', 'inter2', 'inter3', 'inter4',
        'devoir1', 'devoir2',
        'appreciation'
    )
    autocomplete_fields = ['matiere']
    # Tu peux tout modifier, rien n’est bloqué
    readonly_fields = ()

    class Media:
        css = {'all': ('css/admin_bulletin.css',)}  # si tu veux la gardée


@admin.register(Eleves)
class ElevesAdmin(admin.ModelAdmin):
    list_display = ('code_eleve', 'prenom', 'nom', 'classe', 'nb_absence', 'nb_retard')
    list_filter = ('classe',)
    search_fields = ('code_eleve', 'prenom', 'nom')
    inlines = [NoteInline]
    ordering = ('code_eleve',)

    def get_readonly_fields(self, request, obj=None):
        return []  # tout est modifiable


# Bonus : on enregistre aussi les autres modèles pour qu’ils apparaissent bien
admin.site.register(Classe)
admin.site.register(Matiere)
admin.site.register(Semestre)