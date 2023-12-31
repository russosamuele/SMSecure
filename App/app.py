import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack
import pandas as pd


# oggetti per utilizzi futuri
ps = PorterStemmer()
scaler = MinMaxScaler()

# sessione di stato (mi serve per mantenere la history dei messaggi)
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []


# funzione per trasformare il testo
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# funzione per calcolare il numero di words e il numero di characters
def calculate_word_char_count(text):
    words = len(text.split())
    characters = len(text)
    return words, characters


# import modello, tfidf, frequenza parole ham, frequenza parole spam
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))
spamWords = pickle.load(open('spamWords.pkl', 'rb'))
hamWords = pickle.load(open('hamWords.pkl', 'rb'))

# APP

st.title("SMSecure - SMS Spam Classifier") # titolo

input_sms = st.text_area("Enter the message") # input

if not input_sms:
    st.warning("Please enter a message.") # messaggio visualizzato con text area vuota
else:
    if st.button('Predict', key='prediction_button', help='Click to predict'):
        # calcolo numero words e numero caratteri
        num_words, num_characters = calculate_word_char_count(input_sms)

        # Normalizzo le feature con il MinMaxScaler
        features = [[num_words, num_characters]]
        normalized_features = scaler.fit_transform(features)

        # trasformo il testo con la funzione definita in alto
        transformed_sms = transform_text(input_sms)

        # cerco corrispondenze con parole spam
        parole_Spamchiave_trovate = [parola for parola in spamWords if parola in transformed_sms]

        # cerco corrispondenze con parole ham
        parole_Hamchiave_trovate = [parola for parola in hamWords if parola in transformed_sms]

        # applico il tfid sul testo trasformato per avere una rappresentazione numerica processabile dal modello
        vector_input = tfidf.transform([transformed_sms])

        # unisco il testo già vettorizzato con le due feature normalizzate
        final_features = hstack([vector_input[:, :2998], normalized_features])

        # predizione
        result = model.predict(final_features)[0]

        # stampa del risultato
        if result == 1:
            st.header("Spam")
            if parole_Spamchiave_trovate:
                st.write("Parole chiave spam trovate:", ", ".join(parole_Spamchiave_trovate))
        else:
            st.header("Ham")
            if parole_Hamchiave_trovate:
                st.write("Parole chiave ham trovate:", ", ".join(parole_Hamchiave_trovate))

        # Aggiungi la predizione alla history
        st.session_state.predictions_history.append({"Message": input_sms, "Prediction": "Spam" if result == 1 else "Ham"})


st.markdown("---") # linea di divisione grafica

# Mostra la tabella delle predizioni passate
st.title("Predictions History")
if st.session_state.predictions_history:
    df_predictions = pd.DataFrame(st.session_state.predictions_history)
    st.table(df_predictions)
else:
    st.info("No predictions made yet.")
