#!/usr/bin/env python3

import argparse

ACTION_ADD_MODEL = "add-model"
ACTION_BUILD_CONFIG = "build-config"

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to build scripts in python",
    )

    parser.add_argument(
        "action", 
        metavar="action",
        choices=[ACTION_ADD_MODEL, ACTION_BUILD_CONFIG],
        type=str,
        help="Action to take",
    )

    parser.add_argument(
        "--name", "-n", 
        metavar="name", 
        type=str,
        help="Model name.",
    )

    parser.add_argument(
        "--fields", "-f", 
        metavar="fields", 
        type=str, 
        nargs="+",
        help="Fields for the model. Use format <name>:<type>. Valid types str, int, bool",
    )

    args = parser.parse_args()

    if args.action == ACTION_ADD_MODEL:
        import persistence as persist
        persist.add_model(args.name, args.fields)
    print(args.action)

if __name__ == "__main__":
    main()