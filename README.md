
# Flask Learning Project

**flask-rest-api** is project for learning python, flask, pytest, postman.
Im building rest api based on [NBB REST API Design Guide](https://github.com/NationalBankBelgium/REST-API-Design-Guide)
## Installation
### docker

```bash
  docker compose up
```

### venv
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
## Unit Testing
The project also includes a set of unit tests that ensure the correctness of functions and endpoints. The tests are written using the pytest library:
```pytest
pytest
```
## Endpoints
- **GET** /sensors: Retrieves a list of all sensors.
- **POST** /sensors: Creates a new sensor based on the provided temperature.
- **GET** /sensor/<sensor_id>: Retrieves information about a specific sensor based on the ID.
- **PUT** /sensor/<sensor_id>: Updates the temperature of a specific sensor based on the ID.
- **DELETE** /sensor/<sensor_id>: Deletes a specific sensor based on the ID.
- **GET** /averageTemperature: Retrieves the average temperature from all sensors.