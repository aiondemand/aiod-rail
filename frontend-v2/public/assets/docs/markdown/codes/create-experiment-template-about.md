```python
from OuterRail import Configuration, ExperimentTemplateManager

# Login
config = Configuration(host="https://rail.aiod.eu/api")
config.login()


# Use existing Python script as Experiment script
script_path = "./script.py"
# Load requirements (libs) from file
requirements_path = "./requirements.txt"
# Experiment Template base Docker image
base_image = "python:3.9"

template_config = {
    "name": "Cobra Experiment Template",
    "description": "Simple demo experiment template",
    "task": "TEXT_CLASSIFICATION",
    "datasets_schema": {
        "cardinality": "1-1"
    },
    "models_schema": {
        "cardinality": "1-1"
    },
    "envs_required": [
        {
            "name": "SPLIT_NAME",
            "description": "name of a subset",
            "is_secret": False
        }
    ],
    "envs_optional": [
        {
            "name": "BATCH_SIZE",
            "description": "Size of a batch",
            "is_secret": False
        }
    ],
    "is_public": True
}

# Create template
template_manager = ExperimentTemplateManager(config)
template_manager.create(template=(script_path, requirements_path, base_image, template_config))
```
