from flask import Flask, request, jsonify
from simulation import Simulation
from typing import Optional


app = Flask(__name__)
sim: Optional[Simulation] = None


@app.route('/api/status', methods=['GET'])
def get_status():
    status = {}
    if sim:
        status['simulation_started'] = True
        status['currentEnvironment'] = sim.currentEnvironment
        status['perspective'] = sim.perspective
    else:
        status['simulation_started'] = False

    return jsonify(status), 200


@app.route('/api/start', methods=['GET'])
def start_sim():
    global sim
    if sim is None:
        sim = Simulation()
    no_turns = request.args.get('no_turns', default=1, type=int)
    sim.run(no_turns)

    return jsonify({"message": f'{no_turns} turn(s) simulated successfully'}), 200


@app.route('/api/narration', methods=['GET'])
def get_narration():
    if sim:
        return jsonify({"narration": sim.environments_dict[sim.currentEnvironment].narrative}), 200
    return jsonify({"error": "Simulation not started"}), 400


@app.route('/api/user_input', methods=['POST'])
def submit_player_input():
    if sim:
        data = request.json
        user_input = data.get('input')
        result = sim.environments_dict[sim.currentEnvironment].process_user_input(user_input)
        return jsonify(result), 200
    return jsonify({"error": "Simulation not started"}), 400


@app.route('/api/environments', methods=['GET'])
def get_environments():
    if sim:
        return jsonify({env: {"entities": [ent.name for ent in obj.entities.values()], "boundaries": obj.boundaries, "state": obj.state} for env, obj in sim.environments_dict.items()}), 200
    return jsonify({"error": "Simulation not started"}), 400


@app.route('/api/entities', methods=['GET'])
def get_entities():
    if sim:
        return jsonify({ent: {"state": obj.state, "inputs": obj.inputs, "perception": obj.perception} for ent, obj in sim.entities_dict.items()}), 200
    return jsonify({"error": "Simulation not started"}), 400


# Error handling for 404 (Not Found)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# Run the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
