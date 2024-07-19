import functools
import json
import os
from agents import create_agent, AgentState
from nodes import update_entity_node, output_json_node
from utils import base_dir, get_json_schema_prompt, get_model, build_graph


llm = get_model()
llm_json = get_model(json_output=True)


def build_update_graph(prompt_file, schema_dict):
    with open(os.path.join(base_dir, f"prompts/{prompt_file}"), "r", encoding='utf-8') as f:
        update_prompt = f.read()

    json_schema_prompt = get_json_schema_prompt(schema_dict)

    agent = create_agent(llm, update_prompt)
    node = functools.partial(update_entity_node, agent=agent)

    json_agent = create_agent(llm_json, json_schema_prompt)
    json_node = functools.partial(output_json_node, agent=json_agent)

    nodes = [("Update", node), ("Output", json_node)]
    edges = [("Update", lambda s: "continue", {"continue": "Output"}),
             ("Output", lambda s: "continue", {"continue": "__end__"})]
    state_class = AgentState
    entry_point = "Update"
    graph = build_graph(state_class, nodes, edges, entry_point)
    return graph


def run_update_module(graph, input_msg):
    initial_state = AgentState()
    initial_state["messages"] = [input_msg]

    events = graph.stream(initial_state, {"recursion_limit": 15})
    final_state = None
    for s in events:
        final_state = s
        print("Next Node")
        #print(s)
        #print("----")

    return final_state["Output"]["output"]


class Entity:
    def __init__(self, state, inputs, currentOutput, name, perception=None, memory=None):
        self.state = state
        self.inputs = inputs
        self.currentOutput = currentOutput
        self.name = name
        self.perception = perception
        self.memory = memory
        self.entity_update_graph = build_update_graph("entity_update.txt", {"updated_state": "str"})
        self.perception_update_graph = build_update_graph("perception_update.txt", {"updated_perception": "str"})
        self.currentOutput_graph = build_update_graph("currentOutput.txt", {"currentOutput": "str"})

    def update(self):
        self.update_state()
        if self.perception:
            self.update_character()
        self.generate_current_output()

    def update_state(self):
        output = run_update_module(self.entity_update_graph, f"State: {self.state}\nInputs: {self.inputs}\n")
        self.state = output["updated_state"]

    def update_character(self):
        self.update_perception()

    def update_perception(self):
        output = run_update_module(self.perception_update_graph, f"Perception: {self.perception}\nState: {self.state}\n")
        self.perception = output["updated_perception"]

    def generate_current_output(self):
        input_msg = f"State: {self.state}\nInputs: {self.inputs}\n"
        if self.perception:
            input_msg += f"Percetion: {self.perception}\n"
        output = run_update_module(self.currentOutput_graph, input_msg)
        self.currentOutput = output["currentOutput"]


class Environment:
    def __init__(self, boundaries, state, entities, perspective):
        self.boundaries = boundaries
        self.state = state
        self.entities = entities
        self.perspective = perspective
        self.narrative = ""
        self.exit_entities = []
        self.environment_update_graph = build_update_graph("environment_update.txt",
                                                {
                                                            "boundaries": [
                                                                {
                                                                    "ConnectedEnvironmentID": "str",
                                                                    "TransitionCondition": "str"
                                                                },
                                                                {
                                                                    "ConnectedEnvironmentID": "str",
                                                                    "TransitionCondition": "str"
                                                                },
                                                                {
                                                                    "ConnectedEnvironmentID": "str",
                                                                    "TransitionCondition": "str"
                                                                }
                                                            ],
                                                            "state": {
                                                                "OverallState": "str",
                                                                "EntitySpecificStates": {
                                                                    "entity1_name": "str",
                                                                    "entity2_name": "str",
                                                                    "entityN_name": "str"
                                                                }
                                                            },
                                                            "exit_entities": ["entity1_name", "entity2_name", "entityN_name"]
                                                            })
        self.narrative_generation_graph = build_update_graph("narrative_generation.txt", {"narrative": "str"})

    def run_simulation(self):
        while True:
            self.update()
            self.generate_narrative()

    def update(self):
        for entity in self.entities:
            entity.update()
        self.update_state()

    def update_state(self):
        input_msg = (f"Boudaries: {self.boundaries}\nState: {self.state}\nExit Entities: {self.exit_entities}\n" +
                     f"Entities current outputs: {[f'{entity.name}: {entity.currentOutput}' for entity in self.entities]}\n")
        output = run_update_module(self.environment_update_graph, input_msg)
        if len(self.exit_entities) > 0:
            self.entities = [entity for entity in self.entities if entity.name not in self.exit_entities]
        self.state = output["state"]
        self.boundaries = output["boundaries"]
        self.exit_entities = output["exit_entities"]

    def generate_narrative(self):
        output = run_update_module(self.narrative_generation_graph, f"State: {self.state}\nPerception: "
                                                                    f"{self.perspective.name}- {self.perspective.perception}\n"
                                                                    f"Previous Narrative: {self.narrative}\n")
        print(output["narrative"])
        self.narrative += output["narrative"]


if __name__ == "__main__":
    with open(os.path.join(base_dir, "example_environment.json"), "r", encoding='utf-8') as f:
        example = json.load(f)
    example_state = {}
    entities = []
    for entity in example["entities"]:
        ent = Entity(example["entities"][entity]["state"], example["entities"][entity]["new_inputs"], '', entity, example["entities"][entity].get("perception", None))
        example_state[ent.name] = example["environment"]["state"]["EntitySpecificStates"][entity]
        entities.append(ent)
    example_state["OverallState"] = example["environment"]["state"]["OverallState"]
    example_env = Environment(example["environment"]["boundaries"], example_state, entities, entities[0])
    # example_env.update()
    # example_env.generate_narrative()
    example_env.run_simulation()