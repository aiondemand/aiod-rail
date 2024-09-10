```python
from aiod_rail_sdk import Configuration
from aiod_rail_sdk.clients import RailClient


RAIL_API_URI = "https://rail.aiod.eu/api"
os.environ["AIOD_RAIL_API_KEY"] = "YOUR_RAIL_API_KEY"

config = Configuration(host=RAIL_API_URI)
rail_client = RailClient(config)


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
            "description": "name of a subset"
        }
    ],
    "envs_optional": [],
    "available_metrics": [
        "accuracy"
    ],
    "is_public": True
}

# Create template
rail_client.experiments_templates.create_experiment_template(
    template=(script_path, requirements_path, base_image, template_config)
)
```