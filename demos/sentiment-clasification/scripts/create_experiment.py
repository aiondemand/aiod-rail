from OuterRail import Configuration, ExperimentManager, AssetManager
import json


# Login
config = Configuration()
config.login(persist=True)


with open("../metadata.json") as f:
    metadata = json.load(f, ensure_ascii=False)["experiment_1"]
with open("../ids.json") as f:
    ids = json.load(f)


# Retrieve IDs of assets you wish to use
asset_manager = AssetManager(config)
dataset_id = asset_manager.get_datasets(query=metadata["dataset_name"])[0].identifier
model_id = asset_manager.get_models(query=metadata["model_name"])[0].identifie


experiment_env_vars = [
    {"key": k, "value": v}
    for k, v in metadata["env_vars"]
]

# Specify experiment properties
experiment = {
    "name": metadata["name"],
    "description": metadata["description"],
    "publication_ids": [],
    "experiment_template_id": ids["template_id"],
    "dataset_ids": [
        dataset_id
    ],
    "model_ids": [
        model_id
    ],
    "env_vars": experiment_env_vars,
    "is_public": metadata["is_public"]
}


# Create experiment
exp_manager = ExperimentManager(config)
experiment = exp_manager.create(experiment=experiment)

# Execute experiment
run = experiment.run()


# Save experiment ID
ids["experimetn_id"] = experiment.id
ids["run_id"] = run.id
with open("../ids.json", "w") as f:
    json.dump(ids, f)
