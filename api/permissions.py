from rest_framework import permissions


class EstProprietaireOuReadOnly(permissions.BasePermission):
    """
    Règle : lecture libre, mais modification uniquement par le créateur.
    Le modèle doit avoir un champ 'cree_par' ForeignKey vers User.
    """
    message = 'Vous devez être le propriétaire pour modifier cet objet.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.cree_par == request.user or request.user.is_staff
