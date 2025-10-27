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


if __name__ == "__main__":
    inspect_run(
        experiment_name="experiment_sst2",
        demo_dir="demos/use-cases/sentiment-classification",
        path_to_file_to_download="output/predictions.csv",
        rail_host="http://localhost:8000"
    )
