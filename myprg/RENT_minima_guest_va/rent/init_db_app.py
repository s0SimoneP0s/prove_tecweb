from django.db import models
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone



from datetime import timedelta
from django.utils import timezone
from gestione.models import *
import random, os
from django.contrib.auth.models import Group

fake = Faker()


def crea_zone():
    # Crea le regioni
    tipi=["Stato","Regione","Provincia","Comune","Indirizzo"]
    print("Crea zone")
    zone_list=[]
    # crea nuove zone
    for _,ty in enumerate(tipi):
        if ty in ["Stato" , "Provincia" , "Regione"]:
            n=3
        elif ty=="Comune":
            n=10
        else : # indirizzo
            n=100
        for _ in range(n):  # Crea 3 regioni
            if ty in ["Stato" , "Provincia" , "Regione"]:
                nome=fake.country(),
            elif ty=="Comune":
                nome=fake.city()
            else : # indirizzo
                nome=fake.street_address()
            zona = Zona.objects.create(
                nome=nome,
                latitudine=random.uniform(-90, 90),
                longitudine=random.uniform(-180, 180),
                tipo=ty
            )
            zone_list.append(zona)
    print("Imposta struttura soprazone-sottozone")
    # logica soprazone
    for _,zona in enumerate(zone_list):
        tipo_zona = zona.tipo
        j=tipi.index(tipo_zona) # recupera l'indice 
        if tipo_zona == "Stato":
            soprazone_disponibili = [z for z in zone_list if z.nome != zona.nome ]  # filtra gli altri stati
        else:
            soprazone_disponibili = [z for z in zone_list if z.tipo == tipi[j-1]]  # soprazone possibili
        soprazona = random.choice(soprazone_disponibili) if soprazone_disponibili else None
        zona.soprazona = soprazona
        zona.save()

    print("Stati confinanti")
    lista_stati=[z for z in zone_list if z.tipo == "Stato" ]
    lista_stati[0].aggiungi_confinanti(lista_stati[1])
    lista_stati[1].aggiungi_confinanti(lista_stati[2])

    print("Liste confinanti")
    lista_regioni=[z for z in zone_list if z.tipo == "Regione" ]
    lista_provincie=[z for z in zone_list if z.tipo == "Provincia" ]
    lista_comuni=[z for z in zone_list if z.tipo == "Comune" ]
    lista_indirizzi=[z for z in zone_list if z.tipo == "Indirizzo" ]
    matrice=[lista_regioni,lista_provincie,lista_comuni,lista_indirizzi]
    # logica confinanti non stati
    scz1=[]
    scz2=[]
    for i,zona1 in enumerate(matrice):
        for j,zona2 in enumerate(zona1):
            if i<j:
                scz1=zona1[i].soprazona.confinanti.all()
            else:
                scz1=[]
            scz2=zona2.soprazona.confinanti.all()
        union=list(set(scz1) & set(scz2))
        for j,zona2 in enumerate(zona1):
            if union: # se la  lista non è vuota allora le 2 zone possono confinare
                if len(scz2)<5: # tiene basso il numero dei confinanti
                    zona2.aggiungi_confinanti(zona1[i])
                    zona2.save()

def random_date():
    tz = timezone.now()
    return tz - timedelta(days=random.randint(1, 365))

def random_datetime_in_past():
    now = timezone.now()
    delta_days = random.randint(1, 5)
    return now - timedelta(days=delta_days)

def indirizzo_casuale():
    tutte_zone = Zona.objects.filter(tipo='Indirizzo')
    return random.choice(tutte_zone)

def crea_gruppo(nome):
    group, created = Group.objects.get_or_create(name=nome)
    if created:
        print(f"Gruppo '{nome}' creato con successo.")
    else:
        print(f"Il gruppo '{nome}' esiste già nel database.")

def crea_gruppi():
    # Codice per creare il gruppo se non esiste
    gl=['Iscritti','Clienti','Proprietari']
    for i in gl:
        crea_gruppo(i)

def utente_di_prova(n=0):
    password="123utente123"
    return f"utentecasuale{n}" , password

def crea_utente_iscritto(user_tag=None):
    u,p = utente_di_prova(user_tag)
    username = fake.user_name() if user_tag==None else u
    email = fake.email()
    password = fake.password() if user_tag==None else p
    user = User.objects.create_user(username=username, email=email, password=password)
    g = Group.objects.get(name="Iscritti") #cerco il gruppo che mi interessa
    g.user_set.add(user) #aggiungo l'utente al gruppo, tutti sono Iscritti
    if user_tag in ["02","03"]:
        g = Group.objects.get(name="Clienti") #cerco il gruppo che mi interessa
        g.user_set.add(user)
    if user_tag in ["03"]:
        g = Group.objects.get(name="Proprietari") #cerco il gruppo che mi interessa
        g.user_set.add(user)
    return user

def crea_cliente(user_tag=None):
    user = crea_utente_iscritto(user_tag)
    prop = Cliente.objects.create(
        user=user,
        indirizzo=indirizzo_casuale(),
    )
    return  prop

def crea_proprietario(user_tag=None):
    user = crea_utente_iscritto(user_tag)
    prop = Proprietario.objects.create(
        user=user,
        indirizzo=indirizzo_casuale(),
        numero_telefono=fake.phone_number()
    )
    return  prop

def crea_proprietari_immobili_e_clienti():
    # Crea utenti proprietari
    for _ in range(5):
        crea_proprietario()
        crea_cliente()

def sei_confermato(k):
    """Se è il primo immobile l'admin conferma, quindi è random"""
    if k ==1:
        return random.choice([True,True,True, False])
    else:
        return True

immobili = [
    {"nome": "Casa Bella", "prezzo": 1200, "zona": "Centro"},
    {"nome": "Appartamento Mare", "prezzo": 1500, "zona": "Mare"},
    {"nome": "Villetta con Giardino", "prezzo": 1800, "zona": "Periferia"},
    {"nome": "Attico Panoramico", "prezzo": 2000, "zona": "Centro"},
    {"nome": "Chalet Montagna", "prezzo": 2500, "zona": "Montagna"}
]



def crea_immobili():
    proprietari = Proprietario.objects.all()
    for proprietario in proprietari:
        r_inter=random.randint(1, 3)
        for _ in range(r_inter):
            r = random.randint(0, len(immobili) - 1)
            immobile_data = immobili[r]

            Immobile.objects.create(
                proprietario=proprietario,
                nome=immobile_data["nome"],
                prezzo=random.uniform(15, 300),
                indirizzo=indirizzo_casuale(),
                data_creazione=random_datetime_in_past(),
                confermato_da_admin=sei_confermato(r_inter)
            )


def crea_prenotazioni():
    # Crea prenotazioni per gli immobili
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(0, 3)):
            if immobile.confermato_da_admin:
                durata_prenotazione = random.randint(15, 30)
                Prenotazione.objects.create(
                    utente=crea_utente_iscritto(),
                    immobile=immobile,
                    data_prenotazione=timezone.now() + timedelta(days=random.randint(1, 30)),
                    durata=durata_prenotazione
                )


def crea_recensioni():
    # Crea recensioni per gli immobili
    #immobili = Immobile.objects.filter(proprietario=proprietario)
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(0, 3)):
            if immobile.confermato_da_admin:
                Recensione.objects.create(
                    utente=crea_utente_iscritto(),
                    immobile=immobile,
                    testo=fake.text(),
                    stelline=random.randint(0, 5)
                )






def init_db_sql():
    # crea 2 utenti conosciuti
    crea_zone()
    crea_gruppi()
    crea_utente_iscritto("01") 
    crea_cliente("02")
    crea_proprietario("03") 
    crea_proprietari_immobili_e_clienti() # casuali
    crea_immobili()
    crea_prenotazioni()
    crea_recensioni()
    print("Fine creazione database\n")
