from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DOWNLOADER_API = "https://pinterestdownloader.io/frontendService/DownloaderService"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://pinterestdownloader.io/",
    "Origin": "https://pinterestdownloader.io"
}


@app.route("/")
def home():
    return jsonify({
        "creator": "Xeon VRO",
        "status": True,
        "message": "Pinterest Downloader API Running"
    })


@app.route("/pin", methods=["GET"])
def download_pin():
    pin_url = request.args.get("url")

    if not pin_url:
        return jsonify({
            "creator": "Xeon VRO",
            "status": False,
            "message": "Missing url parameter"
        }), 400

    try:
        response = requests.get(
            DOWNLOADER_API,
            params={"url": pin_url},
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return jsonify({
            "creator": "Xeon VRO",
            "status": True,
            "code": 200,
            "result": data
        })

    except requests.exceptions.HTTPError as e:
        return jsonify({
            "creator": "Xeon VRO",
            "status": False,
            "code": response.status_code,
            "message": f"HTTP Error: {str(e)}"
        }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            "creator": "Xeon VRO",
            "status": False,
            "code": 504,
            "message": "Request timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "creator": "Xeon VRO",
            "status": False,
            "code": 500,
            "message": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "creator": "Xeon VRO",
            "status": False,
            "code": 500,
            "message": f"Unexpected error: {str(e)}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
