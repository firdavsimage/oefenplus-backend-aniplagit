from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import docx2txt
import PyPDF2

app = Flask(__name__)
CORS(app)

def extract_text(path, filename):
    if filename.endswith(".pdf"):
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif filename.endswith(".docx"):
        return docx2txt.process(path)

    elif filename.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return ""

def calculate_plagiarism(text):
    words = text.lower().split()
    total = len(words)
    unique = len(set(words))
    if total == 0:
        return 0.0
    return round((1 - unique / total) * 100, 2)

@app.route("/api/check", methods=["POST"])
def check():
    if "file" not in request.files:
        return jsonify({"error": "Fayl yuborilmadi"}), 400

    file = request.files["file"]
    filename = file.filename

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp:
        file.save(temp.name)
        text = extract_text(temp.name, filename)
        os.unlink(temp.name)

    plagiarism = calculate_plagiarism(text)
    return jsonify({"text": text, "plagiarism": plagiarism})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
