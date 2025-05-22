import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_url  = "10.0.3.230"
username = "wazuh-wui"
password = "Oe9lSJE4kNjs9aBV*dADDkNoArmE+rIz"
port     = 55000

def post_authenticate(
        username:str=username,
        password:str=password,
        url:str=api_url,
        port:int=port
        ) -> str:
    """
send post request for authentication, returns string token
    """
    auth_url = f"https://{url}:{port}/security/user/authenticate?raw=true"
    response = requests.post(auth_url, auth=(username, password), verify=False)
    if response.status_code == 200:
        return response.content.decode()
    else:
        print("Authentication failed:", response.text)
        return ""

token = post_authenticate()

def get_(
        suffix:str,
        options:str = "",
        url:str=api_url,
        port:int=port,
        token:str=token
        ) -> list[dict]:
    """
send get request to the wazuh api with authentication token in the header
    """
    agents_url = f"https://{url}:{port}/{suffix}?{options}"
    response = requests.get( url=agents_url, headers={ "Authorization" : f"Bearer {token}" }, verify=False )
    if response.status_code == 200:
        return json.loads(response.content.decode())["data"]["affected_items"]
    else:
        print("request failed:", response.text)
        return [{}]


def get_agents(
        url:str=api_url,
        port:int=port,
        token:str=token,

         status:str|None=None,
         select:str|None="id,ip,name,os.name,os.version,status",
        options:str|None=None,
        ) -> list[dict]:
    """
gets list of agents with informations, returns list of objects
    """
    return get_(
            url=url,
            port=port,
            suffix="agents",
            token=token,
            options=(f"status={status}&" if status else "") +
                    (f"select={select}&" if select else "") +
                    (options or "")
                )


def get_policy_checks(
        agent_id:str, policy_id:str,
        url:str=api_url, port:int=port,
        token:str=token,
        result: str|None = None,
        select: str|None = None,
        id:     str|None = None,
        options:str|None = None,
        ) -> list[dict]:
    """
get list of all the cis policy checks, returns list of objects

:param agent_id:  required, Agent ID. All possible values from 000 onwards
:param policy_id: required, Filter by policy id

:param     id:  Filter by check id
:param result:  Filter by result
:param select:  Select which fields to return (separated by comma). Use '.' for nested fields.
                For example, '{field1: field2}' may be selected with 'field1.field2'
:param options: additional options from the [wazuh api documentation](https://documentation.wazuh.com/current/user-manual/api/reference.html#operation/api.controllers.sca_controller.get_sca_checks) can be added separated with `&`
    """
    return get_(
            url=url, port=port,
            suffix=f"sca/{agent_id}/checks/{policy_id}",
            token=token,
            options=(f"result={result}&" if result else "") +
                    (f"select={select}&" if select else "") +
                    (f"q=id={id}&"       if id     else "") +
                    (options or "")
                    )


def get_agent_sca_database(
        agent_id:str,

        url:str=api_url,
        port:int=port,
        token:str=token 
        ) -> list[dict]:
    """
get the sca database from agent, returns list of object
    """
    return get_(url=url, port=port, suffix=f"sca/{agent_id}", token=token)

