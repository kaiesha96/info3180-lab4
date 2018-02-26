"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug import secure_filename
from forms import UploadForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

filefolder = app.config['UPLOAD_FOLDER']
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not session.get('logged_in'):
        abort(401)
        
    # Instantiate your form class
    form = UploadForm()
    if request.method == "POST": # and form.validate_on_submit():
        # Validate file upload on submit
        #if form.validate_on_submit():
            
        f = request.files['file']
            #filename = secure_filename(f.filename)
            #f = form.upload.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File Saved', 'success')
        return redirect(url_for('home'))
    
    flash('File Not Supported !', 'error')
    return render_template('upload.html',form=form)


def get_uploaded_images():
    image_names = os.listdir('./app/static/uploads')
    # rootdir = '.'
    # imgs = []
    # for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
    #     for file in files:
    #         imgs = imgs + [os.path.join(subdir,file)]
    #         print (imgs)
    return image_names
             
    
    
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)
    
@app.route('/files', methods=['POST','GET'])
def files():
    if not session.get('logged_in'):
        abort(401)
    
    # image_names = os.listdir('./app/static/uploads')
    image_names = get_uploaded_images()
    #print(image_names)
    return render_template("files.html", image_names=image_names)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
