import time

import flask
from werkzeug.utils import secure_filename, redirect

import pywin

app = flask.Flask(__name__)


from flask import Flask, request, url_for
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/individual/')
def route_individual():
    return render_template('page1.html')

@app.route('/csvfile/')
def upload_file():
    return render_template('page2.html')



def placeName(code):
    global uploaded_file
    uploaded_file=code


@app.route('/uploader', methods=['GET', 'POST'])
def execute_file():

    if request.method == 'POST':
        f = request.files['file']

        print("Printing file name here:",f.filename)
        placeName(f.filename)
        f.save(secure_filename(f.filename))
        return redirect(url_for('output_data')),placeName(f.filename)



@app.route('/output')
def output_data():
    def inner():
        output=[]
        print("I am printing at output:",uploaded_file)
        #output.copy()
        yield '<h3>Home (<a href ="/">home</a>)</h3>'
        while 'endofprogramcompletion' not in output:
            yield '<b>The commands are being executed.</b><br/><br/>'
            output = pywin.csv_file(uploaded_file).copy()
            yield '%s<br/>\n' % output
    return flask.Response(inner(), mimetype='text/html')

@app.route('/output1',methods=['GET', 'POST'])
def out_data1():
    hostname = request.form['hostname']
    username= request.form['username']
    password=request.form['password']
    commands=request.form['commands']
    def inner():
        yield '<h3>Home (<a href ="/">home</a>)</h3>'
        yield '<b>The commands are being executed.</b><br/><br/>'
        output = pywin.CreatePod(hostname, username, password, commands)
        for i in output:
            yield '%s<br/>\n' % i

    return flask.Response(inner(), mimetype='text/html')
app.run(debug=True,port=5055)