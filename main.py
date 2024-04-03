# Imports
try:
    from quart import Quart, request, jsonify # Replaced Flask here as we need async functions
    import asyncio # Async functions
    import hypercorn # ASGI server
    from hypercorn.config import Config # Hypercorn config
    from hypercorn.asyncio import serve # Serve requests
    from sklearn.feature_extraction.text import TfidfVectorizer # vectorize queries
    from sklearn.ensemble import RandomForestClassifier # random forest classifier
    import pickle # load model and vectorizer
    from RandomForest import RandomForestModel # our custom random forest model
    import pandas as pd # data manipulation
    import os # file operations
    import tempfile # temporary file operations
    import shutil # file deletion
    import time # time operations
    import requests # HTTP requests
    import warnings # hide warnings
    from sklearn.exceptions import UndefinedMetricWarning # load warning to hide
    warnings.filterwarnings("ignore", category=UndefinedMetricWarning) # hide the UndefinedMetricWarning
except ImportError as e:
    print(f"Error importing libraries, did you install the requirements? {e}")
    exit()

# Get the maindirectory path (failsafe)
maindirectory = os.path.dirname(os.path.abspath(__file__))

# Set hypercorn config
config = Config()
config.bind = ["0.0.0.0:80"] # bind to all interfaces on port 80

# If MODEL_URL AND VECTORIZER_URL are set in the environment variables and the files don't exist, download the model and vectorizer
MODEL_URL = os.getenv('MODEL_URL', '')
VECTORIZER_URL = os.getenv('VECTORIZER_URL', '')
model_filepath = os.path.join(maindirectory, 'data', 'model.pkl')
vectorizer_filepath = os.path.join(maindirectory, 'data', 'vectorizer.pkl')
if MODEL_URL and VECTORIZER_URL and not os.path.exists(model_filepath) and not os.path.exists(vectorizer_filepath):
    print("[INFO] Downloading model and vectorizer...")
    model_response = requests.get(MODEL_URL)
    vectorizer_response = requests.get(VECTORIZER_URL)
    with open(model_filepath, 'wb') as model_file:
        model_file.write(model_response.content)
    with open(vectorizer_filepath, 'wb') as vectorizer_file:
        vectorizer_file.write(vectorizer_response.content)
    print("[INFO] Model and vectorizer downloaded.")
else:
    print("[INFO] Model and vectorizer either already exist, or URL is not specified. Skipping download.")

# Async function to train a model with a given CSV filepath, then delete the entire dir after training
async def train_model(filepath, skip_deletion=False):
    print(f"[AI] Beginning [re]training of model with CSV file at {filepath}...")
    # Read the data from CSV file
    df = pd.read_csv(os.path.join(maindirectory, 'data', 'training_data_sample.csv'), delimiter=',', encoding='utf-8', quotechar='"')
    X = df['query'] # Features
    Y = df['is_malicious'] # Target
    # Initialize and train the model
    print(f"[AI] Training model with {len(X)} samples...")
    model = RandomForestModel()
    model.train(X, Y)
    print("[AI] Training completed, saving model...")
    model.save_model()
    if not skip_deletion:
        print("[AI] Deleting temporary directory...")
        # Delete the entire directory
        shutil.rmtree(os.path.dirname(filepath))
    print("[AI] Done.")

# Async function to get the number of all tasks
async def get_all_tasks():
    return len(asyncio.all_tasks())

# load the model and vectorizer
try:
    with open(os.path.join(maindirectory, 'data', 'model.pkl'), 'rb') as model_file:
        model = pickle.load(model_file)
    with open(os.path.join(maindirectory, 'data', 'vectorizer.pkl'), 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
except FileNotFoundError:
    print("[INFO] Model and/or vectorizer not found, beginning training process with sample data as failsafe...")
    # Run the async function as a synchronous function
    asyncio.run(train_model(os.path.join(maindirectory, 'data', 'training_data_sample.csv'), skip_deletion=True))
    # Load the model and vectorizer
    with open(os.path.join(maindirectory, 'data', 'model.pkl'), 'rb') as model_file:
        model = pickle.load(model_file)
    with open(os.path.join(maindirectory, 'data', 'vectorizer.pkl'), 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    print("[INFO] Training completed and model loaded.")

# Init Flask (Quart) app
app = Quart(__name__)

# Init preferences
# If SECRET_TRAIN_PASSKEY is not set in the environment variables, set to default of 1234
SECRET_TRAIN_PASSKEY = os.getenv('SECRET_TRAIN_PASSKEY', '1234')
# If ALLOW_TRAINING is not set, set to default of False
ALLOW_TRAINING = os.getenv('ALLOW_TRAINING', 'False').lower() == 'true'

# Main endpoint, user sends POST to /detect with SQL query specified in query parameter
@app.route('/detect', methods=['POST'])
async def detect():
    # Get the query from the POST request
    form_data = await request.form
    query = form_data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    print(f"[DETECT] Beginning detection for `{query}`...")
    # Transform query using vectorizer
    query_vector = vectorizer.transform([query])
    # Predict using model
    prediction = model.predict(query_vector)
    # Return result
    is_malicious = bool(prediction[0])
    print(f"[DETECT] Prediction: {is_malicious}")
    return jsonify({'is_malicious': is_malicious})

# Endpoint to upload a CSV file for training
@app.route('/upload_csv', methods=['POST'])
async def upload_csv():
    # check if training is enabled
    if not ALLOW_TRAINING:
        return jsonify({'error': 'Training is not enabled'}), 403
    # get form data
    form_data = await request.form
    # check if the post request has the password part
    if 'password' not in form_data:
        return jsonify({'error': 'No password provided'}), 400
    password = form_data['password']
    # check if the password matches the secret passkey
    if password != SECRET_TRAIN_PASSKEY:
        return jsonify({'error': 'Invalid password'}), 403
    # check if the post request has the file part
    if 'file' not in (await request.files):
        return jsonify({'error': 'No file part in the request'}), 400
    file = (await request.files)['file']
    # if user does not select file, browser submits an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        # check if there are any tasks running
        if not asyncio.all_tasks():
            # create a temporary directory using the tempfile module
            with tempfile.TemporaryDirectory() as tmpdirname:
                # save the file to the temporary directory
                file.save(os.path.join(tmpdirname, file.filename))
                # call train_model asynchronously
                asyncio.create_task(train_model(os.path.join(tmpdirname, file.filename)))
                return jsonify({'message': 'File saved and model training started'}), 200
        else:
            return jsonify({'error': 'Another training process is already in progress'}), 400
    else:
        return jsonify({'error': 'Uploaded file is not a CSV file'}), 400

# Healthcheck endpoint, returning system status and training status
@app.route('/')
@app.route('/healthcheck')
def healthcheck():
    status = 'ok'
    training_status = 'idle'
    if asyncio.run(get_all_tasks()) > 1:
        training_status = 'in progress'
    return jsonify({'status': status, 'training': training_status, 'message': 'System is operational. Please POST to /detect with \'query\' to use the service.'})

if __name__ == '__main__':
    print("[INFO] Starting server on port 80...")
    # Serve request using Hypercorn
    asyncio.run(serve(app, config))
