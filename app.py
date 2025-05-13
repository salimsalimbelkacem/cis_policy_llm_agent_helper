from flask import Flask

import main

app = Flask(__name__)

@app.route("/generate/policy_check/<agent_id>/<policy_id>")
def generate_policy_check(agent_id, policy_id):
    return f"<p>{main.generate_from_policy_checks(agent_id, policy_id)}<p>"
#
# @app.route("/popozo")
# def popozo():
