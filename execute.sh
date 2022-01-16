#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:${PWD}"
eval "python3 ./${1}.py ${@:2}"