#!/bin/bash

# Setup two virtual environments for developing and bundling the tool.
# Call with -C to clean 

req_py_version='3.9.6'

#-----------------
# VENV-TOOLS CHECK
#-----------------
echo "Checking for venv-tools..."
if [[ ! -x venv-tools/venv-setup ]]; then
	echo "venv-tools submodule is not initialized. Please run 'git submodule init'!" >&2
	exit 98
fi

#-------------
# PYENV CHECK
#-------------
echo "Checking for pyenv..."
if ! command -v pyenv 1>/dev/null 2>&1; then
	echo 'pyenv and pyenv-virtualenv are required for this script!' >&2
	echo 'Please see https://github.com/pyenv/pyenv and https://github.com/pyenv/pyenv-virtualenv' >&2
	exit 99
fi
echo "Activating pyenv..."
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

#-------------------------
# DEVELOPMENT ENVIRONMENT
#-------------------------
echo ""
echo "*** SETUP DEVELOPMENT ENVIRONMENT ***"

venv_name='chumsheet-dev'
venv_local_path='.'
venv_req_file="$venv_local_path/requirements-dev.txt"

scriptflags=('-v' '-A' '-A' '-d' '-u')

read -p "Do you use Sublime Text and want to use a local Python-LSP [y|N]? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	scriptflags+=( '-S' )
fi

./venv-tools/venv-setup "${scriptflags[@]}" -n "$venv_name" -p "$req_py_version" -r "$venv_req_file"
if [[ $? -ne 0 ]]; then
	echo "ERROR: An error (#$?) occurred in venv-setup."
	exit 97
fi

echo "Setting local virtual environment for pyenv..."
cd "$venv_local_path"
pyenv local "$venv_name"

#--------------------
# BUNDLE ENVIRONMENT
#--------------------
echo ""
echo "*** SETUP BUNDLE ENVIRONMENT ***"

venv_name='chumsheet-bundle'
venv_local_path='bundle'
venv_req_file="$venv_local_path/requirements-bundle.txt"

scriptflags=('-v' '-A' '-A' '-d' '-u' )

./venv-tools/venv-setup "${scriptflags[@]}" -n "$venv_name" -p "$req_py_version" -r "$venv_req_file"
if [[ $? -ne 0 ]]; then
	echo "ERROR: An error (#$?) occurred in venv-setup."
	exit 97
fi

echo "Setting local virtual environment for pyenv..."
cd "$venv_local_path"
pyenv local "$venv_name"
