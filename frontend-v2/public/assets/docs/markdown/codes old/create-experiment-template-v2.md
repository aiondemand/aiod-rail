```python
from aiod_rail_sdk import Configuration
from aiod_rail_sdk.clients import RailClient


RAIL_API_URI = "https://rail.aiod.eu/api"
os.environ["AIOD_RAIL_API_KEY"] = "YOUR_RAIL_API_KEY"

config = Configuration(host=RAIL_API_URI)
rail_client = RailClient(config)

# Define all properties, script, base image and
# requirements.txt in Dictionary
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
    "is_public": True,
    "pip_requirements": "numpy==1.25.0\nscikit-learn==1.2.2",
    "script": "import os\n\nprint(os.getenv('SPLIT_NAME'))",
    "base_image": "python:3.9"
}

# Create template
rail_client.experiments_templates.create_experiment_template(
    template=template_config
)
```
