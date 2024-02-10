import requests

def check_response(response) -> bool:
   if response.status_code not in range(200,204+1):
      print("Errore nel contattare il server " + str(response.status_code))
      return False
   else:
      print("Ricevuta una risposta di tipo " + response.headers["Content-Type"])
      return True
      

def main():
   #query()
   create_record()

def create_record():
   rest_server = "https://jsonplaceholder.typicode.com/todos/"
   post_values = { "userId" : 1, "id": 400, "title": "Bla Bla Bla ..." , "completed" :  False }
   response = requests.post(rest_server, json=post_values)

   if not check_response(response): return

   print(response.json())   


def query():

   rest_server = "https://jsonplaceholder.typicode.com/todos/"

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

   #andiamo a prendere un record specifico, e.g. il numero 10
   
   rest_server += "10/" #https://jsonplaceholder.typicode.com/todos/10/
   response = requests.get(rest_server)

   if not check_response(response): return

   response = response.json()

   print("Record numero 10: \n" +  str(response)) #stampiamo
   

if __name__ == "__main__":
    main()