import json
import os
from agents import AgentState, InputAgentState
from utils import base_dir
import memory as mem
from memory import MEMORY_MAP, load_graph, query_prompt
from graphs import (entity_update_graph, perception_update_graph, currentOutput_graph,
                    environment_update_graph, entities_update_graph,
                    generate_currentoutput_graph, inputs_update_graph,
                    narrative_generation_graph, get_user_input_graph)


def run_update_module(graph, input_msg, name, agent_class=None):
    if agent_class is None:
        agent_class = AgentState
    initial_state = agent_class()
    initial_state["messages"] = [input_msg]

    events = graph.stream(initial_state, {"recursion_limit": 15})
    final_state = None
    print(f"Running {name} module")
    print(
        "--------------------------------------------------------------------")
    for s in events:
        final_state = s
        #print(s)
        #print("----")

    return final_state["Output"]["output"]


class Entity:
    def __init__(self, state, inputs, currentOutput, name, perception=None):
        self.state = state
        self.inputs = inputs
        self.currentOutput = currentOutput
        self.name = name
        self.perception = perception

    def update(self):
        self.update_state()
        if self.perception:
            self.update_character()
        self.generate_current_output()

    def update_state(self):
        output = run_update_module(entity_update_graph, f"State: {self.state}\nInputs: {self.inputs}\n", "Update Entity State")
        self.state = output["updated_state"]

    def update_character(self):
        query = query_prompt.replace("PERCEPTION", self.perception)

        memory = None
        if self.name in MEMORY_MAP:
            if mem.query_engine is None:
                mem.query_engine = load_graph(MEMORY_MAP[self.name])[1]
            memory = mem.query_engine.query(query)
        self.update_perception(memory)

    def update_perception(self, memory):
        output = run_update_module(perception_update_graph, f"Perception: {self.perception}\nState: {self.state}\nInputs: {self.inputs}\nMemory: {memory}\n", "Update Perception")
        self.perception = output["updated_perception"]

    def generate_current_output(self):
        input_msg = f"State: {self.state}\nInputs: {self.inputs}\n"
        if self.perception:
            input_msg += f"Percetion: {self.perception}\n"
        output = run_update_module(currentOutput_graph, input_msg, "Generate Current Output")
        self.currentOutput = output["currentOutput"]


class Environment:
    def __init__(self, boundaries, state, entities, name):
        self.boundaries = boundaries
        self.state = state
        self.entities = entities
        self.name = name
        self.narrative = ""
        self.exit_entities = {}

    def run_simulation(self, no_turns=None, shared_dict=None):
        while True:
            if shared_dict['perspective'] in self.entities:
                shared_dict['currentEnvironment'] = self.name
            if no_turns is not None and int(no_turns) <= 0:
                break
            self.update()
            if shared_dict['perspective'] in self.entities:
                self.generate_narrative(shared_dict["perspective"], shared_dict)
            self.update_entity_inputs()
            if shared_dict:
                coming_entities = shared_dict.get(self.name)
                if coming_entities:
                    for entity in coming_entities:
                        if entity not in self.entities.values():
                            self.entities[entity.name] = entity
                if len(self.exit_entities) > 0:
                    for exiting_entity in self.exit_entities:
                        if exiting_entity in self.entities:
                            shared_dict[self.exit_entities[exiting_entity]].append(self.entities[exiting_entity])
                            self.entities.remove(exiting_entity)
                            break
            print(
                "--------------------------------------------------------------------")
            print("Turn Ended")
            print(
                "--------------------------------------------------------------------")
            if no_turns is not None:
                no_turns -= 1


    def update(self):
        #for entity in self.entities:
        #    entity.update()
        self.update_all_entities_states()
        for entity_name, entity in self.entities.items():
            if entity.perception:
                entity.update_character()
        self.update_all_entities_currentOutputs()
        self.update_state()

    def update_all_entities_states(self):
        input_msg = {entity_name: {"state": entity.state, "inputs": entity.inputs} for entity_name, entity in self.entities.items()}
        output = run_update_module(entities_update_graph, f"Entities: {input_msg}", "Update All Entities States")
        for entity_name, entity in self.entities.items():
            entity.state = output[entity_name]

    def update_all_entities_currentOutputs(self):
        input_msg = {}
        for entity_name, entity in self.entities.items():
            input_msg[entity_name] = {"state": entity.state, "inputs": entity.inputs}
            if entity.perception:
                input_msg[entity_name]["perception"] = entity.perception
        output = run_update_module(generate_currentoutput_graph, f"Entities: {input_msg}", "Update All Entities Current Outputs")
        for entity_name, entity in self.entities.items():
            entity.currentOutput = output[entity_name]

    def set_environment_fields(self, output):
        if len(self.exit_entities) > 0:
            self.entities = {entity_name: entity for entity_name, entity in self.entities.items() if entity_name not in self.exit_entities}
        self.state = output["state"]
        self.boundaries = output["boundaries"]
        self.exit_entities = output["exit_entities"]

    def update_state(self):
        input_msg = (f"Boudaries: {self.boundaries}\nState: {self.state}\nExit Entities: {self.exit_entities}\n" +
                     f"Entities current outputs: {[f'{entity_name}: {entity.currentOutput}' for entity_name, entity in self.entities.items()]}\n")
        output = run_update_module(environment_update_graph, input_msg, "Update Environment State")
        self.set_environment_fields(output)

    def update_entity_inputs(self):
        input_msg = f"State: {self.state}\nBoundaries: {self.boundaries}\n"
        output = run_update_module(inputs_update_graph, input_msg, "Update Entity Inputs")
        for entity_name, entity in self.entities.items():
            entity.inputs = output[entity_name]

    def generate_narrative(self, perspective, shared_dict=None):
        output = run_update_module(narrative_generation_graph, f"State: {self.state}\nPerception: "
                                                                    f"{perspective}- {self.entities[perspective].perception}\n"
                                                                    f"Previous Narrative: {self.narrative}\n", "Generate Narrative")
        self.narrative += output["narrative"]
        if shared_dict:
            shared_dict["narrative"] = output["narrative"]

    def process_user_input(self, user_input):
        input_msg = f'User Input: {user_input}, Environment Object: Boudaries: {self.boundaries}\nState: {self.state}\nExit Entities: {self.exit_entities}\n'
        output = run_update_module(get_user_input_graph, input_msg, "Get User Input", InputAgentState)
        return_dict = {}
        if "environment" in output:
            self.set_environment_fields(output["environment"])
            return_dict["approved"] = True
        else:
            return_dict["approved"] = False
        return_dict["feedback"] = output["feedback"]
        return return_dict


if __name__ == "__main__":
    try:
        ans = input("Turn on loop? (y/n): ")
        if ans.lower() == "y":
            loop = True
            print("Loop turned on")
        else:
            loop = False
            print("Loop turned off")
        with open(os.path.join(base_dir, "example_environment.json"), "r", encoding='utf-8') as f:
            example = json.load(f)
        example_state = {}
        entities = {}
        for entity in example["entities"]:
            ent = Entity(example["entities"][entity]["state"], example["entities"][entity]["new_inputs"], '', entity, example["entities"][entity].get("perception", None))
            example_state[ent.name] = example["environment"]["state"]["EntitySpecificStates"][entity]
            entities[entity] = ent
        example_state["OverallState"] = example["environment"]["state"]["OverallState"]
        example_env = Environment(example["environment"]["boundaries"], example_state, entities, example["environment"]["name"])
        if loop:
            example_env.run_simulation(None)
        else:
            example_env.run_simulation(1)

    except Exception as e:
        input(f"An error occurred: {e}")
    finally:
        input("Press enter to exit")