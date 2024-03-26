from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle


# load the model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)


app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    # get the query from the request
    data = request.json
    query = data.get('query')

    # check if the query is provided
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # transform the query
    query_vector = vectorizer.transform([query])

    # predict using the model
    prediction = model.predict(query_vector)

    # return the result
    is_malicious = bool(prediction[0])
    return jsonify({'is_malicious': is_malicious})

if __name__ == '__main__':
    app.run(debug=True)
