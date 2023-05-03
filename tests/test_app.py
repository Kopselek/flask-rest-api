import json

data = {"0": {
    "temperature": "25"
}
}


def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert response.request.path == '/sensors'
    assert len(response.history) == 1
    assert response.status_code == 200


def test_sensors_list(client):
    response = client.get('/sensors')
    res = json.loads(response.data)

    assert type(res) is dict
    assert response.status_code == 200


def test_sensor_post(client):
    response = client.post('/sensor', json=data)
    assert response.status_code == 200
