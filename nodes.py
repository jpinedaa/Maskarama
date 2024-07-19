import json
from langchain_core.messages import AIMessage, HumanMessage


def update_entity_node(state, agent):
    temp_state = state
    while True:
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                raise ValueError('Empty response from agent')
            break
        except Exception as e:
            print(f'Error trying to parse output, Error: {e}, retrying')
            # update agent state with error message and try again
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse output - {e}'))
            continue

    return {
        "messages": [result.content]
    }


def output_json_node(state, agent):
    temp_state = state
    output = None
    while True:
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                raise ValueError('Empty response from agent')
            output = json.loads(result.content.replace('json', '').replace('`', ''))
            break
        except Exception as e:
            print(f'Error trying to parse output, Error: {e}, retrying')
            # update agent state with error message and try again
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse output - {e}'))
            continue

    return {
        "output": output
    }