# CIS remediation helper powered by deepseek and wazuh

## instalations and dependencies
you need to install ollama (somewhere in your network) and pull an llm model and the `nomic-embed-text` embedding model from there
```bash
curl -fsSL https://ollama.com/install.sh | sh && ollama pull deepseek-r1:8b && ollama pull nomic-embed-text
```
you then need to deploy wazuh (also somewhere in your network), you can refer to the [instalation guide](https://documentation.wazuh.com/current/installation-guide/index.html)

then you need to install the python dependency:
```bash
python -m venv .venv && ./.venv/bin/pip install chromadb
```

## configuration
you need to create a file named `config.toml` in the root directory. should look like this
```toml
[wazuh]
api_url = ""   # The base URL of your Wazuh API
username = ""  # Your Wazuh API username
password = ""  # Your Wazuh API password
port = 55000   # The port your Wazuh API is running on

[ollama]
api_url = ""   # The base URL of the Ollama API
llm_model = "" # The name of the language model to use
port = 11434   # The port the Ollama service is running on
```

## usage
to simply fetch data from the wazuh api:
```bash
./app.py list agents
./app.py list policyChecks --agentId {STRING} --policyId {STRING} [--id {STRING}] [--result {STRING}]
```

to generate remediation advice from the llm:
```bash
./app.py generate policyChecks  --agentId {STRING} --policyId {STRING} [--id {STRING}] [--result {STRING}]
```

to store files for the RAG (feed):
```bash
./app.py feed {FILE}
```
