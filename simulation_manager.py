import multiprocessing
import time
from queue import Empty
from simulation import Simulation
import logging


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def handle_command(command_data, response_dict, sim):
    command = command_data['command']
    request_id = command_data['id']
    try:
        if command == 'status':
            response = {
                'currentEnvironment': sim.currentEnvironment,
                'perspective': sim.perspective
            }
        elif command == 'run':
            # Stream results
            for result in sim.run(command_data['no_turns']):
                response_dict[request_id] = {'result': result}
                logging.info(f"Turn completed in simulation manager, result: {result}")
                max_wait_time = 5
                interval = 0.1
                while request_id in response_dict:
                    max_wait_time -= interval
                    if max_wait_time <= 0:
                        logging.error("Timeout waiting for response")
                        break
                    time.sleep(0.1)
            response = 'Simulation run completed'
        elif command == 'narration':
            response = {"narration": sim.narration}
        elif command == 'last_narration':
            response = {"last_narration": sim.last_narration}
        elif command == 'user_input':
            response = sim.environments_dict[sim.currentEnvironment].process_user_input(
                command_data['user_input'])
        elif command == 'environments':
            response = {
                env: {
                    "entities": [ent.name for ent in obj.entities.values()],
                    "boundaries": obj.boundaries,
                    "state": obj.state
                }
                for env, obj in sim.environments_dict.items()
            }
        elif command == 'entities':
            response = {
                ent: {
                    "state": obj.state,
                    "inputs": obj.inputs,
                    "perception": obj.perception
                }
                for ent, obj in sim.entities_dict.items()
            }
        elif command == 'reset':
            sim.reset()
            response = {"msg": "reset successful"}
        elif command == 'perspective':
            sim.perspective = command_data['character']
            response = {"msg": f"perspective set to {sim.perspective}"}
        else:
            response = {"error": "Unknown command"}
            logging.error(f"Unknown command {command}")
        response_dict[request_id] = {'result': response}
        logging.debug(f"Command {command} completed")
    except Exception as e:
        logging.error(f"Error handling command {command}: {e}")
        response_dict[request_id] = {'error': str(e)}


def simulation_process(command_queue, response_dict, shutdown_event):
    logging.info("Simulation process started")
    sim = Simulation()
    monitor_process = multiprocessing.Process(target=monitor_event_state, args=(sim.turn_events, sim.start_events, sim.end_events, sim.shared_dict))
    monitor_process.start()
    while not shutdown_event.is_set():
        try:
            command_data = command_queue.get(timeout=1)  # Wait for a command
            handle_command(command_data, response_dict, sim)
        except Empty:
            continue

    logging.info("Simulation process stopped")


def monitor_event_state(turn_events, start_events, end_events, shared_dict):
    while True:
        for env_name, event in turn_events.items():
            logging.debug(f"Turn event {env_name}: {event.is_set()}")
        for env_name, event in start_events.items():
            logging.debug(f"Start event {env_name}: {event.is_set()}")
        for env_name, event in end_events.items():
            logging.debug(f"End event {env_name}: {event.is_set()}")
        for key, value in shared_dict.items():
            logging.debug(f"{key}: {value}")
            if isinstance(value, dict):
                for k, v in value.items():
                    logging.debug(f"    {k}: {v}")
        time.sleep(5)