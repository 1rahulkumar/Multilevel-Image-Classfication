from flask import *
import os 
import cv2
from opencv import *
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os
import pandas as pd
from collections import Counter
from sklearn.cluster import KMeans

import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from modulevechiletetect import myvechiledetection
global result
result=()


app = Flask(__name__,template_folder='templates')
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
        
         file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        
        flash('Image successfully uploaded and displayed below')
        
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
        
        print("display")
@app.route('/display/<filename>')

def display_image(filename):
    
    
    #print('display_image filename: ' + filename)
 
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/<filename>')
def result_model(filename):
    print('start')
    
    path_image=str('static/uploads/' + str(filename))
    result=tuple(myvechiledetection.run(str(path_image)))
    return render_template('result.html',result=result)


    if __name__ == '__main__':  
       app.run(debug = True)
       
    
        
