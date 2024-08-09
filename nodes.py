import json
from langchain_core.messages import AIMessage, HumanMessage


def update_entity_node(state, agent):
    temp_state = state
    retries = 5
    while True:
        print("Input: ", json.dumps(temp_state["messages"], indent=4))
        print("--------------------------------------------------------------------")
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                raise ValueError('Empty response from agent')
            break
        except Exception as e:
            if retries == 0:
                raise ValueError('Max retries reached')
            retries -= 1
            print(f'Error trying to parse output, Error: {e}, Output: {result.content}, retrying')
            # update agent state with error message and try again
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse output - {e}'))
            continue

    print("Output: ", result.content)
    print(
        "--------------------------------------------------------------------")
    return {
        "messages": [result.content]
    }


def input_node(state, agent):
    temp_state = state
    approved = None
    retries = 5
    while True:
        print("Input: ", json.dumps(temp_state["messages"], indent=4))
        print("--------------------------------------------------------------------")
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                raise ValueError('Empty response from agent')
            if 'APPROVED' in result.content:
                approved = True
            elif 'REJECTED' in result.content:
                approved = False
            else:
                raise ValueError('Approval status not found in output, please include either APPROVED or REJECTED in the output')
            break
        except Exception as e:
            if retries == 0:
                raise ValueError('Max retries reached')
            retries -= 1
            print(f'Error trying to parse output, Error: {e}, Output: {result.content}, retrying')
            # update agent state with error message and try again
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse output - {e}'))
            continue

    print("Output: ", result.content)
    print(
        "--------------------------------------------------------------------")
    return {
        "messages": [result.content],
        "approved": approved
    }


def output_node(state, agent):
    return {"output": state["output"]}


def output_json_node(state, agent):
    temp_state = state
    output = None
    retries = 5
    while True:
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                raise ValueError('Empty response from agent')
            output = json.loads(result.content.replace('json', '').replace('`', ''))
            break
        except Exception as e:
            if retries == 0:
                raise ValueError('Max retries reached')
            retries -= 1
            print(f'Error trying to parse output, Error: {e}, Output: {result.content}, retrying')
            # update agent state with error message and try again
            # TODO- test if better too retry without appending the error message
            #temp_state['messages'].append(AIMessage(content=result.content))
            #temp_state['messages'].append(HumanMessage(content=f'Error trying to parse json output, please try again,  error: {e}'))
            continue

    print("JSON Output: ", json.dumps(output, indent=4))
    print(
        "--------------------------------------------------------------------")
    return {
        "output": output
    }