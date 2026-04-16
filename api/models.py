from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Représente un tag/catégorie pour les livres.
    """
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class Auteur(models.Model):
    """
    Représente un auteur de livres.
    Django crée automatiquement un champ 'id' (clé primaire).
    """
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom complet'
    )
    biographie = models.TextField(
        blank=True,
        null=True,
        verbose_name='Biographie'
    )
    nationalite = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Nationalité'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'


class Livre(models.Model):
    """
    Représente un livre. Chaque livre a UN auteur (ForeignKey = N vers 1).
    Un auteur peut avoir PLUSIEURS livres.
    """
    CATEGORIES = [
        ('roman', 'Roman'),
        ('essai', 'Essai'),
        ('poesie', 'Poésie'),
        ('bd', 'Bande dessinée'),
        ('science', 'Science'),
        ('histoire', 'Histoire'),
    ]

    titre = models.CharField(max_length=300, verbose_name='Titre')
    isbn = models.CharField(
        max_length=17,
        unique=True,
        verbose_name='ISBN'
    )
    annee_publication = models.IntegerField(
        verbose_name='Année de publication'
    )
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='roman',
        verbose_name='Catégorie'
    )
    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.CASCADE,
        related_name='livres',
        verbose_name='Auteur'
    )
    disponible = models.BooleanField(default=True)
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livres_crees',
        verbose_name='Créé par'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='livres'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titre} ({self.annee_publication})'

    class Meta:
        ordering = ['-annee_publication', 'titre']


class Emprunt(models.Model):
    """
    Représente un emprunt de livre par un utilisateur.
    """
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emprunts',
        verbose_name='Utilisateur'
    )
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name='emprunts',
        verbose_name='Livre'
    )
    date_emprunt = models.DateField(
        auto_now_add=True,
        verbose_name='Date d\'emprunt'
    )
    date_retour_prevue = models.DateField(
        verbose_name='Date de retour prévue'
    )
    rendu = models.BooleanField(
        default=False,
        verbose_name='Rendu'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.utilisateur.username} - {self.livre.titre}'

    class Meta:
        ordering = ['-date_emprunt']
        verbose_name = 'Emprunt'
        verbose_name_plural = 'Emprunts'


class ProfilLecteur(models.Model):
    """
    Profil lecteur avec OneToOneField vers User.
    """
    utilisateur = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil_lecteur',
        verbose_name='Utilisateur'
    )
    adresse = models.TextField(blank=True, verbose_name='Adresse')
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Téléphone'
    )
    date_naissance = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de naissance'
    )
    livres_favoris = models.ManyToManyField(
        Livre,
        blank=True,
        related_name='favoris_par',
        verbose_name='Livres favoris'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profil de {self.utilisateur.username}'

    class Meta:
        verbose_name = 'Profil lecteur'
        verbose_name_plural = 'Profils lecteurs'
