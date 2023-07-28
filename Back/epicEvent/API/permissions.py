from rest_framework.permissions import BasePermission

from . import models
 
class IsGestionTeam(BasePermission):

    def has_permission(self, request, view):
        return bool(isThis(request.user.id, models.User.GESTION) and request.user.is_authenticated)
    
class IsCommercialTeam(BasePermission):

    def has_permission(self, request, view):
        return bool(isThis(request.user.id, models.User.COMMERCIAL) and request.user.is_authenticated)
    
class ContratsPermission(BasePermission):

    def has_permission(self, request, view):
        # Vérifie si la méthode de requête est en lecture seule (GET, PUT, HEAD, OPTIONS)
        if request.method in ['GET', 'PUT', 'HEAD', 'OPTIONS']:
            return bool(bool(isThis(request.user.id, models.User.GESTION) | isThis(request.user.id, models.User.COMMERCIAL)) and request.user.is_authenticated)
        
        return bool(isThis(request.user.id, models.User.GESTION) and request.user.is_authenticated)
    
class EvenementsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'HEAD', 'OPTIONS']:
            return bool(bool(isThis(request.user.id, models.User.GESTION) | isThis(request.user.id, models.User.SUPPORT)) and request.user.is_authenticated)
        
        return bool(isThis(request.user.id, models.User.COMMERCIAL) and request.user.is_authenticated)


def isThis(userID, role):
    try:
        user = models.User.objects.get(id=userID)
    except models.User.DoesNotExist:
        return False
    return bool(user.role == role)