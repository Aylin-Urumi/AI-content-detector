from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import os
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)
 
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)
 
SIGHTENGINE_USER = os.environ.get('SIGHTENGINE_USER')
SIGHTENGINE_SECRET = os.environ.get('SIGHTENGINE_SECRET')
 
COUNTER_FILE = 'counter.txt'
 
def get_count():
    if not os.path.exists(COUNTER_FILE):
        return 0
    with open(COUNTER_FILE, 'r') as f:
        return int(f.read().strip() or 0)
 
def increment_count():
    count = get_count() + 1
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(count))
    return count
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/count')
def count():
    return jsonify({'count': get_count()})
 
@app.route('/ping')
def ping():
    return 'OK', 200
 
@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per hour")
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
 
        total = increment_count()
 
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
                           reason=reason,
                           total=total)
 
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return render_template('error.html', message="Too many requests. You can analyze up to 10 images per hour. Please try again later."), 429
 
if __name__ == '__main__':
    app.run(debug=True)