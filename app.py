
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/fix')
def fix():
    text = request.args.get('text', '')
    if not text:
        return "No input provided."

    response = requests.post(
        "https://api.languagetool.org/v2/check",
        data={
            "text": text,
            "language": "en-US"
        }
    )

    matches = response.json().get("matches", [])

    # Apply replacements
    corrected_text = list(text)
    offset_correction = 0
    for match in matches:
        replacements = match.get("replacements", [])
        if replacements:
            replacement = replacements[0]["value"]
            offset = match["offset"] + offset_correction
            length = match["length"]
            corrected_text[offset:offset+length] = list(replacement)
            offset_correction += len(replacement) - length

    return "".join(corrected_text)
