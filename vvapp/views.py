from vvapp import app
from flask import render_template, redirect, abort, url_for, json, request, send_from_directory, jsonify

import os, requests, time, pickle

from tf_model import do_inference

# index
@app.route('/')
@app.route('/index')
def end_index():
    #return "Hello, Voice Vector!"
    return render_template("index.html")


@app.route('/process')
def api_process():
    do_inference(