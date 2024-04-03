# [ Copyright 2024 MIT License ]

# Imports
try:
    from sklearn.feature_extraction.text import TfidfVectorizer # vectorize the queries
    from sklearn.ensemble import RandomForestClassifier # random forest classifier
    from sklearn.model_selection import train_test_split # split the data
    from sklearn.metrics import classification_report, accuracy_score # evaluate the model
    import pickle # save model and vectorizer
    import os # file operations
except ImportError as e:
    print(f"Error importing libraries, did you install the requirements? {e}")
    exit()

# Get the maindirectory path (failsafe)
maindirectory = os.path.dirname(os.path.abspath(__file__))

class RandomForestModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X, y):
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        # Fit the vectorizer on the training data and transform training and test data
        X_train = self.vectorizer.fit_transform(X_train)
        X_test = self.vectorizer.transform(X_test)
        # Train the model
        self.model.fit(X_train, y_train)
        # Make predictions on the test data
        y_pred = self.model.predict(X_test)
        # Print the classification report and accuracy
        print(classification_report(y_test, y_pred))

    def save_model(self):
        with open(os.path.join(maindirectory, 'data', 'vectorizer.pkl'), 'wb') as file:
            pickle.dump(self.vectorizer, file)
        with open(os.path.join(maindirectory, 'data', 'model.pkl'), 'wb') as file:
            pickle.dump(self.model, file)

    def load_model(self):
        with open(os.path.join(maindirectory, 'data', 'vectorizer.pkl'), 'rb') as file:
            self.vectorizer = pickle.load(file)
        with open(os.path.join(maindirectory, 'data', 'model.pkl'), 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, query):
        query_vector = self.vectorizer.transform([query])
        prediction = self.model.predict(query_vector)
        return bool(prediction[0])

if __name__ == "__main__":
    print("This is the RandomForestModel class and is not designed to be run directly. Please import this file and use the class methods.")
    exit()