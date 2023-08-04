from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime
import pytz

from . import models


# Create your tests here.
class MyUserTest(TestCase):

    def setUp(self):
        models.User.objects.create(
            email='co@test.test',
            role=models.User.COMMERCIAL,
            first_name="co",
            last_name='test',
            password='Azerty01'
            )
        user = models.User.objects.create(
            email='ge@test.test',
            role=models.User.GESTION,
            first_name="ge",
            last_name='test',
            password='Azerty01'
            )
        models.User.objects.create(
            email='su@test.test',
            role=models.User.SUPPORT,
            first_name="su",
            last_name='test',
            password='Azerty01'
            )
        models.User.objects.create(
            email='testmodife@test.test',
            role=models.User.SUPPORT,
            first_name="test",
            last_name='test',
            password='Azerty01'
            )
        models.User.objects.create(
            email='testdelete@test.test',
            role=models.User.SUPPORT,
            first_name="test",
            last_name='test',
            password='Azerty01'
            )

        # Mise en place de la connexion dans la requete
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        # Créez une instance du client de test APIClient
        self.client = APIClient()

    def testGet(self):
        response = self.client.get('/api/users/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        keysOK = ['id', 'email', 'first_name', 'last_name', 'role']
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)

    def testPost(self):
        data = {
            'email': 'test@test.test',
            'role': models.User.SUPPORT,
            'first_name': "test",
            'last_name': 'test',
            'password': 'Azerty01'
        }
        response = self.client.post('/api/users/', data, **self.headers)
        self.assertEqual(response.status_code, 201)
        keysOK = ['id', 'email', 'first_name', 'last_name', 'role']
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)

    def testPut(self):
        data = {
            'first_name': "testchange",
            'last_name': 'testchange',
        }
        response = self.client.put('/api/users/4/', data, **self.headers)
        self.assertEqual(response.status_code, 200)
        keysOK = ['id', 'email', 'first_name', 'last_name', 'role']
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)
        self.assertEqual(response.data['first_name'], 'testchange')
        self.assertEqual(response.data['last_name'], 'testchange')

    def testDelete(self):
        response = self.client.delete('/api/users/5/', **self.headers)
        self.assertEqual(response.status_code, 204)


class MyClientTest(TestCase):

    def setUp(self):
        user = models.User.objects.create(
            email='co@test.test',
            role=models.User.COMMERCIAL,
            first_name="co",
            last_name='test',
            password='Azerty01'
            )
        models.User.objects.create(
            email='ge@test.test',
            role=models.User.GESTION,
            first_name="ge",
            last_name='test',
            password='Azerty01'
            )
        models.User.objects.create(
            email='su@test.test',
            role=models.User.SUPPORT,
            first_name="su",
            last_name='test',
            password='Azerty01'
            )

        models.Client.objects.create(
            email='clientget@test.test',
            tel='+33634890810',
            first_name="testclient",
            last_name='testclient',
            entreprise='entrepriseCLIENT',
            commercial_contact=user
            )
        models.Client.objects.create(
            email='clientmodife@test.test',
            tel='+33634890810',
            first_name="testclient",
            last_name='testclient',
            entreprise='entrepriseCLIENT',
            commercial_contact=user
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        # Créez une instance du client de test APIClient
        self.client = APIClient()

    def testGet(self):
        response = self.client.get('/api/clients/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        keysOK = [
            'id',
            'first_name',
            'last_name',
            'email',
            'tel',
            'entreprise',
            'time_created',
            'time_update',
            'commercial_contact'
            ]
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)

    def testPost(self):
        data = {
            'email': 'client@test.test',
            'tel': '+33634890810',
            'first_name': "testclient",
            'last_name': 'testclient',
            'entreprise': 'entrepriseCLIENT'
        }
        response = self.client.post('/api/clients/', data, **self.headers)
        self.assertEqual(response.status_code, 201)
        keysOK = [
            'id',
            'first_name',
            'last_name',
            'email',
            'tel',
            'entreprise',
            'time_created',
            'time_update',
            'commercial_contact'
            ]
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)

    def testPut(self):
        data = {
            'first_name': "testclientchange",
            'last_name': 'testclientchange',
        }
        response = self.client.put('/api/clients/2/', data, **self.headers)
        self.assertEqual(response.status_code, 200)
        keysOK = [
            'id',
            'first_name',
            'last_name',
            'email',
            'tel',
            'entreprise',
            'time_created',
            'time_update',
            'commercial_contact'
            ]
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)
        self.assertEqual(response.data['first_name'], 'testclientchange')
        self.assertEqual(response.data['last_name'], 'testclientchange')


class MyContratTest(TestCase):

    def setUp(self):
        userCo = models.User.objects.create(
            email='co@test.test',
            role=models.User.COMMERCIAL,
            first_name="co",
            last_name='test',
            password='Azerty01'
            )
        userGe = models.User.objects.create(
            email='ge@test.test',
            role=models.User.GESTION,
            first_name="ge",
            last_name='test',
            password='Azerty01'
            )
        models.User.objects.create(
            email='su@test.test',
            role=models.User.SUPPORT,
            first_name="su",
            last_name='test',
            password='Azerty01'
            )

        client = models.Client.objects.create(
            email='client@test.test',
            tel='+33634890810',
            first_name="testclient",
            last_name='testclient',
            entreprise='entrepriseCLIENT',
            commercial_contact=userCo
            )

        models.Contrat.objects.create(
            client=client,
            commercial_contact=userCo,
            prix_ttl=532.34,
            prix_restant=334.63,
            statut=0
            )
        models.Contrat.objects.create(
            client=client,
            commercial_contact=userCo,
            prix_ttl=592.34,
            prix_restant=334.63,
            statut=0
            )

        refresh = RefreshToken.for_user(userGe)
        access_token = str(refresh.access_token)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        # Créez une instance du client de test APIClient
        self.client = APIClient()

    def testGet(self):
        response = self.client.get('/api/contrats/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        keysOK = ['id', 'client', 'prix_ttl', 'prix_restant', 'statut',  'time_created', 'commercial_contact']
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)

    def testPost(self):
        data = {
            'prix_ttl': 179.28,
            'prix_restant': 250,
            'statut': 0,
            'first_name': 'testclient',
            'last_name': 'testclient',
            'entreprise': 'entrepriseCLIENT'
        }
        response = self.client.post('/api/contrats/', data, **self.headers)
        self.assertEqual(response.status_code, 201)
        keysOK = ['id', 'client', 'prix_ttl', 'prix_restant', 'statut',  'time_created', 'commercial_contact']
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)

    def testPut(self):
        data = {
            'prix_restant': 0,
            'statut': 1,
        }
        response = self.client.put('/api/contrats/2/', data, **self.headers)
        self.assertEqual(response.status_code, 200)
        keysOK = ['id', 'client', 'prix_ttl', 'prix_restant', 'statut',  'time_created', 'commercial_contact']
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)
        self.assertEqual(response.data['prix_restant'], 0)
        self.assertEqual(response.data['statut'], 'signé')


class MyEvenementTest(TestCase):

    def setUp(self):
        userCo = models.User.objects.create(
            email='co@test.test',
            role=models.User.COMMERCIAL,
            first_name="co",
            last_name='test',
            password='Azerty01'
            )
        userGe = models.User.objects.create(
            email='ge@test.test',
            role=models.User.GESTION,
            first_name="ge",
            last_name='test',
            password='Azerty01'
            )
        userSu = models.User.objects.create(
            email='su@test.test',
            role=models.User.SUPPORT,
            first_name="su",
            last_name='test',
            password='Azerty01'
            )

        client = models.Client.objects.create(
            email='client@test.test',
            tel='+33634890810',
            first_name="testclient",
            last_name='testclient',
            entreprise='entrepriseCLIENT',
            commercial_contact=userCo
            )

        contrat = models.Contrat.objects.create(
            client=client,
            commercial_contact=userCo,
            prix_ttl=532.34,
            prix_restant=334.63,
            statut=1
            )

        user_timezone = pytz.timezone('Europe/Paris')

        models.Evenement.objects.create(
            nom='test',
            contrat=contrat,
            client=client,
            date_start=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            date_end=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            support_contact=userSu,
            location="ici",
            attende=1000,
            note="rien"
            )
        models.Evenement.objects.create(
            nom='testmodife',
            contrat=contrat,
            client=client,
            date_start=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            date_end=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            location="ici",
            attende=1000,
            note="rien"
            )

        refresh = RefreshToken.for_user(userGe)
        access_token = str(refresh.access_token)
        self.headersGe = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        refresh = RefreshToken.for_user(userSu)
        access_token = str(refresh.access_token)
        self.headersSu = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        refresh = RefreshToken.for_user(userCo)
        access_token = str(refresh.access_token)
        self.headersCo = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        # Créez une instance du client de test APIClient
        self.client = APIClient()

    def testGet(self):
        response = self.client.get('/api/evenements/', **self.headersGe)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        keysOK = [
            'id',
            'nom',
            'contrat',
            'client',
            'date_start',
            'date_end',
            'support_contact',
            'location',
            'attende',
            'note'
            ]
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)

    def testPost(self):
        user_timezone = pytz.timezone('Europe/Paris')
        data = {
            'nom': 'testEvenement',
            'date_start': datetime.strptime("1/9/209323:30", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            'date_end': datetime.strptime("20/9/209323:30", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            'location': 'la',
            'attende': 120001,
            'note': 'ehehehe',
            'client_id': 1,
            'contrat_id': 1
        }
        response = self.client.post('/api/evenements/', data, **self.headersCo)
        self.assertEqual(response.status_code, 201)
        keysOK = [
            'id',
            'nom',
            'contrat',
            'client',
            'date_start',
            'date_end',
            'support_contact',
            'location',
            'attende',
            'note'
            ]
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)

    def testPut(self):
        data = {
            'support_email': 'su@test.test',
        }
        response = self.client.put('/api/evenements/2/', data, **self.headersGe)
        self.assertEqual(response.status_code, 200)
        keysOK = [
            'id',
            'nom',
            'contrat',
            'client',
            'date_start',
            'date_end',
            'support_contact',
            'location',
            'attende',
            'note'
            ]
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)
        data = {
            'note': 'AHAHAHAHAHAHAHAHA',
        }
        response = self.client.put('/api/evenements/2/', data, **self.headersSu)
        self.assertEqual(response.status_code, 200)
        keysOK = [
            'id',
            'nom',
            'contrat',
            'client',
            'date_start',
            'date_end',
            'support_contact',
            'location',
            'attende',
            'note'
            ]
        keysOK = sorted(keysOK)
        listKey = response.data.keys()
        self.assertEqual(sorted(listKey), keysOK)
        self.assertEqual(response.data['note'], 'AHAHAHAHAHAHAHAHA')


class MyAllTest(TestCase):

    def setUp(self):
        userCo = models.User.objects.create(
            email='co@test.test',
            role=models.User.COMMERCIAL,
            first_name="co",
            last_name='test',
            password='Azerty01'
            )
        userGe = models.User.objects.create(
            email='ge@test.test',
            role=models.User.GESTION,
            first_name="ge",
            last_name='test',
            password='Azerty01'
            )
        userSu = models.User.objects.create(
            email='su@test.test',
            role=models.User.SUPPORT,
            first_name="su",
            last_name='test',
            password='Azerty01'
            )

        client = models.Client.objects.create(
            email='clientget@test.test',
            tel='+33634890810',
            first_name="testclient",
            last_name='testclient',
            entreprise='entrepriseCLIENT',
            commercial_contact=userCo
            )
        models.Client.objects.create(
            email='clientmodife@test.test',
            tel='+33634890810',
            first_name="testclient",
            last_name='testclient',
            entreprise='entrepriseCLIENT',
            commercial_contact=userCo
            )

        contrat = models.Contrat.objects.create(
            client=client,
            commercial_contact=userCo,
            prix_ttl=532.34,
            prix_restant=334.63,
            statut=0
            )
        models.Contrat.objects.create(
            client=client,
            commercial_contact=userCo,
            prix_ttl=592.34,
            prix_restant=334.63,
            statut=0
            )

        user_timezone = pytz.timezone('Europe/Paris')

        models.Evenement.objects.create(
            nom='test',
            contrat=contrat,
            client=client,
            date_start=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            date_end=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            support_contact=userSu,
            location="ici",
            attende=1000,
            note="rien"
            )
        models.Evenement.objects.create(
            nom='testmodife',
            contrat=contrat,
            client=client,
            date_start=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            date_end=datetime.strptime("1/2/202610:00", "%d/%m/%Y%H:%M").replace(tzinfo=user_timezone),
            location="ici",
            attende=1000,
            note="rien"
            )

        refresh = RefreshToken.for_user(userGe)
        access_token = str(refresh.access_token)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        self.client = APIClient()

    def testClient(self):
        response = self.client.get('/api/clients/all/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        keysOK = [
            'id',
            'first_name',
            'last_name',
            'email',
            'tel',
            'entreprise',
            'time_created',
            'time_update',
            'commercial_contact'
            ]
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)

    def testContrat(self):
        response = self.client.get('/api/contrats/all/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        keysOK = ['id', 'client', 'prix_ttl', 'prix_restant', 'statut',  'time_created', 'commercial_contact']
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)

    def testEvenement(self):
        response = self.client.get('/api/evenements/all/', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        keysOK = [
            'id',
            'nom',
            'contrat',
            'client',
            'date_start',
            'date_end',
            'support_contact',
            'location',
            'attende',
            'note'
            ]
        keysOK = sorted(keysOK)
        for user in response.data:
            listKey = user.keys()
            self.assertEqual(sorted(listKey), keysOK)
