import os

from nodes import update_entity_node, output_json_node
from utils import base_dir, get_json_schema_prompt, build_graph, get_model
from agents import create_agent, AgentState
import functools


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


entity_update_graph = build_update_graph("entity_update.txt",
                                              {"updated_state": "str"})
perception_update_graph = build_update_graph("perception_update.txt",
                                                  {"updated_perception": "str"})
currentOutput_graph = build_update_graph("currentOutput.txt",
                                              {"currentOutput": "str"})
environment_update_graph = build_update_graph("environment_update.txt",
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
                                                            "exit_entities": {"entity1_name": "ConnectedEnvironmentID01",
                                                                              "entity2_name": "ConnectedEnvironmentID01",
                                                                              "entityN_name": "ConnectedEnvironmentID02"}
                                                            })
narrative_generation_graph = build_update_graph("narrative_generation.txt", {"narrative": "str"})
inputs_update_graph = build_update_graph("inputs_update.txt", {"entity1_name": "str", "entity2_name": "str", "entityN_name": "str"})
entities_update_graph = build_update_graph("entity_update.txt", {"entity1_name": "str", "entity2_name": "str", "entityN_name": "str"})
generate_currentoutput_graph = build_update_graph("currentOutput.txt", {"entity1_name": "str", "entity2_name": "str", "entityN_name": "str"})