# [ Copyright 2024 MIT License ]

# Imports
try:
    from RandomForest import RandomForestModel # our custom random forest model
    import pandas as pd # data manipulation
    import os # file operations
except ImportError as e:
    print(f"Error importing libraries, did you install the requirements? {e}")
    exit()

# Get the maindirectory path (failsafe)
maindirectory = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Read the data from CSV file
    df = pd.read_csv(os.path.join(maindirectory, 'data', 'training_data_sample.csv'))
    X = df['query'] # Features
    Y = df['is_malicious'] # Target
    # Initialize and train the model
    model = RandomForestModel()
    model.train(X, Y)
    model.save_model()