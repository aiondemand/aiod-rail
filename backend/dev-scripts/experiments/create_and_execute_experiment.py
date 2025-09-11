import requests

response = requests.get("http://localhost:8000/v1/experiment-templates")
experiment_template_id = response.json()[0]["id"]

# TODO: Create Experiment
experiment = {
    "name": "MyExperiment #1",
    "description": "Train Roberta sentiment classifier on sample dataset",
    "dataset_ids": [51242],
    "model_ids": [2],
    "env_vars": [{"name": "SPLIT_NAME", "value": "train"}],
    "metrics": ["accuracy", "f1_macro"],
    "experiment_template_id": experiment_template_id,
}
#
# response = requests.post("http://localhost:8000/v1/experiments", json=experiment)
# experiment_id = response.json()["id"]
# print(
#     f"Created experiment '{experiment_id}' based on template '{experiment_template_id}'"
# )

# Execute experiment
experiment_id = "<YOUR_EXPERIMENT_ID>"
response = requests.post(f"http://localhost:8000/v1/experiments/{experiment_id}/execute")
experiment_run_id = response.json()["id"]
print(f"Executing experiment run '{experiment_run_id}'")
