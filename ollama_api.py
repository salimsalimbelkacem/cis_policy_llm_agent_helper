import requests
import json

ollama_api_url="10.0.3.230"
model="deepseek-r1:8b"
port=11434

def ollama_post_(data:dict, suffix:str, url:str=ollama_api_url, port:int=port):
    _url = f"http://{url}:{port}/{suffix}"
    response = requests.post(url=_url, json=data, stream=True)
    if response.status_code == 200:
        return response
    else:
        print("request failed:", response.text)

def _generate(prompt:str) -> str:
    response = ollama_post_({"model":model, "prompt":prompt}, "api/generate")
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
        print("")
        return full_response
    return ""
