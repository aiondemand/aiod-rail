```python
from OuterRail import Configuration, ExperimentManager

# Login
config = Configuration(host="http://rail/backend/url")
config.login(username="username", password="password")

# Specify experiment in a dictionary
experiment = {
    "name": "My experiment",
    "description": "Super demo Experiment",
    "publication_ids": [],
    "experiment_template_id": "EX_TEMPLATE_ID",
    "dataset_ids": [
        "1"
    ],
    "model_ids": [
        "2"
    ],
    "env_vars": [
        {
            "key": "SPLIT_NAME",
            "value": "train"
        }
    ],
    "is_public": True
}

# Create experiment
exp_manager = ExperimentManager(config)
new_experiment = exp_manager.create(experiment=experiment)

# Execute experiment
run = new_experiment.run()
```
