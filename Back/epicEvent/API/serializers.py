from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from . import models


class UserSerializer(ModelSerializer):

    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class ClientSerializer(ModelSerializer):

    commercial_contact = UserSerializer()

    class Meta:
        model = models.Client
        fields = '__all__'


class ClientWithoutCommercialSerializer(ModelSerializer):

    class Meta:
        model = models.Client
        fields = ['id', 'email', 'first_name', 'last_name', 'tel', 'entreprise']


class ContratSerializer(ModelSerializer):

    client = ClientWithoutCommercialSerializer()
    commercial_contact = UserSerializer()
    statut = serializers.SerializerMethodField()

    class Meta:
        model = models.Contrat
        fields = '__all__'

    def get_statut(self, obj):
        return 'signé' if obj.statut else 'non signé'


class ContratWithoutClientSerializer(ModelSerializer):

    commercial_contact = UserSerializer()
    statut = serializers.SerializerMethodField()

    def get_statut(self, obj):
        return 'signé' if obj.statut else 'non signé'

    class Meta:
        model = models.Contrat
        fields = ['id', 'prix_ttl', 'prix_restant', 'time_created', 'statut', 'commercial_contact']


class EvenementSerializer(ModelSerializer):

    contrat = ContratWithoutClientSerializer()
    client = ClientSerializer()
    support_contact = UserSerializer()

    class Meta:
        model = models.Evenement
        fields = '__all__'
