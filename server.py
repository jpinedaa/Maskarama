from flask import Flask, request, jsonify, Response
from simulation import Simulation
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/api/status', methods=['GET'])
def get_status():
    status = {}
    status['simulation_started'] = True
    status['currentEnvironment'] = sim.currentEnvironment
    status['perspective'] = sim.perspective

    return jsonify(status), 200


@app.route('/api/start', methods=['GET'])
def start_sim():
    no_turns = request.args.get('no_turns', default=1, type=int)

    return Response(sim.run(no_turns), mimetype='application/json')


@app.route('/api/narration', methods=['GET'])
def get_narration():
    return jsonify({"narration": sim.last_narration}), 200


@app.route('/api/user_input', methods=['POST'])
def submit_player_input():
    data = request.json
    user_input = data.get('input')
    result = sim.environments_dict[sim.currentEnvironment].process_user_input(user_input)
    return jsonify(result), 200


@app.route('/api/environments', methods=['GET'])
def get_environments():
    return jsonify({env: {"entities": [ent.name for ent in obj.entities.values()], "boundaries": obj.boundaries, "state": obj.state} for env, obj in sim.environments_dict.items()}), 200


@app.route('/api/entities', methods=['GET'])
def get_entities():
    return jsonify({ent: {"state": obj.state, "inputs": obj.inputs, "perception": obj.perception} for ent, obj in sim.entities_dict.items()}), 200


# Error handling for 404 (Not Found)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# Run the server
if __name__ == '__main__':
    global sim

    sim = Simulation()
    app.run(debug=True, host='0.0.0.0', port=5500)
