from flask import Flask, render_template, request, url_for, flash, redirect
import os
from werkzeug.utils import secure_filename
from cycle_gan import generate_image

app = Flask(__name__)
app.debug = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['RESULT_FOLDER'] = 'static/results/'
app.secret_key = 'sopiro'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/references')
def ref():
    return render_template('references.html')


@app.route('/sources')
def src():
    return render_template('sources.html')


@app.route('/license')
def lic():
    return render_template('license.html')


@app.route('/uploaded/<filename>')
def display_uploaded(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/results/<filename>')
def display_result(filename):
    return redirect(url_for('static', filename='results/' + filename), code=301)


@app.route('/transform', methods=['POST'])
def transform():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect('/')

        f = request.files['file']

        if request.form['submit_button'] == '그림처럼!':
            mode = 2
        elif request.form['submit_button'] == '사진처럼!':
            mode = 1

        if f.filename == '':
            flash('파일을 선택해 주세요')
            return redirect('/')

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_path = os.path.abspath(app.config['UPLOAD_FOLDER'] + filename)
            save_path = os.path.abspath(app.config['RESULT_FOLDER'] + filename)

            generate_image(image_path, save_path, mode)

            return render_template('result.html', filename=filename)
        else:
            return redirect('/')


if __name__ == '__main__':
    if not os.path.exists("static"):
        os.mkdir('static')
        os.mkdir('static/uploads')
        os.mkdir('static/results')

    app.run(host='0.0.0.0')
