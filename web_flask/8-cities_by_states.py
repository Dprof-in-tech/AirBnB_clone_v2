#!/usr/bin/python3
"""Script that sets up a Flask web application,
fetching the data from MySQL database
"""
from flask import Flask
from flask import render_template
from models import storage
from models import HBNB_TYPE_STORAGE

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """Displays HTML page witha list of all state object in DBStorage
    Sorted by their names
    """
    states = storage.all('State')
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
