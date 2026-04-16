from rest_framework import serializers
from .models import Auteur, Livre, Tag, Emprunt, ProfilLecteur
from django.contrib.auth.models import User


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = '__all__'
        read_only_fields = ['id', 'date_creation']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nom']


class LivreSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_nom', 'disponible', 'cree_par'
        ]
        read_only_fields = ['id', 'date_creation', 'cree_par']

    def get_auteur_nom(self, obj):
        return obj.auteur.nom

    def validate_isbn(self, value):
        clean = value.replace('-', '')
        if not clean.isdigit() or len(clean) != 13:
            raise serializers.ValidationError(
                "L'ISBN doit contenir exactement 13 chiffres."
            )
        return value

    def validate_annee_publication(self, value):
        if value < 1000 or value > 2025:
            raise serializers.ValidationError(
                "L'année doit être entre 1000 et 2025."
            )
        return value

    def validate(self, data):
        if data.get('categorie') == 'essai':
            auteur = data.get('auteur')
            if auteur and not auteur.biographie:
                raise serializers.ValidationError(
                    "Les essais requièrent une biographie de l'auteur."
                )
        return data


class LivreDetailSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True)
    auteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Auteur.objects.all(),
        source='auteur',
        write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_id', 'disponible',
            'cree_par', 'tags', 'tag_ids'
        ]
        read_only_fields = ['id', 'date_creation', 'cree_par']


class EmpruntSerializer(serializers.ModelSerializer):
    livre_titre = serializers.SerializerMethodField()
    utilisateur_username = serializers.SerializerMethodField()

    class Meta:
        model = Emprunt
        fields = [
            'id', 'utilisateur', 'livre', 'livre_titre',
            'utilisateur_username', 'date_emprunt', 'date_retour_prevue', 'rendu'
        ]
        read_only_fields = ['id', 'date_emprunt', 'date_creation']

    def get_livre_titre(self, obj):
        return obj.livre.titre

    def get_utilisateur_username(self, obj):
        return obj.utilisateur.username


class ProfilLecteurSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = ProfilLecteur
        fields = [
            'id', 'utilisateur', 'username', 'adresse', 'telephone',
            'date_naissance', 'livres_favoris'
        ]
        read_only_fields = ['id', 'date_creation']

    def get_username(self, obj):
        return obj.utilisateur.username


class AuteurAvecLivresSerializer(serializers.ModelSerializer):
    livres = LivreSerializer(many=True)

    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'nationalite', 'biographie', 'livres']

    def create(self, validated_data):
        livres_data = validated_data.pop('livres', [])
        auteur = Auteur.objects.create(**validated_data)
        for livre_data in livres_data:
            Livre.objects.create(auteur=auteur, **livre_data)
        return auteur

    def update(self, instance, validated_data):
        livres_data = validated_data.pop('livres', [])
        instance.nom = validated_data.get('nom', instance.nom)
        instance.nationalite = validated_data.get('nationalite', instance.nationalite)
        instance.biographie = validated_data.get('biographie', instance.biographie)
        instance.save()
        instance.livres.all().delete()
        for livre_data in livres_data:
            Livre.objects.create(auteur=instance, **livre_data)
        return instance
