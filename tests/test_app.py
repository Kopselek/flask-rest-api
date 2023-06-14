import pytest
from flask.testing import FlaskClient
from app import app, db, Sensor


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_get_all_sensors(client: FlaskClient):
    with app.app_context():
        sensor1 = Sensor(temperature=20.5)
        sensor2 = Sensor(temperature=22.8)
        db.session.add(sensor1)
        db.session.add(sensor2)
        db.session.commit()

        response = client.get('/sensors')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['temperature'] == 20.5
        assert data[1]['temperature'] == 22.8


def test_create_sensor(client: FlaskClient):
    with app.app_context():
        response = client.post('/sensors', json={'temperature': 25.3})

        assert response.status_code == 201
        data = response.get_json()
        assert data['temperature'] == 25.3

        sensor = Sensor.query.first()
        assert sensor is not None
        assert sensor.temperature == 25.3


def test_get_single_sensor(client: FlaskClient):
    with app.app_context():
        sensor = Sensor(temperature=18.9)
        db.session.add(sensor)
        db.session.commit()

        response = client.get(f'/sensor/{sensor.id}')

        assert response.status_code == 200
        data = response.get_json()
        assert data['temperature'] == 18.9


def test_delete_sensor(client: FlaskClient):
    with app.app_context():
        sensor = Sensor(temperature=21.7)
        db.session.add(sensor)
        db.session.commit()

        response = client.delete(f'/sensor/{sensor.id}')

        assert response.status_code == 204

        deleted_sensor = db.session.get(Sensor, sensor.id)
        assert response.status_code == 204
        assert deleted_sensor is None


def test_update_sensor(client: FlaskClient):
    with app.app_context():
        sensor = Sensor(temperature=23.6)
        db.session.add(sensor)
        db.session.commit()

        response = client.put(f'/sensor/{sensor.id}', json={'temperature': 26.9})

        assert response.status_code == 201
        data = response.get_json()
        assert data['temperature'] == 26.9

        updated_sensor = db.session.merge(sensor)
        assert updated_sensor.temperature == 26.9


def test_get_average_temperature(client: FlaskClient):
    with app.app_context():
        sensor1 = Sensor(temperature=19.5)
        sensor2 = Sensor(temperature=20.5)
        sensor3 = Sensor(temperature=22.5)
        db.session.add(sensor1)
        db.session.add(sensor2)
        db.session.add(sensor3)
        db.session.commit()

        response = client.get('/averageTemperature')

        assert response.status_code == 200
        data = response.get_json()
        assert 'averageTemperature' in data
        assert data['averageTemperature'] == pytest.approx(20.83, 0.01)
