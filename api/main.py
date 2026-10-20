
from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

DEFAULT_GIF = "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif"

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "name": "Max's Image API",
        "endpoint": "/api/image"
    })

@app.route("/api/image", methods=["GET"])
def image():
    image_url = request.args.get("url", DEFAULT_GIF)

    if not image_url.startswith("https://"):
        return jsonify({"error": "HTTPS URLs only"}), 400

    try:
        response = requests.get(
            image_url,
            timeout=15,
            headers={"User-Agent": "MaxImageAPI/1.0"},
            allow_redirects=True
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        content_type = content_type.split(";")[0].strip().lower()

        if content_type not in (
            "image/gif",
            "image/jpeg",
            "image/png",
            "image/webp"
        ):
            return jsonify({"error": "Unsupported image format"}), 400

        if content_type == "image/gif" and not response.content.startswith(
            (b"GIF87a", b"GIF89a")
        ):
            return jsonify({"error": "Invalid GIF data"}), 502

        return Response(
            response.content,
            status=200,
            content_type=content_type,
            headers={"Cache-Control": "public, max-age=300"}
        )

    except requests.RequestException:
        return jsonify({"error": "Unable to retrieve image"}), 502

if __name__ == "__main__":
    app.run(debug=False)
