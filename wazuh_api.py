#!/home/salim/.venv/bin/python3

import requests
import json

api_url  = "10.0.3.230"
username = "wazuh-wui"
password = "Oe9lSJE4kNjs9aBV*dADDkNoArmE+rIz"
port     = 55000

def authenticate( username:str=username, password:str=password, url:str=api_url, port:int=port):
    auth_url = f"https://{url}:{port}/security/user/authenticate?raw=true"
    response = requests.post(auth_url, auth=(username, password), verify=False)
    if response.status_code == 200:
        return response.content.decode()
    else:
        print("Authentication failed:", response.text)
        return ""

token = authenticate()

def get_(  suffix:str, url:str=api_url, port:int=port, token:str=token):
    agents_url = f"https://{url}:{port}/{suffix}"
    response = requests.get( url=agents_url, headers={ "Authorization" : f"Bearer {token}" }, verify=False )
    if response.status_code == 200:
        return json.loads(response.content.decode())
    else:
        print("request failed:", response.text)


def get_agents( url:str=api_url, port:int=port, token:str=token):
    return get_(url=url, port=port, suffix="agents", token=token)

def get_policy_checks( agent_id:str, policy_id:str, url:str=api_url, port:int=port, token:str=token ):
    return get_(url=url, port=port, suffix=f"sca/{agent_id}/checks/{policy_id}", token=token)

def get_sca_database( agent_id:str, url:str=api_url, port:int=port, token:str=token ):
    return get_(url=url, port=port, suffix=f"sca/{agent_id}?pretty=true", token=token)

