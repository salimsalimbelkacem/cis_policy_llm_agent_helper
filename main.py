#!/home/salim/.venv/bin/python3

import requests

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

def get_( url:str=api_url, port:int=port, token:str=token, suffix:str=""):
    agents_url = f"https://{url}:{port}/{suffix}"
    response = requests.get( url=agents_url, headers={ "Authorization" : f"Bearer {token}" }, verify=False )

    if response.status_code == 200:
        return response.content.decode()
    else:
        print("request failed:", response.text)
        return ""

def get_agents( url:str=api_url, port:int=port, token:str=token):
    return get_(url=url, port=port, suffix="agents", token=token)

def get_policy_checks( agent_id:str, policy_id:str, url:str=api_url, port:int=port, token:str=token ):
    return get_(url=url, port=port, suffix=f"sca/{agent_id}/checks/{policy_id}", token=token)

def get_sca_database( agent_id:str, url:str=api_url, port:int=port, token:str=token ):
    return get_(url=url, port=port, suffix=f"sca/{agent_id}?pretty=true", token=token)

print(token)

"""
Pour définir votre token d'authentification : TOKEN=$(curl -u wazuh-wui:Password -k -X POST "https://IP:55000/security/user/authenticate?raw=true")
Pour tester la connectivité : curl -k -X GET "https://IP:55000/" -H "Authorization: Bearer $TOKEN"
Pour récuperer la liste des agents et leurs ID : curl -k -X GET "https://IP:55000/agents" -H  "Authorization: Bearer $TOKEN"
Pour récuperer le résultat de compliance depuis Wazuh : curl -k -X GET "https://IP:55000/sca/[agentID]/checks/cis_win2016?" -H  "Authorization: Bearer $TOKEN" -o result.txt
"""
