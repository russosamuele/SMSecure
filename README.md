# SMSecure - Filtro Spam SMS con IA

# Obiettivi
Implementare un filtro anti spam SMS, andando ad estrapolare i dati a partire da un dataset, andare ad analizzarli e infine preprocessarli per darli in input ad uno o più algortimi di Machine Learning. 

# Struttura della repo
Sono presenti due branch. Il test branch è stato usato durante lo sviluppo per modifiche, ma attualmente è aggiornato con il main branch.

All'interno della repository ci sono due file in particolare:
- SMSecure.ipynb, che è il notebook usato per l'intero processo di sviluppo.
- sms_dataset.csv, che è il dataset utilizzato per la costruzione del modello.

Sono presenti inoltre due cartelle (una dedicata allo sviluppo dell'app, una alla documentazione):
- App, che contiene gli export (modello, vectorizer, frequenze parole ham/spam) dal notebook, nonchè il file app.py, che è la vera e propria app che consentirà di inserire dei messaggi e di classificarne il tipo.
- Documentazione: contiene l'export sorgente di tutta la documentazione scritta in latex, nonchè l'export in pdf.


# Replicare il progetto
Requisiti:
- Python 3

Consigli d'utilizzo:
- PyCharm IDE

Dato che la repo è pubblica, sarà possibile scaricare l'intera repo. 
Dopo aver scaricato la repo:
- aprire il progetto con PyCharm, o un qualunque IDE
- aprire un terminale nella cartella 'App'
- digitare 'streamlit run app.py'
A questo punto verrà lanciata l'app SMSecure sul browser di default, e sarà possibile inserire nel sistema dei messaggi. Cliccando il pulsante 'Predict' il sistema classificherà il messaggio e mostrerà l'output.

# Grazie per la lettura!

  


