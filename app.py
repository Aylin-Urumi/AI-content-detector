from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

SIGHTENGINE_USER = os.environ.get('SIGHTENGINE_USER')
SIGHTENGINE_SECRET = os.environ.get('SIGHTENGINE_SECRET')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if not file:
        return render_template('error.html', message="No file was uploaded. Please go back and try again.")

    allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
    extension = file.filename.rsplit('.', 1)[-1].lower()
    if extension not in allowed_extensions:
        return render_template('error.html', message="Invalid file type. Please upload a JPG, PNG, or WEBP image.")

    filename = os.path.basename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        with open(filepath, 'rb') as image_file:
            response = requests.post(
                'https://api.sightengine.com/1.0/check.json',
                files={'media': image_file},
                data={
                    'models': 'genai',
                    'api_user': SIGHTENGINE_USER,
                    'api_secret': SIGHTENGINE_SECRET
                }
            )
        result = response.json()
        print(result)

        if result.get('status') != 'success':
            return render_template('error.html', message="Analysis failed. Please try again with a different image.")

        ai_score = round(result.get('type', {}).get('ai_generated', 0) * 100, 1)
        real_score = round(100 - ai_score, 1)

        if ai_score >= 80:
            reason = "Strong indicators of AI generation detected. Pixel patterns, lighting, and texture consistency are characteristic of AI image generators."
        elif ai_score >= 50:
            reason = "Several features suggest AI generation. Some areas show unnatural consistency typical of generative models."
        elif ai_score >= 20:
            reason = "Mostly appears real with a few uncertain regions. Could be a heavily edited photo or partially AI-generated."
        else:
            reason = "Image shows strong characteristics of a real photograph. Natural noise, lighting inconsistencies, and texture patterns detected."

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', message="Something went wrong during analysis. Please try again.")

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return render_template('result.html',
                           ai_score=ai_score,
                           real_score=real_score,
                           filename=filename,
                           reason=reason)

if __name__ == '__main__':
    app.run(debug=True)