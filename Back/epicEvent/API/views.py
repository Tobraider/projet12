from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from datetime import datetime

from . import models
from . import permissions
from . import serializers

def choix_list(list, data, default=None):
    """ Cette fonction permet de regarde si la data est dans tout les choix pour le champ 
        si pas le cas retourne default """
    # default est la pour que la valeur ne change pas si deja setup avant
    pris = default
    for choice in list:
        if data == choice[0] or data == choice[1]:
            # le 0 est donnée car c'est la valeur que prendra le champ
            pris = choice[0]
    return pris

class UserViewset(APIView):

    permission_classes = [permissions.IsGestionTeam]

    def get(self, request):
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        newUser = models.User()
        newUser.email = request.POST.get("email")
        newUser.first_name = request.POST.get("first_name")
        newUser.last_name = request.POST.get("last_name")
        newUser.role = choix_list(models.User.role_choice, request.POST.get("role"))
        newUser.password = make_password(request.POST.get("password"))
        print(newUser)
        # Verifie si tout les champs sont OK
        try:
            newUser.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            newUser.save()
        except IntegrityError:
            return Response({'error': 'email deja utilisé'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserSerializer(newUser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UserDetailViewset(APIView):

    permission_classes = [permissions.IsGestionTeam]
    
    def put(self, request, idUser):
        try:
            user = models.User.objects.get(id=idUser)
        except models.User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.POST.get("email"):
            user.email = request.POST.get("email")
        if request.POST.get("first_name"):
            user.first_name = request.POST.get("first_name")
        if request.POST.get("last_name"):
            user.last_name = request.POST.get("last_name")
        if request.POST.get("role"):
            user.role = choix_list(models.User.role_choice, request.POST.get("role"),user.role)
        if request.POST.get("password"):
            user.password = make_password(request.POST.get("password"))
        # Verifie si tout les champs sont OK
        try:
            user.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            user.save()
        except IntegrityError:
            return Response({'error': 'email deja utilisé'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, idUser):
        try:
            user = models.User.objects.get(id=idUser)
        except models.User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class ClientViewset(APIView):

    permission_classes = [permissions.IsCommercialTeam]

    def get(self, request):
        clients = models.Client.objects.filter(commercial_contact__id=request.user.id)
        serializer = serializers.ClientSerializer(clients, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        newClient = models.Client()
        newClient.first_name = request.POST.get("first_name")
        newClient.last_name = request.POST.get("last_name")
        newClient.email = request.POST.get("email")
        newClient.tel = request.POST.get("tel")
        newClient.entreprise = request.POST.get("entreprise")
        newClient.commercial_contact = request.user
        # Verifie si tout les champs sont OK
        try:
            newClient.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            newClient.save()
        except IntegrityError:
            return Response({'error': 'Impossible de sauvegarder le client dans la bdd'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ClientSerializer(newClient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClientDetailView(APIView):

    permission_classes = [permissions.IsCommercialTeam]

    def put(self, request, idClient):
        try:
            client = models.Client.objects.get(id=idClient)
        except models.Client.DoesNotExist:
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.POST.get("first_name"):
            client.first_name = request.POST.get("first_name")
        if request.POST.get("last_name"):
            client.last_name = request.POST.get("last_name")
        if request.POST.get("email"):
            client.email = request.POST.get("email")
        if request.POST.get("tel"):
            client.tel = request.POST.get("tel")
        if request.POST.get("entreprise"):
            client.entreprise = request.POST.get("entreprise")
        client.time_update = datetime.now()
        # Verifie si tout les champs sont OK
        try:
            client.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            client.save()
        except IntegrityError:
            return Response({'error': 'Impossible de sauvegarder le client dans la bdd'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def delete(self, request, idClient):
    #     try:
    #         client = models.Client.objects.get(id=idClient)
    #     except models.Client.DoesNotExist:
    #         return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    #     client.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ClientAllViewset(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = models.Client.objects.all()
        serializer = serializers.ClientSerializer(clients, many=True)
        return Response(serializer.data)

class ContratViewset(APIView):

    permission_classes = [permissions.ContratsPermission]

    def get(self, request):
        if permissions.isThis(request.user.id, models.User.GESTION):
            contrats = models.Contrat.objects.all()
        else:
            contrats = models.Contrat.objects.filter(commercial_contact__id=request.user.id)
        serializer = serializers.ContratSerializer(contrats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        newContrat = models.Contrat()
        newContrat.prix_ttl = request.POST.get("prix_ttl")
        newContrat.prix_restant = request.POST.get("prix_restant")
        if int(request.POST.get("statut")) == 1:
            newContrat.statut = True
        else:
            newContrat.statut = False
        if request.POST.get("client_id"):
            try:
                client = models.Client.objects.get(id=int(request.POST.get("client_id")))
            except models.Client.DoesNotExist:
                return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                client = models.Client.objects.get(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    entreprise=request.POST.get("entreprise")
                    )
            except models.Client.DoesNotExist:
                return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        newContrat.client = client
        if client:
            newContrat.commercial_contact = client.commercial_contact
        # Verifie si tout les champs sont OK
        try:
            newContrat.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            newContrat.save()
        except IntegrityError:
            return Response({'error': 'Impossible de sauvegarder le contrat dans la bdd'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ContratSerializer(newContrat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContratDetailViewset(APIView):

    permission_classes = [permissions.ContratsPermission]

    def put(self, request, idContrat):
        if permissions.isThis(request.user.id, models.User.GESTION):
            try:
                contrat = models.Contrat.objects.get(id=idContrat)
            except:
                return Response({"message": "Contrat not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                contrat = models.Contrat.objects.get(id=idContrat, commercial_contact__id=request.user.id)
            except:
                return Response({"message": "Contrat not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.POST.get("prix_ttl"):
            contrat.prix_ttl = request.POST.get("prix_ttl")
        if request.POST.get("prix_restant"):
            contrat.prix_restant = request.POST.get("prix_restant")
        if request.POST.get("statut"):
            if int(request.POST.get("statut")) == 1:
                contrat.statut = True
            else:
                contrat.statut = False
        # Verifie si tout les champs sont OK
        try:
            contrat.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            contrat.save()
        except IntegrityError:
            return Response({'error': 'Impossible de sauvegarder le contrat dans la bdd'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ContratSerializer(contrat)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContratAllViewset(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = models.Contrat.objects.all()
        serializer = serializers.ContratSerializer(clients, many=True)
        return Response(serializer.data)
    

class EvenementViewset(APIView):

    permission_classes = [permissions.EvenementsPermission]

    def get(self, request):
        if permissions.isThis(request.user.id, models.User.GESTION):
            evenements = models.Evenement.objects.filter(support_contact__isnull=True)
        else:
            evenements = models.Evenement.objects.filter(support_contact__id=request.user.id)
        serializer = serializers.EvenementSerializer(evenements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.POST.get("client_id"):
            try:
                client = models.Client.objects.get(id=int(request.POST.get("client_id")),commercial_contact=request.user)
            except models.Client.DoesNotExist:
                return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                client = models.Client.objects.get(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    entreprise=request.POST.get("entreprise"),
                    commercial_contact=request.user
                    )
            except models.Client.DoesNotExist:
                return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        evenement = models.Evenement()
        evenement.client = client
        try:
            contrat = models.Contrat.objects.get(id=int(request.POST.get("contrat_id")),client=client, statut=True)
        except models.Client.DoesNotExist:
            return Response({"message": "Contrat not found"}, status=status.HTTP_404_NOT_FOUND)
        evenement.contrat = contrat
        evenement.nom = request.POST.get("nom")
        evenement.date_start = request.POST.get("date_start")
        evenement.date_end = request.POST.get("date_end")
        evenement.location = request.POST.get("location")
        evenement.attende = int(request.POST.get("attende"))
        evenement.note = request.POST.get("note")
        try:
            evenement.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            evenement.save()
        except IntegrityError:
            return Response({'error': "Impossible de sauvegarder l'evenement dans la bdd"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.EvenementSerializer(evenement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EvenementDetailViewset(APIView):

    permission_classes = [permissions.EvenementsPermission]

    def put(self, request, idEvenement):
        if permissions.isThis(request.user.id, models.User.GESTION):
            try:
                evenement = models.Evenement.objects.get(id=idEvenement)
            except:
                return Response({"message": "Evenement not found"}, status=status.HTTP_404_NOT_FOUND)
            if request.POST.get("support_email"):
                try:
                    support = models.User.objects.get(email=request.POST.get("support_email"))
                except models.User.DoesNotExist:
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                evenement.support_contact=support
        else:
            try:
                evenement = models.Evenement.objects.get(id=idEvenement,support_contact__id=request.user.id)
            except:
                return Response({"message": "Evenement not found"}, status=status.HTTP_404_NOT_FOUND)
            if request.POST.get("nom"):
                evenement.nom = request.POST.get("nom")
            if request.POST.get("date_start"):
                evenement.date_start = request.POST.get("date_start")
            if request.POST.get("date_end"):
                evenement.date_end = request.POST.get("date_end")
            if request.POST.get("location"):
                evenement.location = request.POST.get("location")
            if request.POST.get("attende"):
                evenement.attende = int(request.POST.get("attende"))
            if request.POST.get("note"):
                evenement.note = request.POST.get("note")
        try:
            evenement.full_clean()
        except ValidationError as e:
            print(e)
            return Response({'error': 'Erreur dans les informations rentrées'}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarde
        try:
            evenement.save()
        except IntegrityError:
            return Response({'error': "Impossible de sauvegarder l'evenement' dans la bdd"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.EvenementSerializer(evenement)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EvenementAllViewset(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = models.Evenement.objects.all()
        serializer = serializers.EvenementSerializer(clients, many=True)
        return Response(serializer.data)