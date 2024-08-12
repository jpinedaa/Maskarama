import json
import random
import time
from langchain_core.messages import AIMessage, HumanMessage


_delay = 5


def update_entity_node(state, agent):
    global _delay
    temp_state = state
    retries = 5
    while True:
        print("Input: ", temp_state["messages"])
        print("--------------------------------------------------------------------")
        time.sleep(random.random() * _delay)
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                #raise ValueError('Empty response from agent')
                if retries == 0:
                    raise ValueError('Max retries reached')
                retries -= 1
                print(f'Empty response from agent,waiting {_delay} seconds before retrying...')
                _delay *= 2
                time.sleep(_delay)
                print(f'Retrying... retries left: {retries}')
                continue
            break
        except Exception as e:
            if retries == 0:
                raise ValueError('Max retries reached')
            retries -= 1
            print(f'Error trying to parse output, Error: {e}, Output: {result.content}, waiting for {_delay} seconds, retrying... retries left: {retries}')
            # update agent state with error message and try again
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse output - {e}'))
            _delay *= 2
            time.sleep(_delay)
            continue

    print("Output: ", result.content)
    print(
        "--------------------------------------------------------------------")
    return {
        "messages": [result.content]
    }


def input_node(state, agent):
    global _delay
    temp_state = state
    approved = None
    retries = 5
    while True:
        print("Input: ", temp_state["messages"])
        print("--------------------------------------------------------------------")
        time.sleep(random.random() * _delay)
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                #raise ValueError('Empty response from agent')
                if retries == 0:
                    raise ValueError('Max retries reached')
                retries -= 1
                print(f'Empty response from agent,waiting {_delay} seconds before retrying...')
                _delay *= 2
                time.sleep(_delay)
                print(f'Retrying... retries left: {retries}')
                continue
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
            print(f'Error trying to parse output, Error: {e}, Output: {result.content}, waiting for {_delay} seconds, retrying... retries left: {retries}')
            # update agent state with error message and try again
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse output - {e}'))
            _delay *= 2
            time.sleep(_delay)
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
    global _delay
    temp_state = state
    output = None
    retries = 5
    while True:
        time.sleep(random.random() * _delay)
        result = agent.invoke(temp_state["messages"])
        try:
            if result.content == '':
                #raise ValueError('Empty response from agent')
                if retries == 0:
                    raise ValueError('Max retries reached')
                retries -= 1
                print(f'Empty response from agent,waiting {_delay} seconds before retrying...')
                _delay *= 2
                time.sleep(_delay)
                print(f'Retrying... retries left: {retries}')
                continue
            output = json.loads(result.content.replace('json', '').replace('`', ''))
            break
        except Exception as e:
            if retries == 0:
                raise ValueError('Max retries reached')
            retries -= 1
            print(f'Error trying to parse output, Error: {e}, output should be json format without any additional text our output so do not explain what you did different in this response just output the json by itself. Wrong Output: {result.content}, waiting for {_delay} seconds, retrying... retries left: {retries}')
            # update agent state with error message and try again
            # TODO - test if better too retry without appending the error message
            temp_state['messages'].append(AIMessage(content=result.content))
            temp_state['messages'].append(HumanMessage(content=f'Error trying to parse json output, please try again,  error: {e}'))
            _delay *= 2
            time.sleep(_delay)
            continue

    print("JSON Output: ", json.dumps(output, indent=4))
    print(
        "--------------------------------------------------------------------")
    return {
        "output": output
    }