#!./.venv/bin/python3
from ./src/main import *
from pprint import pprint
import argparse

def validate_id(value):
    if value is not None:
        if not (len(value) == 3 and value.isdigit()):
            raise argparse.ArgumentTypeError("ID must be exactly 3 numeric characters.")
    return value

def str_to_bool(value):
    if value.lower() in ('true', 'y', 'yes'):
        return True
    elif value.lower() in ('false', 'n', 'no'):
        return False
    raise argparse.ArgumentTypeError("Stream must be a boolean (true/false)")

def main():
    parser = argparse.ArgumentParser(prog="prog")

    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser('list')
    list_subparsers = list_parser.add_subparsers(dest="list_type")

    list_subparsers.add_parser('agents')

    policy_checks_parser = list_subparsers.add_parser('policyChecks')
    policy_checks_parser.add_argument('--agentId', required= True, type=validate_id, help='Agent ID')
    policy_checks_parser.add_argument('--policyId', required= True, type=str, help='Policy ID')
    policy_checks_parser.add_argument('--id', required=False, type=str, help='policy Check ID (optional)')
    policy_checks_parser.add_argument('--result', required=False, type=str, help='Filter by result (optional)')


    
    from_parser = subparsers.add_parser('generate', help='Generate data from sources')
    policy_checks_gen.add_argument('--host', required=True,  type=str)
    policy_checks_gen.add_argument('--model', required=True, type=str)
    policy_checks_gen.add_argument('--port', required=True,  type=int)
    from_subparsers = from_parser.add_subparsers(dest="generate_source")

    policy_checks_gen = from_subparsers.add_parser('policyChecks', help='Generate from policy checks')
    policy_checks_gen.add_argument('--agentId', required=True, type=validate_id)
    policy_checks_gen.add_argument('--policyId', required=True, type=str)
    policy_checks_gen.add_argument('--id', required=False, type=str)
    policy_checks_gen.add_argument('--result', required=False, type=str)
    policy_checks_gen.add_argument('--stream', required=False, type=str_to_bool)

    args = parser.parse_args()

    if args.command == 'list':
        if args.list_type == 'agents':
            pprint(wazuh_api.get_agents())
            print("")

        elif args.list_type == 'policyChecks':
            result = wazuh_api.get_policy_checks( args.agentId, args.policyId, id=args.id, result=args.result)
            for policy in result:
                print(f"{policy['id']} [{policy['result']}] {policy['title']}")
            print("")

    elif args.command == 'generate':
        if args.generate_source == 'policyChecks':
            result = generate_from_all_policy_checks(args.agentId, args.policyId, id=args.id, result=args.result)



if __name__ == "__main__":
    main()

