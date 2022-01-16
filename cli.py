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

    parser.add_argument(
        "--config", "-c", 
        dest="config_file", 
        type=str,
        help="Provide a config file to read from",
    )

    args = parser.parse_args()

    if args.action == ACTION_ADD_MODEL:
        if args.name is None:
            print("Please add model name")
            return

        if args.fields is None or len(args.fields) == 0:
            print("Please add fields to the model")
            return

        import persistence as persist
        persist.add_model(args.name, args.fields)
        return

    if args.action == ACTION_BUILD_CONFIG:
        import helpers
        helpers.main(args.config_file)


if __name__ == "__main__":
    main()