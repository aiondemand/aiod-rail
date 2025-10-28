from OuterRail import Configuration, ExperimentManager, AssetManager
import json
from argparse import ArgumentParser


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


def parse_arguments() -> dict:
    parser = ArgumentParser(description="Create an Experiment and subsequently run it as an Experiment Run.")

    parser.add_argument(
        "--experiment_name",
        type=str,
        default="experiment",
        help="Name of the experiment you wish to create. The eligible names of the experiments are the key values within the 'experiments' object in the metadata.json file pertaining to the particular use case folder you use (default: experiment)"
    )
    parser.add_argument(
        "--demo_dir",
        type=str,
        default="demos/use-cases/testing-use-case",
        help="Path to the demo directory containing all the demo setup. Path is relative to the root of the RAIL project (default: demos/use-cases/testing-use-case)"
    )
    parser.add_argument(
        "--rail_host",
        type=str,
        default="https://rail.aiod.eu/api",
        help="RAIL host URL (default: https://rail.aiod.eu/api)"
    )

    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    args = parse_arguments()
    create_and_run_experiment(**args)
