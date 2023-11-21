import requests

with open("./Dockerfile") as f:
    dockerfile_content = f.read()
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
    "envs_required": ["SPLIT_NAME", "HF_HOME"],
    "envs_optional": [
        "WANDB_API_KEY",
        "WANDB_BASE_URL",
        "WANDB_ENTITY",
        "WANDB_PROJECT",
        "WANDB_NAME",
    ],
    "available_metrics": ["accuracy", "precision_macro", "recall_macro", "f1_macro"],
    "dockerfile": dockerfile_content,
    "script": script_content,
    "pip_requirements": requirements_content,
}

# don't forget to use correct port
response = requests.post(
    "http://localhost:8000/v1/experiment-templates", json=template_to_create
)

print(f"Experiment Template with ID: {response.json()['id']} has been added")
