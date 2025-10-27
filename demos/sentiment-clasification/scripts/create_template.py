from OuterRail import Configuration, ExperimentTemplateManager
import json


# Login
config = Configuration()
config.login(persist=True)

script_path = "../script.py"
requirements_path = "../requirements.txt"

with open("../metadata.json") as f:
    metadata = json.load(f, ensure_ascii=False)["template"]
with open("../ids.json") as f:
    ids = json.load(f)
with open("../env_vars.json") as f:
    env_vars = json.load(f, ensure_ascii=False)


# Specify template properties
template_config = {
    "name": metadata["name"],
    "description": metadata["description"],
    "task": "OTHER",
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
ids["template_id"] = template.id
with open("../ids.json", "w") as f:
    json.dump(ids, f)
