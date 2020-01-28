from flask import send_file, flash, render_template, jsonify, request, redirect, url_for, send_from_directory
from app import app
import random, os
from mollie.api.client import Client
from werkzeug import secure_filename
import simplejson
import PIL
from PIL import Image


ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})



@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/style')
def style():
    return render_template('style.html', title='Style transfer')

@app.route('/upload_style', methods=['POST'])
def upload_style():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    print(APP_ROOT)
    
    print(app.config['UPLOAD_FOLDER'])
    
    target = app.config['UPLOAD_FOLDER']

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'style.jpg'))
            success = "Loaded successfully"
            print("upload success!")
            

    return render_template('uploaded_style.html', success = success, filename = filename)
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>', methods=['POST', 'GET'])
def send_image(filename):
    path = os.path.join("static", "uploads", filename)
    create_thumbnail(filename, path)
    thumbnail_path = os.path.join("static", "uploads", "thumpnails", filename)
    return send_file(thumbnail_path, mimetype='image/jpg')


def create_thumbnail(image, path):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))
        print("success thumbnail")
        return True

    except:
        print("No success thumbnail") #traceback.format_exc()
        return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')


@app.errorhandler(405)
def method_error(e):
    return render_template('405.html')



#<h1 class="ui header">Your style image</h1>
#<div class="error-box" align="center">
 #   <img class="ui medium image error-image" src="{{ url_for('static', filename='uploads/style.jpg') }}">
#</div>

#<div class="error-box" align="center">
#    <img class="ui medium image error-image" src="{{ url_for('static', filename='uploads/ballet3_200.jpg') }}">
#</div>