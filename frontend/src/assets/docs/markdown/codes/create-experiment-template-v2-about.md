```python
from OuterRail import ExperimentTemplateManager

# Login
config = Configuration(host="http://localhost:8000")
config.login(username="username", password="password")

# Define all properties, script, base image and requirements.txt in your dictionary
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
template_manager = ExperimentTemplateManager(config)
template_manager.create(template=template_config)
```
