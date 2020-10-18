from flask import Flask, render_template, url_for, request
from mainapp import *
import json
#import requests

app = Flask(__name__)

@app.route('/')
def hello():
    #return 'Hello World!'
    return render_template('index.html')

@app.route('/api', methods=['GET', 'POST'])
def api_ciscointcfg():
    #dataquery = request.args
    data = request.get_json()
    
    #print(dataquery, data, request.get_data())

    return in_json_trigger(injson=data)
    #return in_json_trigger(injson=json.dumps(data))
    #return in_json_trigger(injson=data)

if __name__ == '__main__':
    app.run(debug=True)