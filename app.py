from flask import Flask, jsonify, request, redirect, url_for


def create_app():
    _app = Flask(__name__)
    return _app


app = create_app()

sensors_cache = {}


@app.route('/')
def index():
    return redirect(url_for('sensors_list'))


@app.route('/sensors')
def sensors_list():
    return jsonify(sensors_cache), 200


@app.post('/sensor')
def sensor_post():
    sensors_cache.update(request.json)
    return '', 200
