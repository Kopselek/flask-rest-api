from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse

sensors_cache = {}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
api = Api(app)


class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'temperature': self.temperature
        }


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('temperature', type=float, required=True)

with app.app_context():
    db.create_all()


class Sensors(Resource):
    def get(self):
        sensors = Sensor.query.order_by(Sensor.id).all()
        return jsonify([Sensor.serialize(sensor) for sensor in sensors])

    def post(self):
        args = parser.parse_args()
        sensor = Sensor(temperature=args['temperature'])
        db.session.add(sensor)
        db.session.commit()
        return Sensor.serialize(sensor), 201


class SingleSensor(Resource):
    def get(self, sensor_id):
        sensor = Sensor.query.filter_by(id=sensor_id).first()
        return Sensor.serialize(sensor)

    def delete(self, sensor_id):
        sensor = Sensor.query.filter_by(id=sensor_id).first()
        db.session.delete(sensor)
        db.session.commit()
        return '', 204

    def put(self, sensor_id):
        sensor = Sensor.query.filter_by(id=sensor_id).first()
        args = parser.parse_args()
        sensor.temperature = args['temperature']
        db.session.commit()
        return Sensor.serialize(sensor), 201


class AverageTemperature(Resource):
    def get(self):
        sensors = Sensor.query.order_by(Sensor.id).all()
        sensors_sum = 0
        sensors_temperature_sum = 0
        for sensor in sensors:
            sensors_sum += 1
            sensors_temperature_sum += sensor.temperature
        average_temperature = round(sensors_temperature_sum / sensors_sum, 2)
        return {"averageTemperature": average_temperature}


api.add_resource(Sensors, '/sensors')
api.add_resource(SingleSensor, '/sensor/<sensor_id>')
api.add_resource(AverageTemperature, '/averageTemperature')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
