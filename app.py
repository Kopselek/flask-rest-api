from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

sensors_cache = {}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    return redirect(url_for('sensor_list'))


@app.route('/sensors')
def sensor_list():
    # sensors = db.session.execute(db.select(Sensor).order_by(Sensor.id)).scalars()
    return "test", 200


@app.post('/sensor')
def sensor_post():
    sensors_cache.update(request.json)
    return '', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
