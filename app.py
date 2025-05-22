#!./.venv/bin/python3
from main import wazuh_api
import argparse
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(prog="prog")

    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser('list')
    list_subparsers = list_parser.add_subparsers(dest="list_type")

    list_subparsers.add_parser('agents')

    policy_checks_parser = list_subparsers.add_parser('policyChecks')
    policy_checks_parser.add_argument('arg1', type=str)
    policy_checks_parser.add_argument('arg2', type=str)


    args = parser.parse_args()

    if args.command == 'list':
        if args.list_type == 'agents':
            pprint(wazuh_api.get_agents())
            print("")
        elif args.list_type == 'policyChecks':
            result = wazuh_api.get_policy_checks(args.arg1, args.arg2, select="id,title,result")
            for policy in result:
                print(f"{policy['id']} [{policy['result']}] {policy['title']}")
            print("")

if __name__ == "__main__":
    main()

