from flask import Flask, flash, render_template, request, redirect, jsonify, url_for

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', move_people_value=0)

@app.route("/test", methods=["POST"])
def test():
    move_people_value = request.form["move_people_slider_name"]
    print(move_people_value)
    return render_template('index.html', move_people_value=move_people_value)

@app.route("/test2", methods=["POST"])
def test2():
    # print(request.args)
    # move_people_value = request.args.get('move_people_value')

    move_people_value = request.form["move_people_slider_name"]
    print(move_people_value)
    return move_people_value
    # return render_template('index.html', move_people_value=move_people_value)