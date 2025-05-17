import wazuh_api
import ollama_api
import raaaaag

def filter_policy_checks(agent_id:str, policy_id:str) -> list[dict]:
    return [ elem for elem in wazuh_api.get_policy_checks( agent_id, policy_id ) if elem["result"]!="passed" ]

def generate_from_one_policy_checks(policy_check:dict) -> str:
    context = raaaaag.retrieve_for_llm(query=policy_check["title"])

    return ollama_api.invoke(
                    f"give me the powershell commands to remidiate this with no details\
                            \n{policy_check}",
                            context=f"\n{context}"
                            )

def generate_from_all_policy_checks(agent_id:str, policy_id:str) :
    print("1")
    policy_checks = filter_policy_checks(agent_id, policy_id)
    print("2")
    file = open("policy_checks_output", "a")

    print("3")
    print(policy_checks)
    for check in policy_checks:
        title = f"\n[{check['id']}] {check['title']}"
        print(title)
        file.write(title+"\n")
        file.write(generate_from_one_policy_checks(check) + "\n\n----\n")


def generate_from_agents_list():
    agents_list = wazuh_api.get_agents()
    return ollama_api.invoke(
            f"this is the list of agents conected to the wazuh server\
                    \n{agents_list}"
                    )

def generate_from_sca_database(agent_id:str):
    sca_database = wazuh_api.get_agent_sca_database(agent_id)
    return ollama_api.invoke(
            f"this is the sca database of the agent numbered {agent_id}\
                    \n{sca_database}"
                    )

def init_deepseek():
    print("Step 1: Initialization Message")
    ollama_api.invoke(
            "You are an assistant specialized in CIS benchmark remediations." +
            "I will feed you remediation scripts in chunks related to various CIS benchmarks." +
            "Later, I will provide JSON-formatted CIS policy check results from Wazuh." +
            "Your task will be to read those JSON inputs and return the appropriate remediation steps." +
            "For now, acknowledge and rephrase your understanding of this task to confirm."
            )

    print("Step 2: Feeding Remediation Script Chunks")
    with open("./Windows Server 2022 Baseline.ps1", "r") as file:
        chunks = file.read().split("\n\n#########################################################")

        for i, chunk in enumerate(chunks):
            ollama_api.invoke(
                    f"Feeding data chunk {i + 1}: Please store this for later use.\n\n{chunk}"
                    )
