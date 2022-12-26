#Importing Libraries

import pandas as pd
import sqlite3
import os
import re


from datetime import datetime
from flask import Flask, jsonify, render_template, send_from_directory, make_response, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from fileinput import filename
from Script import process_word
from werkzeug.utils import secure_filename

#Defining app
app = Flask(__name__)


app.json_encoder= LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda : 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda : '1.0.0'),
    'description' : LazyString(lambda : 'Dokumentasi API untuk Data Processing dan Modeling'), 
    },
    host = LazyString(lambda: request.host)
)

#Flask swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)


#Connecting to database
conn = sqlite3.connect('api_databse.db', check_same_thread=False)
c = conn.cursor()
#Defining and executing the query for table data if it not available
conn.execute('''CREATE TABLE IF NOT EXISTS data (text varchar(255), text_clean varchar(255));''')



#1 Basic API "Hello World"
@swag_from("docs/hello_world.yml", methods = ['GET'])
@app.route('/hello_world', methods=['GET'])
def hello_world():
    json_response = {
        'status_code' : 200,
        'description': "Menyapa Hello World",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

#2 plain API "text"
@swag_from("docs/hello_world.yml", methods = ['GET'])
@app.route('/text', methods=['GET'])
def text():
    json_response = {
        'status_code' : 200,
        'description' : "Original Teks",
        'data' : "Halo, selamat datang di API Laili Salsabila. API ini untuk teks cleansing ya!",
    }

    response_data = jsonify(json_response)
    return response_data

#3 API for cleaning provided text 
@swag_from("docs/hello_world.yml", methods = ['POST'])
@app.route('/text_clean', methods=['POST'])
def text_clean():
    json_response = {
        'status_code' : 200,
        'description' : "Original Teks",
        'data' : process_word("Hallo,,,, nama*&@ saya adl Laili,,,, trims"),
    }
    
    response_data = jsonify(json_response)
    return response_data

#4 API for processing inputted text
@swag_from("docs/text_processing.yml", methods = ['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    text_clean = process_word(text)

    with conn:
        c.execute('''INSERT INTO data(text, text_clean) VALUES (? , ?);''', (text, text_clean))
        conn.commit()
    

    json_response = {
        'status_code' : 200,
        'description' : "Teks yang sudah diproses",
        'data' : text_clean,
    }

    response_data = jsonify(json_response)
    return response_data



#Defining allowed extensions
allowed_extensions = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


#5 API for processing inputted file
@swag_from("docs/file_Upload.yml", methods = ['POST'])
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files['file']

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        time_stamp = (datetime.now().strftime('%d-%m-%Y_%H%M%S'))

        new_filename = f'{filename.split(".")[0]}_{time_stamp}.csv'
        
        
        save_location = os.path.join('input', new_filename)
        file.save(save_location)


        filepath = 'input/' + str(new_filename)

        data = pd.read_csv(filepath, encoding='latin-1')
        first_column_pre_process = data.iloc[:, 0]

        cleaned_word = []

        for text in first_column_pre_process:
            file_clean = process_word(text)

            with conn:
                c.execute('''INSERT INTO data(text, text_clean) VALUES (? , ?);''',(text, file_clean))
                conn.commit()

            cleaned_word.append(file_clean)
        

        new_data_frame = pd.DataFrame(cleaned_word, columns= ['Cleaned Text'])
        outputfilepath = f'output/{new_filename}'
        new_data_frame.to_csv(outputfilepath)

    json_response = {
        'status_code' : 200,
        'description' : "File sudah berhasil diproses, silahkan akses output dalam bentuk .json di http://127.0.0.1:5000/output",
    }

    response_data = jsonify(json_response)
    return response_data

#API Interface
@app.route('/')
def interface():
    json_response = {
        'status_code' : 200,
        'description' : "Selamat Datang",
    }

    response_data = jsonify(json_response)
    return response_data

#Route for showing output
@swag_from("docs/output.yml", methods = ['GET'])
@app.route('/output')
def output():
    row = c.execute('''select * from data''')
    my_list = []
    for text in row:
        my_list.append(text)

    json_response = {
        'status_code' : 200,
        'description' : "Tampilan hasil cleansing, di sini",
        'data' : my_list,
    }

    response_data = jsonify(json_response)
    return response_data


# Error Handling
@app.errorhandler(400)
def handle_400_error(_error):
    "Return a http 400 error to client"
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    "Return a http 401 error to client"
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    "Return a http 404 error to client"
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    "Return a http 500 error to client"
    return make_response(jsonify({'error': 'Server error'}), 500)

#App runner
if __name__ == '__main__' :
    app.run(debug=True)