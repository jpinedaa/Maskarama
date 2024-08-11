import json
import multiprocessing
import os.path
import logging
import traceback
from simulation_utils import Entity, Environment
from utils import base_dir


class Simulation:
    def __init__(self):
        self.entities_dict = {}
        self.environments_dict = {}
        self.perspective = None
        self.currentEnvironment = None
        self.last_narration = ""
        self.narration = []
        self.shared_dict = None
        self.is_running = False

        self.load_state()
        self.start_events = {}
        self.turn_events = {}
        self.end_events = {}
        self.processes = {}

        # Initialize multiprocessing.Manager
        manager = multiprocessing.Manager()
        self.shared_dict = manager.dict()
        self.shared_dict['perspective'] = self.perspective
        self.shared_dict['narrative'] = self.last_narration
        self.shared_dict['results'] = manager.dict()

        # Initialize events and processes
        for env_name, env in self.environments_dict.items():
            logging.info(f"Initializing environment process: {env_name}")
            self.start_events[env_name] = multiprocessing.Event()
            self.turn_events[env_name] = multiprocessing.Event()
            self.end_events[env_name] = multiprocessing.Event()
            self.start_worker_process(env_name, env)

    def start_worker_process(self, env_name, env):
        proc = multiprocessing.Process(
            target=run_environment_simulation,
            args=(env_name, env, self.start_events[env_name], self.turn_events[env_name], self.end_events[env_name], self.shared_dict)
        )
        self.processes[env_name] = proc
        proc.start()
        logging.info(f"Started environment process: {env_name}")

    def run(self, no_turns=1):
        if self.is_running:
            return "Simulation is already running."
        self.is_running = True
        self.shared_dict['no_turns'] = no_turns
        self.shared_dict['current_turn'] = 0

        # Signal all processes to start the simulation
        for start_event in self.start_events.values():
            start_event.set()

        for turn in range(no_turns):
            logging.info(f"Starting turn {turn + 1}")

            # Wait for current environments to complete the current turn
            self.wait_event(self.currentEnvironment)

            # Gather results from the shared dictionary
            if 'currentEnvironment' in self.shared_dict:
                self.currentEnvironment = self.shared_dict['currentEnvironment']

            self.last_narration = self.shared_dict['narrative']
            self.narration.append(self.last_narration)

            logging.info(f"yielding narration")
            yield self.last_narration + '\n'
            logging.info(f"yielded narration: {self.last_narration}")

            # Wait for all environments to complete the current turn
            for env_name in self.environments_dict:
                if env_name == self.currentEnvironment:
                    continue
                self.wait_event(env_name)
            # Clear the turn events and signal to start the next turn
            for turn_event in self.turn_events.values():
                turn_event.clear()
            for start_event in self.start_events.values():
                start_event.set()

            # Update environments_dict and entities_dict with the results
            for env_name, result in self.shared_dict['results'].items():
                self.environments_dict[env_name].update_object(result['environment'],
                                                               result['entities'])
                for entity_name, entity_data in result['entities'].items():
                    self.entities_dict[entity_name].update_object(entity_data)

            self.shared_dict['current_turn'] += 1

        # Wait for all processes to signal that the simulation has ended
        for end_event in self.end_events.values():
            end_event.wait()
        # Clear the end events
        for end_event in self.end_events.values():
            end_event.clear()

        self.save_state()
        self.is_running = False
        yield f"Simulation completed after {no_turns} turns."

    def wait_event(self, env):
        timeout = 10

        while True:
            # Wait with a timeout
            event_triggered = self.turn_events[env].wait(timeout)

            if event_triggered:
                # Check if errors occurred during the turn
                logging.info(f"Environment {env} Event triggered")
                if f'{env}-error' in self.shared_dict:
                    logging.error(f"Error occurred in environment {env}: {self.shared_dict[f'{env}-error']}")
                    del self.shared_dict[f'{env}-error']
                    self.turn_events[env].clear()
                    self.start_events[env].set()  # Signal the process to start
                else:
                    break  # Event was successfully triggered, exit the loop

            # Check if the process is still alive after the timeout
            if not self.processes[env].is_alive():
                logging.error(
                    f"Process for environment {env} has died unexpectedly during wait.")
                self.turn_events[env].clear()  # Clear any potentially stale events
                self.start_events[env].set()  # Signal the process to start
                self.restart_process(env)
                continue  # Restart the loop to check the next process

    def restart_process(self, env_name):
        logging.info(f"Restarting environment process: {env_name}")
        self.processes[env_name].terminate()
        self.start_worker_process(env_name, self.environments_dict[env_name])

    def save_state(self):
        with open(os.path.join(base_dir, 'state/entities.txt'), 'w') as file:
            json.dump({entity: {"state": obj.state, "new_inputs": obj.inputs, "perception": obj.perception} for entity, obj in self.entities_dict.items()}, file, indent=4)

        with open(os.path.join(base_dir, 'state/environments.txt'), 'w') as file:
            json.dump({env: {"boundaries": obj.boundaries, "state": obj.state, "entities": [ent.name for ent in obj.entities.values()]} for env, obj in self.environments_dict.items()}, file, indent=4)

        with open(os.path.join(base_dir, 'state/status.txt'), 'w') as file:
            json.dump({"perspective": self.perspective, "currentEnvironment": self.currentEnvironment, "narration": self.narration}, file, indent=4)

    def load_state(self):
        if os.path.exists(os.path.join(base_dir, 'state/entities.txt')):
            ent_file = os.path.join(base_dir, 'state/entities.txt')
        else:
            ent_file = os.path.join(base_dir, 'initial_states/entities.txt')
        if os.path.exists(os.path.join(base_dir, 'state/environments.txt')):
            env_file = os.path.join(base_dir, 'state/environments.txt')
        else:
            env_file = os.path.join(base_dir, 'initial_states/environments.txt')
        if os.path.exists(os.path.join(base_dir, 'state/status.txt')):
            status_file = os.path.join(base_dir, 'state/status.txt')
        else:
            status_file = os.path.join(base_dir, 'initial_states/status.txt')

        with open(env_file, 'r') as file:
            env_json = json.load(file)
        with open(ent_file, 'r') as file:
            entities_json = json.load(file)
        with open(status_file, 'r') as file:
            status_json = json.load(file)

        for entity in entities_json:
            self.entities_dict[entity] = Entity(entities_json[entity]["state"], entities_json[entity]["new_inputs"], '', entity, entities_json[entity].get("perception", None))

        for env in env_json:
            ents = {}
            for ent in env_json[env]["entities"]:
                ents[ent] = self.entities_dict[ent]
            self.environments_dict[env] = Environment(env_json[env]["boundaries"], env_json[env]["state"], ents, env)

        self.perspective = status_json["perspective"]
        self.currentEnvironment = status_json["currentEnvironment"]
        self.narration = status_json["narration"]
        self.last_narration = self.narration[-1] if len(self.narration) > 0 else ""

    def reset_state(self):
        if os.path.exists('state/entities.txt'):
            os.remove('state/entities.txt')
        if os.path.exists('state/environments.txt'):
            os.remove('state/environments.txt')
        if os.path.exists('state/status.txt'):
            os.remove('state/status.txt')

    def reset(self):
        self.reset_state()
        for proc in self.processes.values():
            proc.terminate()
        self.__init__()


def run_environment_simulation(env_name, env, start_event, turn_event, end_event, shared_dict):
    while True:
        try:
            # Wait for the start signal
            logging.info(f"Environment {env_name} waiting for start signal")
            start_event.wait()
            start_event.clear()

            # Run the simulation for the specified number of turns
            for _ in range(shared_dict['current_turn'], shared_dict['no_turns']):

                # Check if we should stop early
                if end_event.is_set():
                    logging.info(f"Environment {env_name} received stop signal")
                    break

                # Perform the simulation for one turn
                logging.info(f"Environment {env_name} running turn")
                env_result, entities_result = env.run_simulation(no_turns=1, shared_dict=shared_dict)

                # Store the results in the shared_dict
                shared_dict['results'][env_name] = {'environment': env_result,
                                                    'entities': entities_result}

                # Signal that the turn has completed
                turn_event.set()

                # Wait until the main process acknowledges the turn completion
                logging.info(f"Environment {env_name} waiting for next turn")
                start_event.wait()
                start_event.clear()
                logging.info(f"Environment {env_name} completed turn")

            # Signal that the simulation has ended
            end_event.set()

        except Exception as e:
            logging.error(f"Exception in environment {env_name}, traceback: {traceback.format_exc()}")
            shared_dict[f'{env_name}-error'] = f"Exception in environment {env_name}: {str(e)}"
            turn_event.set()  # Ensure the main process knows this turn is done to prevent deadlocks

if __name__ == '__main__':
    sim = Simulation()
    sim.run()
