 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import soundfile as sf
import numpy as np
from scipy.io import wavfile
from keras.models import load_model

# Load the pre-trained AI model
model = load_model('dog_bark_translator.h5')

# Create a Flask app
app = Flask(__name__)

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for recording a new dog bark
@app.route('/record', methods=['POST'])
def record():
    # Get the audio file from the user
    audio_file = request.files['audio_file']

    # Save the audio file on the server
    audio_file.save('new_bark.wav')

    # Load the audio file
    fs, data = wavfile.read('new_bark.wav')

    # Preprocess the audio data
    data = data / np.max(np.abs(data))

    # Predict the human-readable translation
    prediction = model.predict(np.expand_dims(data, axis=0))[0]

    # Return the prediction to the user
    return render_template('index.html', prediction=prediction)

# Define the route for displaying information about the app
@app.route('/about')
def about():
    return render_template('about.html')

# Define the route for providing contact information
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Run the app
if __name__ == '__main__':
    app.run()
