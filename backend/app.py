from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load trained model
model = tf.keras.models.load_model("action_model.h5")

# Labels for your dataset
labels = ["calling","clapping","cycling","dancing","drinking","eating",
          "fighting","hugging","laughing","listening_to_music",
          "running","sitting","sleeping","texting","using_laptop"]

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img = Image.open(file).resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    action = labels[np.argmax(pred)]
    return jsonify({"action": action})

if __name__ == "__main__":
    app.run(debug=True)
