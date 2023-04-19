from flask import Flask, jsonify, request

app = Flask(__name__)


sensors = [{}]


@app.route('/')
def index():
    return jsonify(sensors)


@app.post('/sensor')
def sensor_post():
    return ''
