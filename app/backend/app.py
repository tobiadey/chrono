import io
import os

import torch
import torch.nn.functional as F
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from torchvision import transforms

app = Flask(__name__)
CORS(app)

# Set up the path for the classification and regression models
current_dir = os.path.dirname(__file__)
classification_model_path = os.path.join(
    current_dir, "../../models/classifier_model.pth"
)
regression_model_path = os.path.join(current_dir, "../../models/regression_model.pth")

# Load the models
classification_model = torch.load(
    classification_model_path, map_location=torch.device("cpu")
)
classification_model.eval()

regression_model = torch.load(regression_model_path, map_location=torch.device("cpu"))
regression_model.eval()

CLASSES = [
    "Audemars Piguet",
    "Breitling",
    "Cartier",
    "Gucci",
    "IWC",
    "Jaegerle Coultre",
    "Movado",
    "Omega",
    "Panerai",
    "Patek Philippe",
    "Rolex",
    "Seiko",
    "Zenith",
]


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    image = Image.open(io.BytesIO(file.read()))
    image = image.convert("RGB")

    # Convert image to tensor
    image_tensor = transforms.ToTensor()(image).unsqueeze(0)

    # Predict the brand
    with torch.no_grad():
        outputs = classification_model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)
        max_probs, preds = torch.max(probabilities, 1)

    predicted_class = CLASSES[preds.item()]
    confidence = max_probs.item()

    # Predict the price using the regression model
    with torch.no_grad():
        price_output = regression_model(image_tensor)
        predicted_price = price_output.item()

    return jsonify(
        {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "price": f"${predicted_price:.2f}",
        }
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
