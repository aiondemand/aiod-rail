```python
from OuterRail import Configuration, ExperimentManager

# Login
config = Configuration(host="https://rail.aiod.eu/api")
config.login()

# Specify experiment in a dictionary
experiment = {
    "name": "My experiment",
    "description": "Super demo Experiment",
    "publication_ids": [
        "pub_J5WL8fuaDHl0hUMMiTEk45Do"
    ],
    "experiment_template_id": "EX_TEMPLATE_ID",
    "dataset_ids": [
        "data_14H9yMvYxB0UQg6UALE94q4o"
    ],
    "model_ids": [
        "mdl_0JWgp63vVi5H8sw5ahkf4Mcx"
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
