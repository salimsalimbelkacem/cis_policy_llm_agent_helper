import requests
import json

llm_model = "deepseek-r1:8b"
ollama_api_url = "localhost"
port = 11434

def ollama_post_(data: dict, suffix: str, url: str = ollama_api_url, port: int = port):
    _url = f"http://{url}:{port}/{suffix}"
    response = requests.post(url=_url, json=data)
    if response.status_code == 200:
        return response
    else:
        print("request failed:", response.text)
        return None

def invoke(
        prompt:		str,
        suffix:		str = "",
        format:		str = "",
        system:		str = "",
        template:	str = "",
        options:	dict | None = None,
        context:	list | None = None,
        keep_alive:	str = "5m",
        stream:		bool = False,
        ):

    return ollama_post_({
        "model": llm_model,
        "prompt": prompt,
        "suffix": suffix,
        "format": format,
        "options": options or {},
        "system": system,
        "template": template,
        "context": context or [],
        "stream": stream,
        "keep_alive": keep_alive,
        }, "api/generate").json()
