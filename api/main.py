
from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "name": "Max's Image API"
    })

@app.route("/api/image", methods=["GET"])
def image():
    image_url = request.args.get(
        "url",
        "https://thekurdishproject.org/wp-content/uploads/2015/02/3333590254_514b4fd2dc_z.jpg"
    )

    if not image_url.startswith("https://"):
        return jsonify({"error": "HTTPS image URLs only"}), 400

    try:
        response = requests.get(
            image_url,
            timeout=10,
            headers={"User-Agent": "MaxImageAPI/1.0"}
        )
        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        )

        if not content_type.startswith("image/"):
            return jsonify({"error": "URL did not return an image"}), 400

        return Response(
            response.content,
            content_type=content_type
        )

    except requests.RequestException:
        return jsonify({"error": "Unable to retrieve image"}), 502
