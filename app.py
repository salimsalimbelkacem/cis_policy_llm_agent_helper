#!./.venv/bin/python3
from main import *
import argparse
from pprint import pprint

wazuh_api.authenticate()

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(prog="prog")

    # Define subparsers for the commands
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: list
    list_parser = subparsers.add_parser('list', help='List agents or PCs')
    list_subparsers = list_parser.add_subparsers(dest="list_type")
    list_subparsers.add_parser('agents', help='List all agents')
    # list_subparsers.add_parser('policyChecks', help='List all PCs')
    # list_subparsers.add_parser('scaDatabase', help='List all PCs')

    # # Subcommand: gen
    # gen_parser = subparsers.add_parser('generate', help='')
    # gen_subparsers = gen_parser.add_subparsers(dest="gen_type")
    # gen_subparsers.add_parser('pc', help='')
    # gen_subparsers.add_parser('agents', help='')

    # Parse the arguments
    args = parser.parse_args()

    # Handle the parsed arguments
    if args.command == 'list':
        if args.list_type == 'agents':
            pprint(wazuh_api.get_agents())
        # elif args.list_type == 'policyChecks':
        #     pass
    #     else:
    #         print("Invalid list type")
    # elif args.command == 'gen':
    #     if args.gen_type == 'pc':
    #         pass
    #     elif args.gen_type == 'agents':
    #         pass
    #     else:
    #         print("Invalid gen type")
    # else:
    #     print("Invalid command")

if __name__ == "__main__":
    main()

