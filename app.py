from flask import Flask, render_template, request
from transformers import pipeline
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load the model once when the server starts
detector = pipeline("image-classification", model="umm-maybe/AI-image-detector")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if not file:
        return "No file received", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Run the image through the model
    image = Image.open(filepath).convert("RGB")
    results = detector(image)

    # Parse the results
    scores = {r['label']: round(r['score'] * 100, 2) for r in results}
    ai_score = scores.get('artificial', scores.get('LABEL_1', 0))
    real_score = scores.get('human', scores.get('LABEL_0', 0))

    return render_template('result.html', ai_score=ai_score, real_score=real_score, filename=file.filename)

if __name__ == '__main__':
    app.run(debug=True)