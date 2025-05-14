import wazuh_api
import ollama_api

def filter_policy_checks(agent_id:str, policy_id:str) -> list[dict]:
    return [ elem for elem in wazuh_api.get_policy_checks( agent_id, policy_id ) if elem["result"]!="passed" ]

def generate_from_policy_checks(agent_id:str, policy_id:str) :
    policy_checks = filter_policy_checks(agent_id, policy_id)
    file = open("policy_checks_output", "a")

    for check in policy_checks:
        print(f"\n[{check['id']}] {check['title']}")

        file.write(f"[{check['id']}] {check['title']}\n")
        file.write(
                ollama_api._generate(
                    f"explain what does this policy check mean in simple words then\
                            give me detailed steps to follow that are required for\
                            remidiation in bullet points\
                            \n{check}"
                            ) + "\n"
                )

def generate_from_agents_list():
    agents_list = wazuh_api.get_agents()
    return ollama_api._generate(
            f"this is the list of agents conected to the wazuh server\
                    \n{agents_list}"
                    )

def generate_from_sca_database(agent_id:str):
    sca_database = wazuh_api.get_sca_database(agent_id)
    return ollama_api._generate(
            f"this is the sca database of the agent numbered {agent_id}\
                    \n{sca_database}"
                    )

# def init_deepseek():
#     return ollama_api._generate("")
