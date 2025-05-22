import wazuh_api
import ollama_api
import raaaaag


# def filter_policy_checks(agent_id:str, policy_id:str) -> list[dict]:
#     return [ elem for elem in wazuh_api.get_policy_checks( agent_id, policy_id ) if elem["result"]!="passed" ]


def generate_from_one_policy_checks(policy_check:dict,policy_id):
    print("semantic search extraction")
    context = raaaaag.semantic_search(
            policy_check["title"] + policy_id,
            top_k = 1,
            )

    prompt = "give me technical steps to follow that are required for remidiation, with few details"+\
                f"{policy_check}\ncontext: {context}"

    response = ollama_api.invoke(prompt)

    # print(response['response'].split("</think>")[1])

    raaaaag.store_message("remidiation response", prompt, response['response'].split("</think>")[1])
    return response


def generate_from_all_policy_checks(agent_id:str, policy_id:str,
                                    result: str|None = "failed",
                                    select: str|None = "id,remediation,result,title",
                                    id:     str|None = None,
                                    options:str|None = None,
                                    ):

    policy_checks = wazuh_api.get_policy_checks(agent_id,          policy_id,
                                                result=result, select=select,
                                                id=id,        options=options)
    file = open("policy_checks_output", "a")

    for check in policy_checks:
        title = f"\n[{check['id']}] {check['title']}"
        print(title)

        file.write(title+"\n")
        file.write(f"{generate_from_one_policy_checks(check, policy_id)['response'].split('</think>')[1]}" + "\n\n------\n")

    file.close()


# def generate_from_agents_list():
#     agents_list = wazuh_api.get_agents()
#     return ollama_api.invoke(
#             f"this is the list of agents conected to the wazuh server" +
#                     "\n{agents_list}"
#                     )
#
#
# def generate_from_sca_database(agent_id:str):
#     sca_database = wazuh_api.get_agent_sca_database(agent_id)
#     return ollama_api.invoke(
#             f"this is the sca database of the agent numbered {agent_id}\
#                     \n{sca_database}"
#                     )


# def feed_file(file):
#     with open( file, "r" ) as file:
#         chunks = file.read().split("\n\n#########################################################")
#
#     for i, chunk in enumerate(chunks):
#         print(f"chunk {i}")
#         prompt = f"Feeding data chunk {i + 1}: Please store this for later use.\n\n{chunk}"
#         response = ollama_api.invoke(prompt)["response"]
#
#         print(f"storing in rag")
#         raaaaag.store_message("feeding", prompt, response.split("</think>")[1])
#
# def init_deepseek():
#     print("Step 1: Initialization Message")
#     prompt = "You are an assistant specialized in CIS benchmark remediations." +\
#             "I will feed you remediation scripts in chunks related to various CIS benchmarks." +\
#             "Later, I will provide JSON-formatted CIS policy check results from Wazuh." +\
#             "Your task will be to read those JSON inputs and return the appropriate remediation steps." +\
#             "For now, acknowledge and rephrase your understanding of this task to confirm."
#
#     response:str = ollama_api.invoke(prompt)['response']
#     print(response)
#
#     raaaaag.store_message("feeding", prompt, response.split("</think>")[1])
#
#     print("Step 2: Feeding Remediation Script Chunks")
#     feed_file("./Windows Server 2022 Baseline.ps1")
#
