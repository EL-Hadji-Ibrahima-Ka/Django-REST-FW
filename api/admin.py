from django.contrib import admin
from .models import Auteur, Livre, Emprunt, Tag, ProfilLecteur


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nationalite', 'date_creation']
    search_fields = ['nom', 'nationalite']


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'annee_publication', 'categorie', 'disponible']
    list_filter = ['categorie', 'disponible']
    search_fields = ['titre', 'isbn']


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'livre', 'date_emprunt', 'date_retour_prevue', 'rendu']
    list_filter = ['rendu', 'date_emprunt']
    search_fields = ['utilisateur__username', 'livre__titre']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(ProfilLecteur)
class ProfilLecteurAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'telephone', 'date_naissance']
    search_fields = ['utilisateur__username']
