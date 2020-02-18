'''Main file for routing'''
import os, re, os.path
from flask import send_file, flash, render_template
from flask import request, redirect
from werkzeug import secure_filename
from PIL import Image
import PIL
from app import app
from app.s3_interaction import list_files, upload_file
# from mollie.api.client import Client


ALLOWED_EXTENSIONS = set(
    ['txt', 'gif', 'png', 'jpg', 'jpeg',
     'bmp', 'rar', 'zip', '7zip', 'doc', 'docx']
    )

BUCKET = app.config['BUCKET']


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


@app.route('/upload_style', methods=['POST', 'GET'])
def upload_style():
    ''' Method to upload the style image '''
    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    print("called function upload_style")

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
            # upload to s3 folder
            s3_load = upload_file(
                os.path.join(app.config['UPLOAD_FOLDER'], 'style.jpg'),
                BUCKET)
            print("s3_returned: ", s3_load)
            create_thumbnail(filename, 'style.jpg')
            # success = "Loaded style successfully"
            print("upload success!")
    # Hier kan bv de gallery worden gebouwd.

    files = os.listdir(app.config['THUMBNAIL_FOLDER'])
    files = [file for file in files]
    print(files)
    return render_template('gallery.html', files=files)

    # return render_template(
    #     'uploaded_style.html',
    #     success=success,
    #     filename=filename)


@app.route('/upload_content', methods=['POST'])
def upload_content():
    ''' Method to upload the content image '''
    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    print("called function upload_content")

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'content.jpg'))
            # upload to s3 folder
            s3_load = upload_file(
                os.path.join(app.config['UPLOAD_FOLDER'], 'content.jpg'),
                BUCKET)
            print("s3_returned: ", s3_load)
            create_thumbnail(filename, 'content.jpg')
            success = "Loaded content successfully"
            print("upload success!")

    files = os.listdir(app.config['THUMBNAIL_FOLDER'])
    files = [file for file in files]
    return render_template('gallery.html', files=files)

    # return render_template(
    #     'uploaded_content.html',
    #     success=success,
    #     filename=filename)


def allowed_file(filename):
    ''' Checks the filename with allowed extentions'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/send_content/<filename>', methods=['POST', 'GET'])
def send_content(filename):
    '''
    Procedure to send a thumbnail image to the user.
    '''
    print("called function send_content")
    # create_thumbnail(filename)
    thumbnail_path = os.path.join("static", "uploads", "thumpnails", filename)
    return send_file(thumbnail_path, mimetype='image/jpg')


@app.route('/send_style/<filename>', methods=['POST', 'GET'])
def send_style(filename):
    '''
    Procedure to send a thumbnail image to the user.
    '''
    print("called function send_style")
    # create_thumbnail(filename)
    thumbnail_path = os.path.join("static", "uploads", "thumpnails", filename)
    return send_file(thumbnail_path, mimetype='image/jpg')


def create_thumbnail(image, app_name):
    ''' Function to create the thumbnail '''
    print("called function create_thumbnail")
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], app_name))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        delete_images(app.config['THUMBNAIL_FOLDER'])
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))
        print("success thumbnail")
        return True

    except:
        print("No success thumbnail")  # traceback.format_exc()
        return False


@app.route('/gallery', methods=['GET'])
def send_gallery():
    ''' Returns all images'''
    files = os.listdir(app.config['THUMBNAIL_FOLDER'])
    # files = [app.config['THUMBNAIL_FOLDER'] + '/' + file for file in files]
    files = [file for file in files]
    print(files)
    return render_template('gallery.html', files=files)


def delete_images(path_to_images):
    '''deletes images'''
    print("function delete_images called")
    for files in os.listdir(path_to_images):
        print(files)
        os.remove(os.path.join(path_to_images, files))
    print("removal successful")



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
