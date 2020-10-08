import os
from flask import Flask
from flask import request
from flask import make_response
from main import SudokuKit
#from flask_cors import CORS
#from werkzeug.utils import secure_filename

from datetime import datetime

app = Flask(__name__)
#cors = CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/upload', methods=['POST'])
def upload():
    print("Got a request")
    pic_name = 'scr.png'
    if 'capture' in request.files:
        request.files['capture'].save(pic_name)
        SudokuKit().solve_from_picture(pic_name)
    else:
        print("file not sent")
    return ""