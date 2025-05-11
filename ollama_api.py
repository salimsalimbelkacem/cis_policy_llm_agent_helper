#!/home/salim/.venv/bin/python3
# curl "10.0.3.230:11434/api/generate" -d '{"model":"deepseek-r1:1.5b", "prompt":"i will feed you cis policy checks logs from wazuh ok?"}'

import requests

ollama_api_url="10.0.3.230"
model="deepseek-r1:1.5b"
port=11434

def ollama_get_(data:dict, suffix:str, url:str=ollama_api_url, port:int=port):
    _url = f"http://{url}:{port}/{suffix}"
    response = requests.get(url=_url, data=data)
    if response.status_code == 200:
        return response
    else:
        print("request failed:", response.text)

def get_generate(prompt:str, url:str=ollama_api_url, port:int=port):
    ollama_get_({"model":model, "prompt":prompt}, "api/generate", url=url, port=port)

print(get_generate("hello"))
