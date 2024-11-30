#!/usr/bin/env bash

# ~/.gitconfig.aliases is provided in Dockerfile
# shellcheck disable=SC2088
git config --global include.path '~/.gitconfig.aliases'

REPO_DIR='/workspaces/richy'
if [ -d "${REPO_DIR}" ]; then
	git config --global --add safe.directory "${REPO_DIR}"

    pushd "${REPO_DIR}" || (echo "[ERROR] Could not 'pushd \"${REPO_DIR}\"'" && exit 1)
    poetry lock && poetry install --all-extras
    popd || (echo "[ERROR] Could not 'popd'" && exit 2)
fi
