from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
from gevent.wsgi import WSGIServer
from detector import test_one
import requests
import urllib
from bs4 import BeautifulSoup
app= Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/',methods=['GET'])
@app.route('/test',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'])
@app.route('/test',methods=['POST'])
def download():
    if 'iurl' in request.form:
        url = request.form['iurl']
        pred = test_one(url)
        print (pred)
        if pred[0] == 1:
            result = "Malicious"
        else :
            result = "Benign"
        return render_template('result.html',url = url, result = result)
    else:
        return render_template('index.html')
@app.route('/train',methods=['GET'])
def download_private():
    return render_template('private.html')
if __name__=='__main__':
    #app.run(host='0.0.0.0',port=80,threaded=True)
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
