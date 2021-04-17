#!/bin/bash

# Setup two virtual environments for developing and bundling the tool.
PY_VERSION='3.9.4'
DEV_ENV_NAME='chumsheet-dev'
BUNDLE_ENV_NAME='chumsheet-bundle'

#-------------
# PYENV CHECK
#-------------
echo "Checking for pyenv..."
if ! command -v pyenv 1>/dev/null 2>&1; then
	echo 'pyenv and pyenv-virtualenv are required for this script!'
	echo 'Please see https://github.com/pyenv/pyenv and https://github.com/pyenv/pyenv-virtualenv'
	exit 1
fi
echo "Activating pyenv..."
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

#----------------
# PYTHON VERSION
#----------------

# Install the Python version, if not already installed
if pyenv versions --bare | grep -q $PY_VERSION; then
	echo "Python Version <$PY_VERSION> already present."
else
	echo "Installing Python version <$PY_VERSION>..."
	pyenv install --skip-existing $PY_VERSION
fi

#-------------------------
# DEVELOPMENT ENVIRONMENT
#-------------------------
echo ""
echo "*** SETUP DEVELOPMENT ENVIRONMENT ***"

# Check if Virtual environment for development is already there
if pyenv virtualenvs --bare | grep -q $DEV_ENV_NAME; then
	echo "Virtual environment <$DEV_ENV_NAME> already present."
else
	echo "Creating virtual environment <$DEV_ENV_NAME>..."
	pyenv virtualenv $PY_VERSION $DEV_ENV_NAME
fi

echo "Setting local virtual environment for pyenv..."
pyenv local $DEV_ENV_NAME

echo "Activate development environment..."
pyenv activate $DEV_ENV_NAME

echo "Installing requirements..."
pip install -r requirements.txt

#--------------------
# BUNDLE ENVIRONMENT
#--------------------
#echo ""
#echo "*** SETUP BUNDLE ENVIRONMENT ***"

# TODO: descend into bundle dir and setup the other venv.