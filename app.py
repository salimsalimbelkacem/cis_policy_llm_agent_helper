#!./.venv/bin/python3
from src.main import *
from pprint import pprint
import argparse
import tomllib

def validate_id(value):
    if value is not None:
        if not (len(value) == 3 and value.isdigit()):
            raise argparse.ArgumentTypeError("ID must be exactly 3 numeric characters.")
    return value

def main():
    parser = argparse.ArgumentParser(prog="prog")

    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser('list', help='fetch data from wazuh api')
    list_subparsers = list_parser.add_subparsers(dest="list_type")

    list_subparsers.add_parser('agents')

    policy_checks_parser = list_subparsers.add_parser('policyChecks')
    policy_checks_parser.add_argument('--agentId', required= True, type=validate_id, help='Agent ID')
    policy_checks_parser.add_argument('--policyId', required= True, type=str, help='Policy ID')
    policy_checks_parser.add_argument('--id', required=False, type=str, help='policy Check ID (optional)')
    policy_checks_parser.add_argument('--result', required=False, type=str, help='Filter by result (optional)')


    
    from_parser = subparsers.add_parser('generate', help='generate from ollama')
    # from_parser.add_argument('--host', required=False,  type=str)
    # from_parser.add_argument('--model', required=False, type=str)
    # from_parser.add_argument('--port', required=False,  type=int)

    from_subparsers = from_parser.add_subparsers(dest="generate_source")

    policy_checks_gen = from_subparsers.add_parser("policyChecks", help="Generate from policy checks")
    policy_checks_gen.add_argument("--agentId", required=True, type=validate_id)
    policy_checks_gen.add_argument("--policyId", required=True, type=str)
    policy_checks_gen.add_argument("--id", required=False, type=str)
    policy_checks_gen.add_argument("--result", required=False, type=str)

    feed_parser = subparsers.add_parser("feed", help="feed file to the llm")
    feed_parser.add_argument("file")

    args = parser.parse_args()

    if args.command == "list":
        if args.list_type == "agents":
            result = wazuh_api.get_agents()
            for agent in result:
                print(f"{agent['id']} {agent['name']}\n \tos: {agent['os']['name']} {agent['os']['version']}\n \tip: {agent['ip']}\n \tstatus: {agent['status']}\n")

        elif args.list_type == "policyChecks":
            result = wazuh_api.get_policy_checks( args.agentId, args.policyId, id=args.id, result=args.result)
            for policy in result:
                print(f"{policy['id']} [{policy['result']}] {policy['title']}")

    elif args.command == "generate":
        if args.generate_source == "policyChecks":
            result = generate_from_all_policy_checks(args.agentId, args.policyId, id=args.id, result=args.result)

    elif args.command == "feed":
        if args.file:
           raaaaag.ingest_file(args.file)
           # print(args.file)


if __name__ == "__main__":
    main()

