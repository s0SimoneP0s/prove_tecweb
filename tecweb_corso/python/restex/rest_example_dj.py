import requests
import socket
import json

def check_response(response) -> bool:
   if response.status_code not in range(200,204+1):
      print("Errore nel contattare il server " + str(response.status_code))
      return False
   else:
      print("Ricevuta una risposta di tipo " + response.headers["Content-Type"])
      return True


def main():
   create_record()
   query()
  

def main_with_auth():
   #register_user()
   key = login_user("utente1","u1_password")
   create_record_auth(key)
   query_auth(key)
   logout_user(key)


def register_user():

   #ricorda: password validator sono attivi!

   print("Procedura di registrazione")
   username = input("Inserisci lo username ")
   pw = input("Inserisci password ")

   reg_server = "http://127.0.0.1:8000/registration/"
   post_values = { "username":username, "password1" : pw, "password2" : pw }
   response = requests.post(reg_server, json=post_values)

   if check_response(response): print("Registrazione avvenuta con successo")
   else: print("Errore nella registrazione")

   print(response)


def login_user(username, pw):

   auth_server = "http://127.0.0.1:8000/auth/login/"
   post_values = { "username":username, "password" : pw}
   response = requests.post(auth_server, json=post_values)

   if check_response(response): print("Login valido")
   else: print("Errore nel login")

   data = json.loads(response.content.decode('utf-8'))
   print("Chiave ricevuta " + str(data["key"]))

   return data["key"]


def logout_user(token):

   auth_server = "http://127.0.0.1:8000/auth/logout/"

   response = requests.post(auth_server, json={}, headers={'Authorization': 'Token {}'.format(token)})

   if check_response(response): print("Logout eseguito")
   else: print("Errore nel logout")

   del token #distruzione del token client side.

   print(response.content)


def create_record():
   rest_server = "http://127.0.0.1:8000/todo/"

   hostname = socket.gethostname()
   local_ip = socket.gethostbyname(hostname)

   post_values = { "userIP" : local_ip, "title": "Bla Bla Bla ..."} #non riempiamo tutti i campi...
   response = requests.post(rest_server, json=post_values)

   if not check_response(response): return

   print(response.json())   


def create_record_auth(token):
   rest_server = "http://127.0.0.1:8000/todo/"

   hostname = socket.gethostname()
   local_ip = socket.gethostbyname(hostname)

   post_values = { "userIP" : local_ip, "title": "Bla Bla Bla ..."} #non riempiamo tutti i campi...
   response = requests.post(rest_server, json=post_values,  
                           headers={'Authorization': 'Token {}'.format(token)})

   if not check_response(response): return

   print(response.json())   


def query():

   rest_server = "http://127.0.0.1:8000/todo/"

   response = requests.get(rest_server)

   if not check_response(response): return

   response = response.json()

   print("Ho ricevuto " + str(len(response))+ " Entry(s)")

   for r in response: #stampiamole tutte
      print(r)

   first_response = response[0] #isoliamone la prima

   for k in first_response: #stampiamo le chiavi
      print(k)

   print("Titolo della prima: " + first_response["title"])

   #andiamo a prendere un record specifico, e.g. il numero 1
   
   rest_server += "1/" 
   response = requests.get(rest_server)

   if not check_response(response): return

   response = response.json()

   print("Record numero 1: \n" +  str(response)) #stampiamo


def query_auth(token):

   rest_server = "http://127.0.0.1:8000/todo/"

   response = requests.get(rest_server,headers={'Authorization': 'Token {}'.format(token)})

   if not check_response(response): return

   response = response.json()

   print("Ho ricevuto " + str(len(response))+ " Entry(s)")

   for r in response: #stampiamole tutte
      print(r)

   first_response = response[0] #isoliamone la prima

   for k in first_response: #stampiamo le chiavi
      print(k)

   print("Titolo della prima: " + first_response["title"])

   #andiamo a prendere un record specifico, e.g. il numero 1
   
   rest_server += "1/" 
   response = requests.get(rest_server, headers={'Authorization': 'Token {}'.format(token)})

   if not check_response(response): return

   response = response.json()

   print("Record numero 1: \n" +  str(response)) #stampiamo


if __name__ == "__main__":
   #main()
    main_with_auth()