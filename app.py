from flask import Flask, jsonify, request, redirect, url_for

sensors_cache = {}


def create_app():
    app = Flask(__name__)

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

    return app


if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0')
