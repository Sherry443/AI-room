from flask import Flask, render_template, request, send_file, redirect, url_for
import requests
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/generated'

# API Configuration
API_URL = "https://try-on-diffusion.p.rapidapi.com/try-on-file"
HEADERS = {
    "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com",
    "x-rapidapi-key": "7a258408a0mshdbf99bcf3cc49fap15d3b1jsn5bafd765f661",
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result_path = None
    error = None

    if request.method == 'POST':
        files = {}
        data = {}

        clothing_image = request.files.get('clothing_image')
        clothing_prompt = request.form.get('clothing_prompt')

        avatar_image = request.files.get('avatar_image')
        avatar_sex = request.form.get('avatar_sex')
        avatar_prompt = request.form.get('avatar_prompt')

        background_image = request.files.get('background_image')
        background_prompt = request.form.get('background_prompt')

        seed = request.form.get('seed')
        if seed and seed != "-1":
            data['seed'] = seed

        if clothing_image:
            files["clothing_image"] = (clothing_image.filename, clothing_image.stream, clothing_image.mimetype)
        if clothing_prompt:
            data["clothing_prompt"] = clothing_prompt

        if avatar_image:
            files["avatar_image"] = (avatar_image.filename, avatar_image.stream, avatar_image.mimetype)
        if avatar_sex:
            data["avatar_sex"] = avatar_sex
        if avatar_prompt:
            data["avatar_prompt"] = avatar_prompt

        if background_image:
            files["background_image"] = (background_image.filename, background_image.stream, background_image.mimetype)
        if background_prompt:
            data["background_prompt"] = background_prompt

        response = requests.post(API_URL, headers=HEADERS, files=files, data=data)

        if response.status_code == 200:
            now = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"tryon_output_{now}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            result_path = f"/{filepath}"
        else:
            error = f"API Failed: {response.status_code} {response.text}"

    return render_template("index.html", error=error, result_image=result_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)