# API Bibliothèque - Django REST Framework

Ce projet est une API REST complète pour la gestion d'une bibliothèque, développée avec Django REST Framework selon le TP demandé.

## Fonctionnalités implémentées

### Modèles
- **Auteur** : nom, biographie, nationalité
- **Livre** : titre, ISBN, année de publication, catégorie, auteur (ForeignKey), tags (ManyToMany), disponible, créé par
- **Emprunt** : utilisateur, livre, date d'emprunt, date de retour prévue, rendu
- **Tag** : nom
- **ProfilLecteur** : utilisateur (OneToOne), adresse, téléphone, date de naissance, livres favoris

### Sérialiseurs
- Validation personnalisée (ISBN 13 chiffres, année entre 1000-2025)
- Sérialiseurs imbriqués pour les relations
- Champs calculés (auteur_nom)

### Vues (ViewSets)
- **AuteurViewSet** : CRUD complet + actions personnalisées (livres, stats)
- **LivreViewSet** : CRUD complet + actions personnalisées (disponibles, emprunter, rendre)
- **TagViewSet** : CRUD complet
- **EmpruntViewSet** : CRUD complet (filtré par utilisateur connecté)
- **Vues fonctionnelles** : profil_lecteur, ajouter_favori

### Authentification & Permissions
- JWT (JSON Web Token) avec SimpleJWT
- Permission personnalisée : EstProprietaireOuReadOnly
- Permissions par défaut : IsAuthenticatedOrReadOnly

### Pagination & Filtres
- Pagination personnalisée (page_size=10, paramètre size)
- Filtres avancés : catégorie, annee_min/max, titre, auteur_nom, disponible
- Recherche : titre, auteur__nom, isbn
- Tri : titre, annee_publication, date_creation

## Installation

1. **Créer l'environnement virtuel**
```bash
python -m venv env_bibliotheque
env_bibliotheque\Scripts\activate  # Windows
source env_bibliotheque/bin/activate  # Linux/Mac
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Appliquer les migrations**
```bash
python manage.py migrate
```

4. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

5. **Lancer le serveur**
```bash
python manage.py runserver
```

## Endpoints API

### Authentification
- `POST /api/auth/token/` - Obtenir un token JWT
- `POST /api/auth/token/refresh/` - Rafraîchir le token

### Auteurs
- `GET /api/auteurs/` - Liste des auteurs (paginée, filtrée)
- `POST /api/auteurs/` - Créer un auteur (auth requise)
- `GET /api/auteurs/{id}/` - Détail d'un auteur
- `PUT /api/auteurs/{id}/` - Modifier un auteur (propriétaire)
- `DELETE /api/auteurs/{id}/` - Supprimer un auteur (admin)
- `GET /api/auteurs/{id}/livres/` - Livres d'un auteur
- `GET /api/auteurs/stats/` - Statistiques globales

### Livres
- `GET /api/livres/` - Liste des livres (paginée, filtrée)
- `POST /api/livres/` - Créer un livre (auth requise)
- `GET /api/livres/{id}/` - Détail d'un livre
- `PATCH /api/livres/{id}/` - Modification partielle
- `DELETE /api/livres/{id}/` - Supprimer un livre
- `POST /api/livres/{id}/emprunter/` - Emprunter un livre
- `POST /api/livres/{id}/rendre/` - Rendre un livre
- `GET /api/livres/disponibles/` - Livres disponibles

### Tags
- `GET /api/tags/` - Liste des tags
- `POST /api/tags/` - Créer un tag (auth requise)
- `GET /api/tags/{id}/` - Détail d'un tag
- `PUT /api/tags/{id}/` - Modifier un tag
- `DELETE /api/tags/{id}/` - Supprimer un tag

### Emprunts
- `GET /api/emprunts/` - Mes emprunts (auth requise)
- `POST /api/emprunts/` - Créer un emprunt
- `GET /api/emprunts/{id}/` - Détail d'un emprunt

### Profil Lecteur
- `GET /api/profil/` - Mon profil (auth requise)
- `PUT /api/profil/` - Mettre à jour le profil
- `POST /api/profil/favoris/` - Ajouter un livre aux favoris

## Exemples d'utilisation

### Obtenir un token JWT
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "admin123"}'
```

### Créer un livre avec authentification
```bash
curl -X POST http://127.0.0.1:8000/api/livres/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{
    "titre": "Le Petit Prince",
    "isbn": "9782070612758",
    "annee_publication": 1943,
    "categorie": "roman",
    "auteur": 2
  }'
```

### Filtrer les livres
```bash
GET /api/livres/?categorie=roman&disponible=true
GET /api/livres/?search=hugo
GET /api/livres/?annee_min=1900&annee_max=1950
GET /api/livres/?ordering=-annee_publication
GET /api/livres/?page=1&size=5
```

## Structure du projet

```
bibliotheque_project/
├── manage.py
├── requirements.txt
├── README.md
├── bibliotheque_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── permissions.py
    ├── filters.py
    ├── pagination.py
    └── admin.py
```

## Technologies utilisées

- Django 5.2.12
- Django REST Framework
- django-filter
- djangorestframework-simplejwt
- SQLite (base de données)

## Compte de test

- **Username**: admin
- **Password**: admin123

## Interface d'administration

L'interface d'administration Django est disponible à :
http://127.0.0.1:8000/admin/

## Interface API browsable

L'interface browsable de DRF est disponible à :
http://127.0.0.1:8000/api/
