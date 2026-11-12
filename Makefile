#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = fds_course
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python3
VENV_DIR = fds_venv
CONDA_ENV = $(PROJECT_NAME)
DATA_DIR = data
NOTEBOOK_DIR = notebooks

#################################################################################
# ENVIRONMENT                                                                   #
#################################################################################

## Create a local virtual environment and install requirements
create_venv:
	$(PYTHON_INTERPRETER) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo ">>> venv ready. Activate with: source $(VENV_DIR)/bin/activate"

## Create a conda environment and install requirements
create_conda:
	conda create -y --name $(CONDA_ENV) python=$(PYTHON_VERSION)
	conda run -n $(CONDA_ENV) pip install -r requirements.txt
	@echo ">>> conda env ready. Activate with: conda activate $(CONDA_ENV)"

## Install requirements into the active environment
requirements:
	$(PYTHON_INTERPRETER) -m pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

#################################################################################
# DATA                                                                          #
#################################################################################

## Fetch all course datasets into data/ (raw, no processing)
data_gen:
	$(PYTHON_INTERPRETER) data_gen.py fetch --all

## Fetch a single dataset, e.g. make data_gen_one NAME=penguins
data_gen_one:
	$(PYTHON_INTERPRETER) data_gen.py fetch --name $(NAME)

## List datasets registered in data_gen.py
data_list:
	$(PYTHON_INTERPRETER) data_gen.py list

## Run preprocessing (cleaned Parquet files written to data/processed/)
preprocess:
	$(PYTHON_INTERPRETER) preprocessing.py

#################################################################################
# NOTEBOOKS                                                                     #
#################################################################################

## Launch JupyterLab from the repo root
lab:
	jupyter lab

## Execute every week's lecture notebook in place (smoke test)
run_notebooks:
	for nb in $(NOTEBOOK_DIR)/week_*/*.ipynb; do \
		jupyter nbconvert --to notebook --execute --inplace $$nb; \
	done

## Strip outputs from every notebook in the repo (nbstripout)
nbstripout:
	find . -name "*.ipynb" -not -path "./.ipynb_checkpoints/*" -not -path "*/.ipynb_checkpoints/*" \
		-not -path "./$(VENV_DIR)/*" -print0 | xargs -0 -r nbstripout

## Install nbstripout as a git filter so outputs are stripped on every commit
nbstripout_install:
	nbstripout --install --attributes .gitattributes

#################################################################################
# SITE                                                                          #
#################################################################################

## Render the Quarto book into _site/ (executes notebooks once; later renders use _freeze/)
render_site:
	quarto render

## Serve the site locally with live reload
preview_site:
	quarto preview

#################################################################################
# RELEASE                                                                       #
#################################################################################

STUDENT_DIR = ../fds_course_students

## Build the student-facing copy (no solution keys, no quiz banks) into ../fds_course_students
export_students:
	$(PYTHON_INTERPRETER) tools/export_students.py . $(STUDENT_DIR)
	@echo ">>> review $(STUDENT_DIR), then commit and push from there."

#################################################################################
# HOUSEKEEPING                                                                  #
#################################################################################

## Remove Python caches and checkpoints
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

## Lint with ruff
lint:
	ruff check .

## Format with black
format:
	black .

#################################################################################
# SELF-DOCUMENTING HELP                                                         #
#################################################################################

.DEFAULT_GOAL := help

## Show this help
help:
	@echo ""
	@echo "$(PROJECT_NAME) - available targets:"
	@echo ""
	@awk '/^## / { desc = substr($$0, 4); next } \
	      /^[a-zA-Z_]+:/ && desc { printf "  \033[36m%-18s\033[0m %s\n", $$1, desc; desc = "" }' $(MAKEFILE_LIST) | sed 's/://'
	@echo ""

.PHONY: create_venv create_conda requirements data_gen data_gen_one data_list \
        preprocess lab run_notebooks nbstripout nbstripout_install render_site preview_site export_students clean lint format help