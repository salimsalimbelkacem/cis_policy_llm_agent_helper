#!/home/salim/.venv/bin/python3

import requests

def authenticate( username:str, password:str, url:str, port:int):
    auth_url = f"https://{url}:{port}/security/user/authenticate?raw=true"
    response = requests.post(auth_url, auth=(username, password), verify=False)
    if response.status_code == 200:
        return response.content.decode()
    else:
        print("Authentication failed:", response.text)
        return ""

def get_( url:str, port:int, token:str | None, suffix:str=""):
    agents_url = f"https://{url}:{port}/{suffix}"
    response = requests.get( url=agents_url, headers={ "Authorization" : f"Bearer {token}" }, verify=False )

    if response.status_code == 200:
        return response.content.decode()
    else:
        print("request failed:", response.text)
        return ""

def get_agents( url:str, port:int, token:str):
    return get_(url=url, port=port, suffix="agents", token=token)

def get_compliance( url:str, port:int, token:str, agent_id:str, compliace:str):
    return get_(url=url, port=port, suffix=f"sca/{agent_id}/checks/{compliace}", token=token)

api_url  = "10.0.3.230"
username = "wazuh-wui"
password = "Oe9lSJE4kNjs9aBV*dADDkNoArmE+rIz"
port     = 55000

token = authenticate(url=api_url, username=username, password=password, port=port)

print(token)

print(get_agents(url=api_url, port=port, token=token))

"""
Pour définir votre token d'authentification : TOKEN=$(curl -u wazuh-wui:Password -k -X POST "https://IP:55000/security/user/authenticate?raw=true")
Pour tester la connectivité : curl -k -X GET "https://IP:55000/" -H "Authorization: Bearer $TOKEN"
Pour récuperer la liste des agents et leurs ID : curl -k -X GET "https://IP:55000/agents" -H  "Authorization: Bearer $TOKEN"
Pour récuperer le résultat de compliance depuis Wazuh : curl -k -X GET "https://IP:55000/sca/[agentID]/checks/cis_win2016?" -H  "Authorization: Bearer $TOKEN" -o result.txt
"""
