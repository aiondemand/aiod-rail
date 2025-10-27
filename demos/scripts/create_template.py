from OuterRail import Configuration, ExperimentTemplateManager
import json


def create_template(demo_dir: str, rail_host: str = "https://rail.aiod.eu/api") -> None:
    # Login
    config = Configuration(host=rail_host)
    config.login(persist=True)

    script_path = f"{demo_dir}/script.py"
    requirements_path = f"{demo_dir}/requirements.txt"

    with open(f"{demo_dir}/metadata.json") as f:
        metadata = json.load(f)["template"]
    with open(f"{demo_dir}/ids.json") as f:
        ids = json.load(f)
    with open(f"{demo_dir}/env_vars.json") as f:
        env_vars = json.load(f)


    # Specify template properties
    template_config = {
        "name": metadata["name"],
        "description": metadata["description"],
        "task": "TEXT_CLASSIFICATION",
        "datasets_schema": {
            "cardinality": "1-1"
        },
        "models_schema": {
            "cardinality": "1-1"
        },
        "envs_required": env_vars["required"],
        "envs_optional": env_vars["optional"],
        "is_public": metadata["is_public"]
    }


    # Create template
    template_manager = ExperimentTemplateManager(config)
    template = template_manager.create(
        template=(
            script_path,
            requirements_path,
            metadata["base_image"],
            template_config
        )
    )

    # Save template ID
    ids = {
        "template_id": template.id,
        "experiment_ids": {},
        "runs_ids": {}
    }
    with open(f"{demo_dir}/ids.json", "w") as f:
        json.dump(ids, f, ensure_ascii=False)

    print(f"Experiment Template (ID={template.id}) has been successfully created.")
    print("Now you need to wait for RAIL maintainers to approve your template to be usable.")


if __name__ == "__main__":
    create_template(
        # demo_dir="demos/use-cases/testing-use-case",
        demo_dir="demos/use-cases/sentiment-classification",
        rail_host="http://localhost:8000"
    )
