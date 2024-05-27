import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        response = requests.post(
            "http://localhost:5001/predict",
            files={"image": file},
        )
        if response.status_code == 200:
            print(response.json())
            return jsonify(response.json())
        else:
            return (
                jsonify({"error": "Failed to get prediction"}),
                response.status_code,
            )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
