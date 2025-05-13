# interaction with wazuh api
cis alerts data will be sent from wazuh based on either:
- subscrition
- manually triggered by the user

# llm and app deployment
about the app it will be dockerized
but about the llm it we will either:
- deploy llm localy with deepseek (probably also dockerized)

# LLM
the llm's behaviour will either be:
- directly responding to promt acording to what data he was fed
- LLM agent, interacts with external APIs to get needed data per example: microsoft websites

# front end
the app then must display the data collected from the llm with either:
- a custom dashboard plugin for wazuh
- a standalone front end
