```python
import json

# Get all runs of an experiment and select the latest one
all_experiment_runs =  new_experiment.get_runs()
last_run = all_experiment_runs[-1]

# Check status of the run
print(last_run.status)

# Once finished, you can see the logs of the Run
logs = json.loads(last_run.logs())

# Download run output file
# You can see the list of files in Web UI
# In this case, Experiment saves output.txt
# to 'output' directory.
# The results are downloaded to 'experiment-output' directory
last_run.download_file(filepath="output/output.txt", to_dir="experiment-output")
```
