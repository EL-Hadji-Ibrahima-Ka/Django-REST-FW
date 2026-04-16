from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AuteurViewSet, LivreViewSet, TagViewSet, EmpruntViewSet,
    profil_lecteur, ajouter_favori
)

router = DefaultRouter()
router.register(r'auteurs', AuteurViewSet, basename='auteur')
router.register(r'livres', LivreViewSet, basename='livre')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'emprunts', EmpruntViewSet, basename='emprunt')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profil/', profil_lecteur, name='profil_lecteur'),
    path('profil/favoris/', ajouter_favori, name='ajouter_favori'),
]
