'''Main file for routing'''
from flask import send_file, flash, render_template
from flask import request, redirect
from werkzeug import secure_filename
from PIL import Image
import PIL
import os
from app import app
# from mollie.api.client import Client


ALLOWED_EXTENSIONS = set(
    ['txt', 'gif', 'png', 'jpg', 'jpeg',
     'bmp', 'rar', 'zip', '7zip', 'doc', 'docx']
    )


@app.route('/')
@app.route('/index')
def index():
    ''' Return Index'''
    return render_template('index.html', title='Home')


@app.route('/contact')
def contact():
    '''
    Some basic contact form
    '''
    return render_template('contact.html', title='Contact')


@app.route('/style')
def style():
    ''' Returns the Style transfer template'''
    return render_template('style.html', title='Style transfer')


@app.route('/upload_style', methods=['POST'])
def upload_style():
    ''' Method to upload the style image '''
    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    print(app.config['UPLOAD_FOLDER'])

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

    return render_template(
        'uploaded_style.html',
        success=success,
        filename=filename)


def allowed_file(filename):
    ''' Checks the filename with allowed extentions'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>', methods=['POST', 'GET'])
def send_image(filename):
    '''
    Procedure to send a thumbnail image to the user.
    '''
    create_thumbnail(filename)
    thumbnail_path = os.path.join("static", "uploads", "thumpnails", filename)
    return send_file(thumbnail_path, mimetype='image/jpg')


def create_thumbnail(image):
    ''' Function to create the thumbnail '''
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
        print("No success thumbnail")  # traceback.format_exc()
        return False


# @app.errorhandler(404)
# def page_not_found(error):
#     ''''to do'''
#     return render_template('404.html')


# @app.errorhandler(500)
# def server_error(error):
#     ''''to do'''
#     return render_template('500.html')


# @app.errorhandler(405)
# def method_error(error):
#     ''''to do'''
#     return render_template('405.html')
