 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import soundfile as sf
import numpy as np
from tensorflow.keras.models import load_model

# Load the AI model
model = load_model('dog_bark_translator.h5')

# Create the Flask application
app = Flask(__name__)

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Define the route to handle the translation
@app.route('/translate', methods=['POST'])
def translate():
    # Retrieve the audio file from the request
    audio_file = request.files['audio_file']

    # Read the audio file
    audio, sr = sf.read(audio_file)

    # Preprocess the audio data
    audio = audio.reshape(1, -1)

    # Make predictions using the AI model
    prediction = model.predict(audio)

    # Get the translation from the prediction
    translation = prediction[0]

    # Redirect to the results page with the translation
    return redirect(url_for('results', translation=translation))

# Define the route to display the translation results
@app.route('/results')
def results():
    # Get the translation from the query string
    translation = request.args.get('translation')

    # Render the results page with the translation
    return render_template('results.html', translation=translation)

# Run the Flask application
if __name__ == '__main__':
    app.run()
