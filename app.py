from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/check", methods=["POST"])
def check_plagiarism():
    try:
        data = request.get_json()
        text = data.get("text", "")

        # Bu yerda siz plagiatni tekshiradigan logikani qo‘shasiz
        # Hozircha test uchun shunchaki matn uzunligini qaytaramiz
        result = {
            "length": len(text),
            "plagiarism": "false"  # bu yerga haqiqiy tekshiruv natijasi keladi
        }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
