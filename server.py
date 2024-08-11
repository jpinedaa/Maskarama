import time
import uuid
from multiprocessing import Process, Queue, Event, Manager
from flask import Flask, request, jsonify, Response
from simulation_manager import simulation_process
from flask_cors import CORS
from utils import update_api_key
import logging


app = Flask(__name__)
CORS(app)


# Helper function to handle internal errors
def handle_internal_error(e):
    response = {
        "internal_error": "An unexpected error occurred.",
        "details": str(e)
    }
    return jsonify(response), 500


# Helper function to send commands to the simulation and wait for the correct response
def send_command(command, **kwargs):
    request_id = str(uuid.uuid4())
    command_queue.put({'command': command, 'id': request_id, **kwargs})

    while True:
        if request_id in response_dict:
            response = response_dict.pop(request_id)
            logging.debug(f"Send command response: {response}")
            if 'error' in response:
                raise Exception(response['error'])
            return response['result']


@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        status = send_command('status')
        return jsonify(status), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/start', methods=['GET'])
def start_sim():
    try:
        no_turns = request.args.get('no_turns', default=1, type=int)

        # Generator function to yield the results
        def generate():
            request_id = str(uuid.uuid4())
            command_queue.put({'command': 'run', 'id': request_id, 'no_turns': no_turns})

            while True:
                if request_id in response_dict:
                    response = response_dict.pop(request_id)
                    if 'error' in response:
                        yield f"ERROR: {response['error']}\n\n"
                        break
                    if response['result'] == 'Simulation run completed':
                        break
                    else:
                        yield f"{response['result']}\n\n"
                time.sleep(0.1)

        return Response(generate(), content_type='text/event-stream')
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/narration', methods=['GET'])
def get_narration():
    try:
        narration = send_command('narration')
        return jsonify(narration), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/last_narration', methods=['GET'])
def get_last_narration():
    try:
        last_narration = send_command('last_narration')
        return jsonify(last_narration), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/user_input', methods=['POST'])
def submit_player_input():
    try:
        data = request.json
        user_input = data.get('input')
        result = send_command('user_input', user_input=user_input)
        return jsonify(result), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/environments', methods=['GET'])
def get_environments():
    try:
        environments = send_command('environments')
        return jsonify(environments), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/entities', methods=['GET'])
def get_entities():
    try:
        entities = send_command('entities')
        return jsonify(entities), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/perspective', methods=['GET'])
def set_perspective():
    try:
        character = request.args.get('character', default=1, type=str)
        if character == 1:
            return jsonify({"msg": "Missing character in request"}), 200
        resp = send_command('perspective', character_name=character)
        return jsonify(resp), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/reset', methods=['GET'])
def reset_simulation():
    try:
        result = send_command('reset')
        return jsonify(result), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/api_key', methods=['POST'])
def set_api_key():
    try:
        key = request.json.get('key')
        update_api_key(key)
        send_command('restart_process')
        return jsonify({"msg": "api key updated"}), 200
    except Exception as e:
        return handle_internal_error(e)


# Error handling for 404 (Not Found)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="Resource not found"), 404


# Run the server
if __name__ == '__main__':
    global command_queue, response_dict, shutdown_event

    # Command Queue
    command_queue = Queue()
    shutdown_event = Event()

    # Create a manager for shared data structures
    manager = Manager()
    response_dict = manager.dict()  # Shared dictionary to store responses

    simulation_proc = Process(target=simulation_process, args=(command_queue, response_dict, shutdown_event))
    simulation_proc.start()

    try:
        app.run(debug=False, host='0.0.0.0', port=5500)
    finally:
        shutdown_event.set()
        simulation_proc.join()
