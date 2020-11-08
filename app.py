from flask import Flask, flash, render_template, request, redirect, jsonify, url_for

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/test", methods=["POST"])
def test():
    name_of_slider = request.form["name_of_slider"]
    return name_of_slider