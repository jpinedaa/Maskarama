import json
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
import re
import unicodedata
#import io
#from tkinter import Image


base_dir = os.path.dirname(os.path.abspath(__file__))
disable_filters = {HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                   }


def set_api_key():
    with open(os.path.join(base_dir, "config.json"), "r") as f:
        config = json.load(f)
    os.environ["GOOGLE_API_KEY"] = config["api_key"]


set_api_key()


def update_api_key(api_key):
    with open(os.path.join(base_dir, "config.json"), "r") as f:
        config = json.load(f)
    config["api_key"] = api_key
    with open(os.path.join(base_dir, "config.json"), "w") as f:
        json.dump(config, f)
    set_api_key()


def get_model(json_output=False):
    set_api_key()
    # return ChatOpenAI(model="gpt-4-turbo", api_key="")
    if not json_output:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                      safety_settings=disable_filters,
                                      temperature=0.5
                                     )
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                      safety_settings=disable_filters,
                                      temperature=0.5,
                                    generation_config={"response_mime_type": "application/json"})
    return llm


def get_json_schema_prompt(dict_schema):
    with open(os.path.join(base_dir, "prompts/json_output.txt"), "r", encoding='utf-8') as f:
        json_schema_prompt = f.read()

    json_schema_string = json.dumps(dict_schema, indent=4)
    variable_name = "JSON_SCHEMA"
    json_schema_prompt = json_schema_prompt.replace(variable_name, json_schema_string)

    return json_schema_prompt


# def show_graph(graph):
#     # show image
#     graph_image = graph.get_graph(xray=True).draw_mermaid_png()
#
#     # Convert bytes to a file-like object
#     graph_image_file = io.BytesIO(graph_image)
#
#     # Open the image file
#     img = Image.open(graph_image_file)
#
#     ## Display the image
#     img.show()


def build_graph(state_class, nodes, edges, entry_point):
    workflow = StateGraph(state_class)

    for node in nodes:
        workflow.add_node(node[0], node[1])

    for edge in edges:
        workflow.add_conditional_edges(edge[0], edge[1], edge[2])

    workflow.set_entry_point(entry_point)
    graph = workflow.compile()
    # show_graph(graph)

    return graph


def clean_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()

    # Remove control characters except for newline (\n) and carriage return (\r)
    text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C' or ch in ('\n', '\r'))

    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)


if __name__ == '__main__':
    dir = os.path.join(base_dir, "initial_states")
    for file in os.listdir(dir):
        if file.endswith(".txt"):
            print(f"Cleaning file: {file}")
            clean_file(os.path.join(dir, file), os.path.join(dir, file))