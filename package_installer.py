#!/usr/bin/env python3

import yaml
import subprocess
from pathlib import Path


def main():
    if Path("./env").is_dir() is True:
        print("Local env is already created")
        return

    create_virtual_env()
    install_dependencies()
    lock_dependencies()


def install_dependencies():
    """
    Install dependencies using pip from a config file.

    Config file must be a yaml valid file.
    """
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            print(config)
            if "deps" not in config:
                print("Could not find deps key in config")
                return

            deps = config["deps"]

            if isinstance(deps, list):
                print("Deps key should be a list")
                return

            for dep in deps:
                exec(f"./env/bin/pip install {dep}")

        except yaml.YAMLError as err:
            print(f"Encountered error: {err}")


def create_virtual_env():
    """
    Function creates the virtual env.

    The name of the virtual env will be env.
    """
    exec("python3 -m venv env")


def lock_dependencies():
    """
    Function locks the dependencies of the project to a requirements file.

    After the dependencies are install using pip into the virtual env, they need to be locked using this function.
    """

    res = exec_with_output("./env/bin/python -m pip freeze")
    f = open("requirements.txt", "w")
    f.write(res)
    f.close()


def install_deps_from_lock():
    exec("./env/bin/python -m pip install -r requirements.txt")


def exec(cmd: str)-> int:
    """
    Function executes a command and returns the status code.

    Status code 0 means that the command run has been successful.

    Anything except 0 there was an error. Please google the status code to see the cause.
    """
    return subprocess.run(
        cmd.split(" "), 
        stdout=subprocess.DEVNULL,
    ).returncode


def exec_with_output(cmd: str)-> str:
    """
    Function runs a comman and returns the output as a string.

    It is similar to the simple exec function, but instead of status code, it returns the output as a string.
    """
    return subprocess.run(
        cmd.split(" "), 
        capture_output=True, 
        text=True
    ).stdout


if __name__ == "__main__":
    main()