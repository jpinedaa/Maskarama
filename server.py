from flask import Flask, request, jsonify, Response
from simulation import Simulation
from flask_cors import CORS
from utils import update_api_key


app = Flask(__name__)
CORS(app)


# Helper function to handle internal errors
def handle_internal_error(e):
    response = {
        "internal_error": "An unexpected error occurred.",
        "details": str(e)
    }
    return jsonify(response), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        status = {}
        status['simulation_started'] = True
        status['currentEnvironment'] = sim.currentEnvironment
        status['perspective'] = sim.perspective
        return jsonify(status), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/start', methods=['GET'])
def start_sim():
    try:
        no_turns = request.args.get('no_turns', default=1, type=int)
        return Response(sim.run(no_turns))
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/narration', methods=['GET'])
def get_narration():
    try:
        return jsonify({"narration": sim.last_narration}), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/user_input', methods=['POST'])
def submit_player_input():
    try:
        data = request.json
        user_input = data.get('input')
        result = sim.environments_dict[sim.currentEnvironment].process_user_input(user_input)
        return jsonify(result), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/environments', methods=['GET'])
def get_environments():
    try:
        environments = {
            env: {
                "entities": [ent.name for ent in obj.entities.values()],
                "boundaries": obj.boundaries,
                "state": obj.state
            }
            for env, obj in sim.environments_dict.items()
        }
        return jsonify(environments), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/entities', methods=['GET'])
def get_entities():
    try:
        entities = {
            ent: {
                "state": obj.state,
                "inputs": obj.inputs,
                "perception": obj.perception
            }
            for ent, obj in sim.entities_dict.items()
        }
        return jsonify(entities), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/reset', methods=['GET'])
def reset_simulation():
    try:
        sim.reset()
        return jsonify({"msg": "reset successful"}), 200
    except Exception as e:
        return handle_internal_error(e)


@app.route('/api/api_key', methods=['POST'])
def get_api_key():
    try:
        key = request.json.get('key')
        update_api_key(key)
    except Exception as e:
        return handle_internal_error(e)


# Error handling for 404 (Not Found)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="Resource not found"), 404


# Run the server
if __name__ == '__main__':
    global sim

    sim = Simulation()
    app.run(debug=True, host='0.0.0.0', port=5500)
