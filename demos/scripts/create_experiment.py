from OuterRail import Configuration, ExperimentManager, AssetManager
import json


def create_and_run_experiment(
    experiment_name: str, demo_dir: str, rail_host: str = "https://rail.aiod.eu/api"
) -> None:
    # Login
    config = Configuration(host=rail_host)
    config.login(persist=True)


    with open(f"{demo_dir}/metadata.json") as f:
        metadata = json.load(f)["experiments"][experiment_name]
    with open(f"{demo_dir}/ids.json") as f:
        ids = json.load(f)


    # Retrieve IDs of assets you wish to use
    asset_manager = AssetManager(config)
    dataset_id = asset_manager.get_datasets(query=metadata["dataset_name"], limit=10)[0].identifier
    model_id = asset_manager.get_models(query=metadata["model_name"], limit=10)[0].identifier


    experiment_env_vars = [
        {"key": k, "value": v}
        for k, v in metadata["env_vars"].items()
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

    print(f"Experiment (ID={experiment.id}) has been successfully created.")

    # Execute experiment
    run = experiment.run()
    print(f"Experiment Run (ID={run.id}) has been successfully created.")


    # Save experiment ID
    ids["experiment_ids"][experiment_name] = experiment.id
    ids["run_ids"][experiment.id] = [run.id]
    with open(f"{demo_dir}/ids.json", "w") as f:
        json.dump(ids, f)


if __name__ == "__main__":
    create_and_run_experiment(
        experiment_name="experiment_sst2",
        # demo_dir="demos/use-cases/testing-use-case",
        demo_dir="demos/use-cases/sentiment-classification",
        rail_host="http://localhost:8000"
    )
