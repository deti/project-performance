#! /usr/bin/env bash
# Getting the directory of the script
# All interactions with the file system should be relative to the script's directory

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR || exit 1

if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

#cd $SCRIPT_DIR/.. || exit 1

#mypy server --exclude server/.venv/ --exclude server/venv/

ruff check --fix src
ruff format src
