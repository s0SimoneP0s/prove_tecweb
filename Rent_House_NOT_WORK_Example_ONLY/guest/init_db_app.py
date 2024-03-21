from django.db import models
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone



from datetime import timedelta
from django.utils import timezone
from guest.models import *
import random, os


proprietari = ["Proprietario1", "Proprietario2", "Proprietario3", "Proprietario4", "Proprietario5"]
immobili = [
    {"nome": "Casa Bella", "prezzo": 1200, "zona": "Centro"},
    {"nome": "Appartamento Mare", "prezzo": 1500, "zona": "Mare"},
    {"nome": "Villetta con Giardino", "prezzo": 1800, "zona": "Periferia"},
    {"nome": "Attico Panoramico", "prezzo": 2000, "zona": "Centro"},
    {"nome": "Chalet Montagna", "prezzo": 2500, "zona": "Montagna"}
]


def random_date():
    tz = timezone.now()
    return tz - timedelta(days=random.randint(1, 365))

def erase_db():
    path_db="db.sqlite3"
    print (os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(path_db):
        print("Cancello il DB")
        os.remove(path_db)
        print(f'Successfully deleted {path_db}')
    else:
        print (f'{path_db} does not exist')

fake = Faker()

from datetime import timedelta

def random_datetime_in_past():
    now = timezone.now()
    delta_days = random.randint(1, 5)
    return now - timedelta(days=delta_days)



def crea_utente():
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    user = User.objects.create_user(username=username, email=email, password=password)
    return user

def crea_proprietario():
    user = crea_utente()
    prop = Proprietario.objects.create(
        user=user,
        indirizzo=fake.address(),
        numero_telefono=fake.phone_number()
    )
    return  prop

def crea_proprietari_immobili():
    # Crea utenti proprietari
    for _ in range(5):
        crea_proprietario()

def sei_confermato(k):
    """Se è il primo immobile l'admin conferma, quindi è random"""
    if k ==1:
        return random.choice([True, False])
    else:
        return True


def crea_immobili():
    # Crea immobili per ogni proprietario
    proprietari = Proprietario.objects.all()
    for proprietario in proprietari:
        r_inter=random.randint(1, 3)
        for _ in range(r_inter):
            r = random.randint(0, len(immobili) - 1)
            immobile_data = immobili[r]

            Immobile.objects.create(
                proprietario=proprietario,
                nome=immobile_data["nome"],
                prezzo=random.uniform(10000, 500000),
                zona=fake.city(),
                #data_creazione=fake.date_time_this_decade(),
                data_creazione=random_datetime_in_past(),
                confermato_da_admin=sei_confermato(r_inter)
            )




def crea_recensioni():
    # Crea recensioni per gli immobili
    #immobili = Immobile.objects.filter(proprietario=proprietario)
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(0, 3)):
            if immobile.confermato_da_admin:
                Recensione.objects.create(
                    utente=crea_utente(),
                    immobile=immobile,
                    testo=fake.text(),
                    stelline=random.randint(0, 5)
                )


def crea_prenotazioni():
    # Crea prenotazioni per gli immobili
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(0, 3)):
            if immobile.confermato_da_admin:
                Prenotazione.objects.create(
                    cliente=crea_utente(),
                    immobile=immobile,
                    data_prenotazione=timezone.now() + timedelta(days=random.randint(1, 30))
                )

def init_db_sql():
    #erase_db()
    crea_proprietari_immobili()
    crea_immobili()
    crea_recensioni()
    crea_prenotazioni()



# Chiamare la funzione per inizializzare il database con dati casuali
#init_db_sql()


from django.contrib.auth.models import Group


def group_create():
    # Creazione dei gruppi
    gruppo_utente, _ = Group.objects.get_or_create(name='Utente')
    gruppo_proprietario, _ = Group.objects.get_or_create(name='Proprietario')
    gruppo_admin, _ = Group.objects.get_or_create(name='Admin')