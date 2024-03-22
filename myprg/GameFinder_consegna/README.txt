Per installare tutte le librerie del progetto dare il seguente comando:
pip install -r requirements.txt

L'interfaccia utente è stata creata con il framework Django.
Per provarla, entrare nella cartella /GameSearcher e dare il seguente comando:
python manage.py runserver
e andare su http://127.0.0.1:8000/

Benchmark:
Il file contenete le UIN è presente in UIN.txt
Nel file Data_comparison sono presenti le valutazioni del benchmark
Per la valutazione del benchmark sono state usate le seguenti misurazioni:
- precision e recall
- average precision
- MAP
- DCG
- Media armonica DCG