# OuterRail

An SDK for AIoD - RAIL tool.

## What is RAIL

RAIL stands for: __Research and Innovation AI Lab__

RAIL is a tool that allows AI practitioners to explore and use AI assets 
directly in the AI on Demand platform (AIoD). RAIL is developed within the 
[AI4Europe project](https://www.ai4europe.eu) as one of the core services 
of the [AI on Demand platform](https://aiod.eu).

## Requirements

Python 3.9+

## Installation 
### pip install
The OuterRail package can simply be installed with pip via command:
```sh
pip install OuterRail
```
### Manual installation with wheel

## Usage

### Importing the package

You can import the SDK with:
```python
import OuterRail
```
### Configuration
For the SDK to work with underlying RAIL backend, you need to 
specify the URL of the RAIL as well as your API key.
The code for this would look something like:

```python
import os
from OuterRail import Configuration

os.environ["AIOD_RAIL_API_KEY"] = "your_api_key"
config = Configuration(host="http://localhost:8000")
```

### Examples:

#### Experiment Template Manager
```python
### EXPERIMENT TEMPLATE MANAGER TESTING
from OuterRail import ExperimentTemplateManager

template_manager = ExperimentTemplateManager(config)

# Get the count of available templates
template_manager.count()
# Get the list of Template instances
template_manager.get()
# Get a single template by its identifier
template_manager.get_by_id("identifier_here")

# Create new template
script_path = "script.py" # Adjust this
requirements_path = "requirements.txt" # Adjust this
base_image = "python:3.9"
template_config = {
    "name": "Example Template",
    "description": "Description of example template",
    "task": "TEXT_CLASSIFICATION",
    "datasets_schema": { "cardinality": "1-1" },
    "models_schema": { "cardinality": "1-1" },
    "envs_required": [ { "name": "SPLIT_NAME", "description": "name of a subset" }
    ],
    "envs_optional": [], "available_metrics": [ "accuracy" ],
    "is_public": True
}
new_template = template_manager.create((script_path, requirements_path, base_image, template_config))
```

#### Experiment Template class

```python
from OuterRail import ExperimentTemplateManager

# Get some experiment
template_manager = ExperimentTemplateManager(config)
template = template_manager.get()[0]

# Check if template is archived
print(template.is_archived)

# Archive template
template.archive(True)

# Update template (uses same params as create)
template.update((script_path, requirements_path, base_image, template_config)).name

# Delete template
template.delete()
```

### Experiment Manager
```python
from OuterRail import ExperimentManager

# Initialize
exp_manager = ExperimentManager(config)

# Get the count of experiments
exp_manager.count()
# Fetch only experiments that belong to you
experiments = exp_manager.get(mine=True)

# Create an example experiment
experiment_dict = {
    "name": "test123",
    "description": "321test",
    "is_public": True,
    "experiment_template_id": "685151f2d08da970a3a5d6ce",
    "dataset_ids": [ "data_000002AhzqHqOQwQLP0qCRds" ],
    "model_ids": [ "mdl_003Csk8QjNfE80c7g6Rt8yVb" ],
    "publication_ids": [],
    "env_vars": [ { "key": "SPLIT_NAME", "value": "Test"
        }
    ]
}
new_experiment = exp_manager.create(experiment_dict)
```

#### Experiment class

```python

from OuterRail import ExperimentManager

# Initialize
exp_manager = ExperimentManager(config)
# Get a single experiment that belongs to you
new_experiment = exp_manager.get(mine=True)[0]

# Check archivation
new_experiment.is_archived

# Archive experiment
new_experiment.archive(archive=False)

# Update experiment
update_dict = {
    "name": "NewAndImprovedName",
    "description": "321test",
    "is_public": True,
    "experiment_template_id": "685151f2d08da970a3a5d6ce",
    "dataset_ids": [ "data_000002AhzqHqOQwQLP0qCRds" ],
    "model_ids": [ "mdl_003Csk8QjNfE80c7g6Rt8yVb" ],
    "publication_ids": [],
    "env_vars": [ { "key": "SPLIT_NAME", "value": "Test"
                    }
                  ]
}
new_experiment.update(update_dict)

# Delete
new_experiment.delete()

# Count the runs of some an experiment
new_experiment.count_runs()

# Get list of runs
new_experiment.get_runs()
```

#### Experiment run class

```python
# Create an instance by running the experiment
exp_run = new_experiment.run()

# Check the state
print(exp_run.state)

# Check the logs of the run
print(f"exp run logs: {exp_run.logs()}")

# Delete a run
exp_run.delete()
```

## Author

This SDK was created at [KInIT](https://kinit.sk) by Jozef Barut.
