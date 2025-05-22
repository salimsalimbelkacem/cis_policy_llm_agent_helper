import requests
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import tomllib

with open("./config.toml", "rb") as config_file:
    configs = tomllib.load(config_file)['ollama']

def ollama_post_(
        data:   dict,
        suffix: str,
        url:    str = configs['ollama_api_url'],
        port:   int = configs['port'],
        ):

    _url = f"http://{url}:{port}/{suffix}"
    response = requests.post(url=_url, json=data)
    if response.status_code == 200:
        return response
    else:
        print("request failed:", response.text)
        return response


def invoke(
        prompt:		str,
        context:	list | None = None,
        stream:		bool = False,

        # suffix:str = "", system:str = "",
        # template:str = "", options:dict | None = None,
        # format:str = "", keep_alive:str = "5m",
        ):

    print("generating")
    if stream:
        print("stream!")

        response = ollama_post_({ "model": configs['llm_model_name'], "prompt": prompt,\
        "context": context or [], "stream": stream, }, "api/generate") 

        chunkies = ""
        last_obj:dict={}

        for line in response.iter_lines():
            if line:
                decoded = json.loads(line.decode('utf-8'))
                print(decoded["response"], end="")
                chunkies += decoded["response"]
                last_obj = decoded

        last_obj["response"] = chunkies        
        return last_obj

    else:
        return ollama_post_({
            "model": configs['llm_model_name'],
            "prompt": prompt,
            "context": context or [],
            "stream": stream,
            # "suffix": suffix, "options": options or {},
            # "system": system, "keep_alive": keep_alive,
            # "template": template, "format": format,
            }, "api/generate").json()


import json
import os


def generate(prompt:str):

    if os.path.exists(".context"):
        file = open(mode="r", file=".context")
        context = '{"context":'+file.read()+'}'
        file.close()

    else:
        context = '{"context":[]}'

    response = invoke(prompt, context = json.loads(context)["context"])

    file = open(mode="w", file=".context")
    file.write(f"{response['context']}")
    file.close()

    return response

