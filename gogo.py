from flask import Flask, request, redirect, url_for, send_from_directory, redirect
from flask_pymongo import PyMongo, ASCENDING
import os
from werkzeug.utils import secure_filename


from modules.items.views import itemsView
from modules.logging.views import logsView
from modules.barcodes.views import barcodesView

from modules.logging.controller import Logs
from modules.notifications.controller import Notifications
from modules.notifications import mail

app = Flask(__name__, static_folder='static', static_url_path='')

app.config.from_object('config.DevelopmentConfig')

mongo = PyMongo(app)

with app.app_context():
	itemsView.db = mongo.db.items
	Logs.db = mongo.db.logs
	logsView.db = mongo.db.logs
	barcodesView.db = mongo.db.barcodes

	itemsView.db.create_index([("name", ASCENDING)], unique=True)

	Notifications.errors = app.config['NOTIFY_ERRORS']

	mail.templates['error']['dest'] = app.config['MAILER_DEST']['error']
	mail.templates['warning']['dest'] = app.config['MAILER_DEST']['warning']
	mail.templates['info']['dest'] = app.config['MAILER_DEST']['info']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


#ROUTES
# Custom static data
@app.route('/cdn/<path:filename>', endpoint='assets_static')
def assets_static(filename):
    return send_from_directory(app.config['ASSETS_PATH'], filename)

@app.route('/cdn/<path:filename>', endpoint='uploads_static')
def uploads_static(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/')
def index():
    return redirect('http://localhost:5000/items/', 302)

@app.route('/barcodes/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

itemsView.register(app)
logsView.register(app)
barcodesView.register(app)

if __name__ == '__main__':
	app.run()

