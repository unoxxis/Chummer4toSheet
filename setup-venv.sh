#!/bin/bash

# Setup two virtual environments for developing and bundling the tool.
PY_VERSION='3.9.6'
DEV_ENV_NAME='chumsheet-dev'
BUNDLE_ENV_NAME='chumsheet-bundle'

#-------------
# PYENV CHECK
#-------------
echo "Checking for pyenv..."
if ! command -v pyenv 1>/dev/null 2>&1; then
	echo 'pyenv and pyenv-virtualenv are required for this script!'
	echo 'Please see https://github.com/pyenv/pyenv and https://github.com/pyenv/pyenv-virtualenv'
	exit 99
fi
echo "Activating pyenv..."
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

#----------------
# PYTHON VERSION
#----------------

# Install the Python version, if not already installed
if pyenv versions --bare | grep -q "$PY_VERSION"; then
	echo "Python Version <$PY_VERSION> already present."
else
	echo "Installing Python version <$PY_VERSION>..."
	pyenv install --skip-existing "$PY_VERSION"
fi

#-------------------------
# DEVELOPMENT ENVIRONMENT
#-------------------------
echo ""
echo "*** SETUP DEVELOPMENT ENVIRONMENT ***"

echo "Checking if virtual environment $DEV_ENV_NAME already exists..."
./venv-tools/venv-check-version "$DEV_ENV_NAME" "$PY_VERSION" 1>/dev/null 2>&1
case $? in
	0)	echo "Virtual environment exists and has correct python version."
		;;
	1)  echo "Virtual environment exists but is for a different python version $(./venv-tools/venv-check-version "$DEV_ENV_NAME")!"
		# TODO Add an option to save and restore old version requirement data.
		read -p "Reinstall with correct python version $PY_VERSION? " -n 1 -r
		echo
		if [[ $REPLY =~ ^[Yy]$ ]]; then
			echo "Deleting old virtual environment..."
			pyenv virtualenv-delete "$DEV_ENV_NAME"
			createenv='yes'
		else
			echo "The script will still try to install correct dependencies."
			echo "However, it is not guaranteed that it will work if the versions"
			echo "differ by substantial amount."
		fi
		;;
	2)	echo "Virtual environment does not exist and will be created."
		createenv='yes'
esac

if [[ "$createenv" == "yes" ]]; then
	echo "Creating virtual environment <$DEV_ENV_NAME> ..."
	pyenv virtualenv "$PY_VERSION" "$DEV_ENV_NAME"
	createenv=
fi



echo "Setting local virtual environment for pyenv..."
pyenv local $DEV_ENV_NAME

echo "Activate development environment..."
pyenv activate $DEV_ENV_NAME

echo "Installing requirements..."
pip install -r requirements-dev.txt
echo "Installing LSP server to dev venv for Sublime Text PyLSP..."
pip install "python-lsp-server[all]" python-lsp-black mypy-ls pyls-isort types-PyYAML

#--------------------
# BUNDLE ENVIRONMENT
#--------------------
echo ""
echo "*** SETUP BUNDLE ENVIRONMENT ***"
cd bundle

# Check if Virtual environment for development is already there
if pyenv virtualenvs --bare | grep -q $BUNDLE_ENV_NAME; then
	echo "Virtual environment <$BUNDLE_ENV_NAME> already present."
else
	echo "Creating virtual environment <$BUNDLE_ENV_NAME>..."
	pyenv virtualenv $PY_VERSION $BUNDLE_ENV_NAME
fi

echo "Setting local virtual environment for pyenv..."
pyenv local $BUNDLE_ENV_NAME

echo "Activate bundle environment..."
pyenv activate $BUNDLE_ENV_NAME

echo "Installing requirements..."
pip install -r requirements-bundle.txt