import requests

with open("./requirements.txt") as f:
    requirements_content = f.read()
with open("./script.py") as f:
    script_content = f.read()

template_to_create = {
    "name": "Text classification on HuggingFace platform",
    "description": "This Experiment template only supports text classification tasks, both the model and the dataset that are used to execute this experiment, need to be obtained from HuggingFace",
    "task": "TEXT_CLASSIFICATION",
    "datasets_schema": {"cardinality": "1-1"},
    "models_schema": {"cardinality": "1-1"},
    "envs_required": [
        {"name": "SPLIT_NAME", "description": "split name descr"},
    ],
    "envs_optional": [
        {"name": "WANDB_API_KEY", "description": "wandb api key descr"},
        {"name": "WANDB_BASE_URL", "description": "wandb base url descr"},
        {"name": "WANDB_ENTITY", "description": "wandb entity descr"},
        {"name": "WANDB_PROJECT", "description": "wandb project descr"},
        {"name": "WANDB_NAME", "description": "wandb name descr"},
    ],
    "base_image": "python:3.9",
    "script": script_content,
    "pip_requirements": requirements_content,
}

# don't forget to use correct port
response = requests.post(
    "http://localhost:8000/v1/experiment-templates", json=template_to_create
)

print(f"Experiment Template with ID: {response.json()['id']} has been added")
