from argparse import ArgumentParser
from OuterRail import Configuration, ExperimentRunManager
import json
import os

def inspect_run(
    experiment_name: str, demo_dir: str,
    path_to_file_to_download: str, rail_host: str = "https://rail.aiod.eu/api"
) -> None:
    # Login
    config = Configuration(host=rail_host)
    config.login(persist=True)

    with open(f"{demo_dir}/ids.json") as f:
        ids = json.load(f)

    experiment_id = ids["experiment_ids"][experiment_name]
    run_id = ids["run_ids"][experiment_id][-1]

    run_manager = ExperimentRunManager(config)
    run = run_manager.get_by_id(run_id)


    os.makedirs(f"{demo_dir}/temp", exist_ok=True)

    # Save experiment run logs
    with open(f"{demo_dir}/temp/logs.txt", "w") as f:
        f.write(run.logs())
    print(f"Successfully downloaded logs of the experiment run (ID={run_id})")

    # Download a desired file if it exists
    try:
        run.download_file(path_to_file_to_download, f"{demo_dir}/temp")
        print(f"Successfully downloaded a file from the path: '{path_to_file_to_download}'")
    except:
        print(f"There was an error trying to download a file from the path: '{path_to_file_to_download}'")


def parse_arguments() -> dict:
    parser = ArgumentParser(description="Inpsect an Experiment Run logs and download one of its files.")

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
        "--path_to_file_to_download",
        type=str,
        default="output/metrics.json",
        help="A filepath within the REANA workflow to a file we wish to download (default: output/metrics.json)"
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
    inspect_run(**args)
