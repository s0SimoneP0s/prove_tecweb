from django.test import TestCase
from faker import Faker
import random
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from .models import Proprietario, Immobile, Prenotazione, Zona,Recensione
from django.contrib.auth.models import User



#######################################################################
#--------------------------- Models Dati -----------------------------#
#######################################################################


class DataCreation:
    fake = Faker()
    def random_datetime_in_past(self):
        now = timezone.now()
        delta_days = random.randint(1, 5)
        return now - timedelta(days=delta_days)
    
    def crea_utente(self , name=None):
        return User.objects.create_user(
            username=self.fake.user_name() if name ==None else name, 
            email=self.fake.email(), 
            password=self.fake.password()
        )
    def crea_proprietario(self, name=None):
        return  Proprietario.objects.create (
            user=self.crea_utente(name),
            indirizzo=self.fake.address(),
            numero_telefono=self.fake.phone_number()
        )
    def crea_immobile(self, name=None):
        return Immobile.objects.create(
                    proprietario=self.crea_proprietario(name),
                    nome="Casa di Test",
                    prezzo=random.uniform(10000, 500000),
                    zona=self.fake.city(),
                    data_creazione=self.random_datetime_in_past(),
                    confermato_da_admin=True
                )
    def crea_prenotazione(self, cliente=None,proprietario=None):
        return  Prenotazione.objects.create(
                utente=self.crea_utente(cliente),
                immobile=self.crea_immobile(proprietario),
                data_prenotazione=timezone.now() - timedelta(days=300), # passato non attiva
                durata=random.randint(15, 30)
            )

#######################################################################
#--------------------------- Models Test -----------------------------#
#######################################################################


class ProprietarioModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_proprietario()

    def test_proprietario_str(self):
        proprietario = self.dt.crea_proprietario()
        expected_str = f"{proprietario.user.username} - {proprietario.indirizzo.nome} - {proprietario.numero_telefono}"
        self.assertEqual(str(proprietario), expected_str)

class ImmobileModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_immobile()

    def test_disponibile_method(self):
        immobile = self.dt.crea_immobile()
        self.assertTrue(immobile.disponibile())

    def test_immobile_str(self):
        immobile = self.dt.crea_immobile()
        expected_str = f"{immobile.nome} di {immobile.zona} costo giornaliero € {immobile.prezzo}"
        self.assertEqual(str(immobile), expected_str)


class PrenotazioneModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_prenotazione()

    def test_attiva_method(self):
        prenotazione = self.dt.crea_prenotazione()
        self.assertFalse(prenotazione.attiva())  # Non affittato inizialmente
        near_past = timezone.now() - timedelta(days=1)
        prenotazione.data_prenotazione = near_past
        prenotazione.save()
        self.assertTrue(prenotazione.attiva())  # Ora affittato


    def test_prenotazione_str(self):
        prenotazione = self.dt.crea_prenotazione()
        expected_str = f"Prenotazione di {prenotazione.immobile.nome} di {prenotazione.immobile.zona} affittato dal {str(prenotazione.data_prenotazione)} per {prenotazione.durata} giorni"
        self.assertEqual(str(prenotazione), expected_str)

class ZonaTestCase(TestCase):
    def setUp(self):
        # Creazione di istanze di zona per i test
        self.zona1 = Zona.objects.create(nome="Zona 1", latitudine=45.0, longitudine=9.0, tipo="Stato")
        self.zona2 = Zona.objects.create(nome="Zona 2", latitudine=46.0, longitudine=10.0, tipo="Regione")
        self.zona3 = Zona.objects.create(nome="Zona 3", latitudine=44.0, longitudine=9.5, tipo="Regione")

    def test_str_method(self):
        self.assertEqual(str(self.zona1), "Zona 1")
        self.assertEqual(str(self.zona2), "Zona 2")
    
    def test_aggiungi_soprazona_method(self):
        self.zona2.aggiungi_soprazona(self.zona1)
        self.assertEqual(self.zona2.soprazona.nome, "Zona 1")
        self.assertEqual(self.zona2.soprazona.tipo, "Stato")
        self.assertEqual(self.zona2.soprazona.pk, 1)  
    
    def test_aggiungi_confinanti_method(self):
        self.zona3.aggiungi_confinanti(self.zona2)
        self.assertIn(self.zona3, self.zona2.confinanti.all())  

  
    def test_calcola_distanza_method(self):
        # Creazione di un'altra zona per il test della distanza
        zona3 = Zona.objects.create(nome="Zona 3", latitudine=47.0, longitudine=11.0, tipo="Comune")
        distanza_km = self.zona1.calcola_distanza(zona3)
        self.assertAlmostEqual(distanza_km, 270.76, places=1)  # Verifica approssimativa della distanza

        # Verifica che la distanza tra una zona e se stessa sia 0
        distanza_self = self.zona1.calcola_distanza(self.zona1)
        self.assertEqual(distanza_self, 0.0)

        # Verifica che la distanza tra due zone uguali sia 0
        distanza_uguale = self.zona1.calcola_distanza(self.zona1)
        self.assertEqual(distanza_uguale, 0.0)




"""
class RecensioneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        proprietario = Proprietario.objects.create(user=user)
        immobile = Immobile.objects.create(proprietario=proprietario, nome='Casa di Test', zona='Centro')
        Recensione.objects.create(utente=user, immobile=immobile, testo='Recensione di prova', stelline=4)

    def test_recensione_str(self):
        recensione = Recensione.objects.get(id=1)
        expected_str = f"Recensione di {recensione.immobile} di {recensione.utente}"
        self.assertEqual(str(recensione), expected_str)
"""