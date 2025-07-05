#!/usr/bin/env bash

set -e

DEFAULT_SCRIPT_NAME=main
export SCRIPT_NAME=${SCRIPT_NAME:-"$DEFAULT_SCRIPT_NAME"}

poetry run "$SCRIPT_NAME"