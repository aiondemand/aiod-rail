from OuterRail import Configuration, ExperimentRunManager
import json
import os


# Login
config = Configuration()
config.login(persist=True)


with open("../ids.json") as f:
    ids = json.load(f)

run_manager = ExperimentRunManager(config)
run = run_manager.get_by_id(ids["run_id"])


os.makedirs("./temp", exist_ok=True)

# Save experiment run logs
with open("./temp/logx.txt", "w") as f:
    f.write(run.logs())

# Download metrics.json file if it exists
try:
    run.download_file("output-dir/metrics.json", "./temp")
    pass
except:
    pass
