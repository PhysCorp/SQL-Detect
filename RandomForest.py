from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import pickle


# sample data
data = {
    "query": [
        "SELECT * FROM users WHERE id = 1",
        "SELECT id FROM users WHERE username = 'admin' --",
        "UPDATE users SET password = 'passwd' WHERE id = 1",
        "' OR '1'='1",
        "SELECT * FROM products WHERE category = 'books'",
        "1; DROP TABLE users"
    ],
    "is_malicious": [0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

# vectorize the queries
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['query'])

# target values
y = df['is_malicious']

# split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# random forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# predict
y_pred = clf.predict(X_test)

# evaluate
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


# save the vectorizer and model
with open('vectorizer.pkl', 'wb') as file:
    pickle.dump(tfidf_vectorizer, file)

with open('model.pkl', 'wb') as file:
    pickle.dump(clf, file)