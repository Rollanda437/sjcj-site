
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Eleves, Note, Classe, Matiere, Semestre

# Toutes les matières par classe (exactement comme ton JS)
MATIERES_PAR_CLASSE = {
    "1ère F4": ["FRANÇAIS","ANGLAIS","MATH","PCT","RDM","PE","DESSIN","SMC","TP","METRE","HYGIENE","PC"],
    "2nde F4": ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","DESSIN","INFORMATIQUE","TM/TC","TP","MECANIQUE","PREVENTION","LEGIS"],
    "Tle F4":  ["FRANÇAIS","ANGLAIS","MATH","PCT","RDM","PE","DESSIN","METRE","PC","BA","TP","LEGIS"],
    "2nde IMI": ["FRANÇAIS","ANGLAIS","MATH","EB","LA","AS","SEV","SER","ALGO","MATH APPLIQUE","LEGIS"],
    "Tle IMI":  ["FRANÇAIS","ANGLAIS","MATH","EB","RESEAU","RP","MATH APPLIQUÉ","LEGIS","BD","PG","ELEC"],
    "Tle F3":   ["FRANÇAIS","ANGLAIS","MATH","PHYSIQUE","ELECTRO","EST","PRATIQUE","MEL","DESSIN","ANGLAIS"],
    "2nde FC":  ["FRANÇAIS","ANGLAIS","MATH","EPS","PHYSIQUE","HIST-GÉO","PHYSIQUE APPLIQUE","AUTOMATISME","DESSIN","ELECTRO DE BASE"],
    "1ère HR":  ["FRANÇAIS","ANGLAIS","MATH","TC","SAAH","ECONOMAT","TRB","DROIT","MERCATIQUE","COMPTABILITE"],
    "2nde F3":  ["FRANÇAIS","ANGLAIS","MATH","PCT","TECHNO","SCHÉMA","DESSIN","ELECTRO","PRATIQUE","MEL"]
}

class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = ('matiere', 'semestre', 'inter1', 'inter2', 'inter3', 'inter4', 'devoir1', 'devoir2', 'appreciation')
    autocomplete_fields = ['matiere']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('matiere', 'semestre')

@admin.register(Eleves)
class ElevesAdmin(admin.ModelAdmin):
    list_display = ('code_eleve', 'prenom', 'nom', 'classe', 'voir_bulletin')
    search_fields = ('code_eleve', 'prenom', 'nom')
    list_filter = ('classe',)
    inlines = [NoteInline]

    def voir_bulletin(self, obj):
        url = reverse('eleves:bulletin', args=[obj.code_eleve])
        return format_html(f'<a href="{url}" target="_blank" class="btn btn-success btn-sm">Voir le bulletin</a>')
    voir_bulletin.short_description = "Bulletin"

    # LA MAGIE : affiche TOUTES les matières de la classe même si pas de note
    def changelist_view(self, request, extra_context=None):
        # On crée automatiquement les matières manquantes pour chaque élève
        from django.db.models import Q
        for eleve in Eleves.objects.all():
            classe_nom = str(eleve.classe)
            if classe_nom in MATIERES_PAR_CLASSE:
                matieres_classe = MATIERES_PAR_CLASSE[classe_nom]
                for nom_matiere in matieres_classe:
                    matiere, _ = Matiere.objects.get_or_create(nom=nom_matiere)
                    # On crée la note si elle n'existe pas (pour S1 par défaut)
                    Note.objects.get_or_create(
                        eleve=eleve,
                        matiere=matiere,
                        semestre=Semestre.objects.get_or_create(nom="S1")[0],
                        defaults={'appreciation': ''}
                    )
        return super().changelist_view(request, extra_context)

    class Media:
        css = {'all': ('css/admin_bulletin.css',)}  # si tu veux garder le style