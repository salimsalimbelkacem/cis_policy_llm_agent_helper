#!/bin/python
# curl "10.0.3.230:11434/api/generate" -d '{"model":"deepseek-r1:1.5b", "prompt":"i will feed you cis policy checks logs from wazuh ok?"}'
import requests
import json
from time import sleep

ollama_api_url="localhost"
model="deepseek-r1:1.5b"
port=11434

def ollama_post_(data:dict, suffix:str, url:str=ollama_api_url, port:int=port):
    _url = f"http://{url}:{port}/{suffix}"
    response = requests.post(url=_url, json=data, stream=True)
    if response.status_code == 200:
        return response
    else:
        print("request failed:", response.text)

def post_generate(prompt:str, url:str=ollama_api_url, port:int=port):
    response = ollama_post_(data={"model":model, "prompt":prompt}, suffix="api/generate", url=url, port=port)
    if response:
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if "response" in chunk:
                        print(chunk["response"], end="", flush=True)
                        full_response += chunk["response"]
                except json.JSONDecodeError:
                    print("Error decoding JSON chunk:", line)
        return full_response
    return None

post_generate("if 1+1 is 2 why 2+2 is not 1?")
