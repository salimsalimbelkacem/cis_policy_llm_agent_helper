import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

llm_model = "deepseek-r1:8b"
ollama_api_url = "10.0.3.230"
port = 11434


def ollama_post_(
        data:   dict,
        suffix: str,
        url:    str = ollama_api_url,
        port:   int = port
        ):

    _url = f"http://{url}:{port}/{suffix}"
    response = requests.post(url=_url, json=data)
    if response.status_code == 200:
        return response
    else:
        print("request failed:", response.text)
        return None


def invoke(
        prompt:		str,
        context:	list | None = None,
        stream:		bool = False,

        # suffix:		str = "",
        # system:		str = "",
        # template:	str = "",
        # options:	dict | None = None,
        # how do i insert context
        # format:		str = "",
        # keep_alive:	str = "5m",
        ):

    print("generating")
    return ollama_post_({
        "model": llm_model,
        "prompt": prompt,
        "context": context or [],
        "stream": stream,

        # "suffix": suffix,
        # "format": format,
        # "options": options or {},
        # "system": system,
        # "template": template,
        # "keep_alive": keep_alive,
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

