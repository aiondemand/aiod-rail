```python
all_experiment_runs = rail_client.experiments.get_experiment_runs(id=new_experiment.id)

last_run = all_experiment_runs[-1]

# Check status of the run
print(last_run.status)

# Once finished, you can see the logs of the Run
logs = json.loads(rail_client.experiments.logs_experiment_run(run.id))

# Download run output file
# You can see the list of files in Web UI
# In this case, Experiment saves output.txt
# to 'output' directory.
# The results are downloaded to 'experiment-output' directory
rail_client.experiments.download_experiment_run(
    id=run.id, 
    filepath="output/output.txt", 
    to_dir="experiment-output"
)
```