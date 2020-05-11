
from app.application.get_events import GetEventsQuery
from app.application.persist_event import PersistEventCommand
from app.application.persist_inventory import PersistInventoryCommand
from app.infrastructure.boot import Boot
from flask import Flask, jsonify, request, render_template
from uuid import uuid4

import logging

boot = Boot()
boot.start()
injector = boot.injector
app = Flask(__name__, template_folder='infrastructure/flask/templates')


@app.route('/')
def index():
    handler = injector.get_service('app.application.query.get_events').instance
    return render_template('index.html', events=handler.handle(GetEventsQuery()))


@app.route('/event')
def get_events():
    logging.debug('GET all events')
    handler = injector.get_service('app.application.query.get_events').instance
    result = handler.handle(GetEventsQuery())
    return jsonify(result)


@app.route('/event/<identifier>')
def get_event(identifier):
    logging.debug('GET event with ID')
    handler = injector.get_service('app.application.query.get_events').instance
    result = handler.handle(GetEventsQuery(identifier))
    return jsonify(result)


@app.route('/event', methods=['POST', 'PATCH'])
def post_event():
    logging.debug('POST new event')
    if request.form['name'] is None:
        logging.debug('POST failed: no name was attached')
        return jsonify({'response': 'failed', 'reason': 'no name was attached'})
    handler = injector.get_service(
        'app.application.command.persist_event'
    ).instance
    handler.handle(
        PersistEventCommand(
            uuid4(),
            request.form['name']
        )
    )
    return jsonify({'response': 'done'})


@app.route('/inventory', methods=['POST'])
def post_inventory():
    logging.debug('POST new inventory')
    if not __is_valid_inventory_request(request.form):
        logging.debug('POST failed: field missing')
        return jsonify({'response': 'failed', 'reason': 'field missing'})
    handler = injector.get_service(
        'app.application.inventory.persist_inventory'
    ).instance
    handler.handle(
        PersistInventoryCommand(
            uuid4(),
            request.form['event_id'],
            request.form['amount'],
            request.form['seller_name']
        )
    )
    return jsonify({'response': 'done'})


def __is_valid_inventory_request(body):
    logging.debug('Fields attached to the request: {0}'.format(body))
    REQUIRED_FIELDS = ['event_id', 'amount', 'seller_name']
    for field in REQUIRED_FIELDS:
        if field not in body:
            return False
    return True
