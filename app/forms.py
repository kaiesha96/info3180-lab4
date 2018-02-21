'''import os
from flask import Flask, request, redirect, url_for, flash'''
#from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField

# imgs = UploadSet('images', IMAGES)
class UploadForm(FlaskForm):
    upload = FileField('Upload Your Image', validators = [FileRequired(), FileAllowed(['jpg', 'png'],'Images Only !')])
    
