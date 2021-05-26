import functools,math,time,os
from werkzeug.utils import secure_filename, redirect
from flask import Flask, request, url_for, Response, render_template, make_response

import CSV_LI_WINDOW

session = []
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        uname = request.cookies.get('uname')
        print("Printing content of session here:",uname)

        if uname != "kiranrj07":
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function


@app.route('/')
def login():
    resp = make_response(render_template('login.html'))
    resp.set_cookie('uname',expires=0)
    return resp

@app.route('/validation', methods = ['POST', 'GET'])
def validation():
    uname = request.form['uname']
    password = request.form.get('passwd')
    print(uname, password)
    #user = db.find_by_name_and_password(user_name, password) DB statement here.
    user="kiranrj07"
    if user != "kiranrj07":
        #proper exception to be added here.
        raise ValueError("Invalid username or password supplied")
    resp = make_response(render_template('Index_page.html'))
    resp.set_cookie('uname', user)
    return resp

@app.route('/index')
@login_required
def index():
    return render_template('Index_page.html')

@app.route('/individual_page')
@login_required
def individual_page():
    return render_template('individual_page.html')


@app.route('/csv_file')
@login_required
def csv_file():
    return render_template('csv_page.html')


@app.route('/servers')
@login_required
def servers():
    print(request.form.getlist('my_checkbox'))
    return render_template('server.html')


@app.route('/server_wakeup', methods=['POST'])
@login_required
def server_wakeup():
    if request.method == 'POST':
        server_lists = request.form.getlist('server_list')
        print(server_lists)
        return str(server_lists)


@app.route('/csv_content', methods=['POST'])
@login_required
def csv_content():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    session.insert(1,f.filename)
    return render_template('csv_output.html')


@app.route('/content')
@login_required
def content():
    def inner():
        output = []
        # simulate a long process to watch
        while 'endofprogramcompletion' not in output:
           # yield '<b>The commands are being executed.</b><br/><br/>'
            output = CSV_LI_WINDOW.csv_file(session[1]).copy()
            print("printing output before yield:",output)
            yield '<h1 style="font-color: blue; font-size: 12px; font-weight: bold">  %s <br>  </h1> '% output
    return Response(inner(), mimetype='text/html')


    #return render_template('csv_output.html', word=inner())
    # def inner():
    #     output=[]
    #     print("Printing file name here:",f.filename)
    #     print("printing output before while:",output)
    #     while 'endofprogramcompletion' not in output:
    #        # yield '<b>The commands are being executed.</b><br/><br/>'
    #         output = CSV_LI_WINDOW.csv_file(f.filename).copy()
    #         print("printing output before yield:",output)
    #         yield '%s<br/>\n' % output
    #     return render_template('csv_output.html', data=inner())



# @app.route('/output')
# @login_required
# def output_data():
#     def inner():
#         output=[]
#
#         #output.copy()
#         yield '<h3>Home (<a href ="/">home</a>)</h3>'
#         while 'endofprogramcompletion' not in output:
#             yield '<b>The commands are being executed.</b><br/><br/>'
#             output = pywin.csv_file(uploaded_file).copy()
#             yield '%s<br/>\n' % output
#     return flask.Response(inner(), mimetype='text/html')


@app.route('/individual_output',methods=['POST'])
@login_required
def individual_output():
    ipadd = request.form.get('ipaddr')
    uname = request.form.get('uname')
    password = request.form.get('passwd')
    commands = request.form.get('commands')
    print("I am printing the ipadd for individual :",ipadd)
    output = CSV_LI_WINDOW.CreatePod(ipadd, uname, password, commands)
    return render_template('individual_output.html', len=len(output), data=output)

@app.route('/log_data')
@login_required
def log_data():
    return render_template('log_data.html')


#if __name__ == '__main__':
context = ('certificate.crt', 'privateKey.key')#certificate and key files
app.run(debug=True, ssl_context=context)