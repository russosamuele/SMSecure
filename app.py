import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack
import pandas as pd


ps = PorterStemmer()
scaler = MinMaxScaler()

# Inizializza la sessione di stato
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


# import model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("SMSSecure - SMS Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict', key='prediction_button', help='Click to predict'):
    # calcolo numero words e numero caratteri
    num_words, num_characters = calculate_word_char_count(input_sms)

    # Normalizzo le feature con il MinMaxScaler
    features = [[num_words, num_characters]]
    normalized_features = scaler.fit_transform(features)

    # trasformo il testo (stemming, riduzione a maiuscolo ecc.)
    transformed_sms = transform_text(input_sms)

    # applico il tfid sul testo trasformato per avere una rappresentazione numerica processabile dal modello
    vector_input = tfidf.transform([transformed_sms])

    # unisco il testo già vettorizzato con le due feature normalizzate
    final_features = hstack([vector_input[:, :2998], normalized_features])

    # predizione
    result = model.predict(final_features)[0]

    # stampa del risultato
    if result == 1:
        st.header("Spam")
    else:
        st.header("Ham")

    # Aggiungi la predizione alla lista di storico
    st.session_state.predictions_history.append({"Message": input_sms, "Prediction": "Spam" if result == 1 else "Ham"})


# Mostra la tabella delle predizioni passate
st.title("Predictions History")
if st.session_state.predictions_history:
    df_predictions = pd.DataFrame(st.session_state.predictions_history)
    st.table(df_predictions)
else:
    st.info("No predictions made yet.")
