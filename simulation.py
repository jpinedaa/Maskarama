import json
import multiprocessing
from simulation_utils import Entity, Environment


class Simulation:
    def __init__(self):
        with open('initial_states/environments.txt', 'r') as file:
            env_json = json.load(file)
        with open('initial_states/entities.txt', 'r') as file:
            entities_json = json.load(file)

        self.entities_dict = {}
        for entity in entities_json:
            self.entities_dict[entity] = Entity(entities_json[entity]["state"], entities_json[entity]["new_inputs"], '', entity, entities_json[entity].get("perception", None))

        self.environments_dict = {}
        for env in env_json:
            ents = {}
            for ent in env_json[env]["entities"]:
                ents[ent] = self.entities_dict[ent]
            self.environments_dict[env] = Environment(env_json[env]["boundaries"], env_json[env]["state"], ents, env)

        self.perspective = self.entities_dict["hermes01"].name
        self.currentEnvironment = self.environments_dict["hallsOfJudgment01"].name
        self.narrative = ""


    def run(self, no_turns=1):
        with multiprocessing.Manager() as manager:
            shared_dict = manager.dict()
            shared_dict['perspective'] = self.perspective
            shared_dict['narrative'] = ""
            env_processes = []
            for env in self.environments_dict:
                proc = multiprocessing.Process(target=self.environments_dict[env].run_simulation, kwargs={'no_turns': no_turns, 'shared_dict': shared_dict})
                env_processes.append(proc)
                proc.start()

            for proc in env_processes:
                proc.join()

            if 'currentEnvironment' in shared_dict:
                self.currentEnvironment = shared_dict['currentEnvironment']

            self.narrative = shared_dict['narrative']


if __name__ == '__main__':
    sim = Simulation()
    sim.run()

