```python
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

new_experiment = rail_client.experiments.create_experiment(experiment=experiment)


# Execute experiment
run = rail_client.experiments.run_experiment(id=new_experiment.id)
```
