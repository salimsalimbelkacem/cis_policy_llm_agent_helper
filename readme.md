# CIS remediation helper powered by deepseek and wazuh

## dependencies
you need to install ollama (somewhere in your network) and pull an llm model and the `nomic-embed-text` embedding model from there
```bash
curl -fsSL https://ollama.com/install.sh | sh && ollama pull deepseek-r1:8b && ollama pull nomic-embed-text
```
you then need to deploy wazuh (also somewhere in your network), you can refer to the [instalation guide](https://documentation.wazuh.com/current/installation-guide/index.html)

then you need to install the python dependency:
```bash
python -m venv .venv && ./.venv/bin/pip install chromadb
```

## usage
to simply fetch data from the wazuh api:
```bash
./app.py list agents
./app.py list policyChecks --agentId STRING --policyId STRING [--id STRING] [--result STRING]
```

to generate text from the llm:
```bash
./app.py generate policyChecks  --agentId STRING --policyId STRING [--id STRING] [--result STRING]
```
