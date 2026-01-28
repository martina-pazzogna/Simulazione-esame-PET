# Simulazione-esame-PET

Nella cartella "progetto_esame" sono presenti due file .py:
- "sistema_pet.py" contiene l'implementazione della classe "esame", che descrive un generico esame PET, per il quale possono essere definite le caratteristiche richieste nella consegna, e contiene i metodi necessari alla simulazione.

- "simulazione_esame.py" contiene la simulazione di alcuni esami. Si è adottato il modulo "argparse", per evitare ogni volta l'esecuzione di tutto il codice, che richiederebbe dei tempi piuttosto lunghi. I comandi da utilizzare sono i seguenti:
    - "-e1" : si mostra la ricostruzione di una sorgente puntiforme;
    - "-e2" : si mostra la ricostruzione di una sorgente estesa;
    - "-e3" : si mostra il confronto degli esiti di esami eseguiti con tre macchinari con differente risoluzione temporale.

Senza questi comandi, il codice non produce risultati. L'ultimo comando potrebbe richiedere dei tempi di esecuzione di qualche minuto.
