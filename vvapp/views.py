from vvapp import app
from flask import render_template, redirect, abort, url_for, json, request, send_from_directory, jsonify

import os, requests, time, pickle

# index
@app.route('/')
@app.route('/index')
def end_index():
    return "Hello, Voice Vector!"
