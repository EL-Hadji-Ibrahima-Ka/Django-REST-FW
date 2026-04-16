from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Auteur, Livre, Tag, Emprunt, ProfilLecteur
from .serializers import (
    AuteurSerializer, LivreSerializer, LivreDetailSerializer,
    TagSerializer, EmpruntSerializer, ProfilLecteurSerializer
)
from .permissions import EstProprietaireOuReadOnly
from .filters import LivreFilter, EmpruntFilter
from .pagination import StandardPagination


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='livres')
    def livres(self, request, pk=None):
        auteur = self.get_object()
        livres = auteur.livres.all()
        serializer = LivreSerializer(livres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        data = {
            'total_auteurs': Auteur.objects.count(),
            'total_livres': Livre.objects.count(),
            'nationalites': list(Auteur.objects.values_list('nationalite', flat=True).distinct()),
        }
        return Response(data)


class LivreViewSet(viewsets.ModelViewSet):
    queryset = (
        Livre.objects
        .select_related('auteur')
        .prefetch_related('tags')
        .all()
    )
    permission_classes = [EstProprietaireOuReadOnly]
    pagination_class = StandardPagination
    filterset_class = LivreFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['titre', 'auteur__nom', 'isbn']
    ordering_fields = ['titre', 'annee_publication', 'date_creation']
    ordering = ['-date_creation']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LivreDetailSerializer
        return LivreSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(cree_par=self.request.user)

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        qs = self.get_queryset().filter(disponible=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def emprunter(self, request, pk=None):
        livre = self.get_object()
        if not livre.disponible:
            return Response(
                {'erreur': 'Ce livre n\'est pas disponible.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        livre.disponible = False
        livre.save()
        return Response({'message': f'Livre "{livre.titre}" emprunté avec succès.'})

    @action(detail=True, methods=['post'])
    def rendre(self, request, pk=None):
        livre = self.get_object()
        livre.disponible = True
        livre.save()
        return Response({'message': f'Livre "{livre.titre}" rendu avec succès.'})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.all().select_related('utilisateur', 'livre')
    serializer_class = EmpruntSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = EmpruntFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['livre__titre', 'utilisateur__username']
    ordering = ['-date_emprunt']

    def get_queryset(self):
        return Emprunt.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def profil_lecteur(request):
    profil, created = ProfilLecteur.objects.get_or_create(
        utilisateur=request.user
    )
    
    if request.method == 'GET':
        serializer = ProfilLecteurSerializer(profil)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProfilLecteurSerializer(profil, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ajouter_favori(request):
    livre_id = request.data.get('livre_id')
    try:
        livre = Livre.objects.get(id=livre_id)
        profil, created = ProfilLecteur.objects.get_or_create(
            utilisateur=request.user
        )
        profil.livres_favoris.add(livre)
        return Response({'message': 'Livre ajouté aux favoris.'})
    except Livre.DoesNotExist:
        return Response(
            {'erreur': 'Livre non trouvé.'},
            status=status.HTTP_404_NOT_FOUND
        )
