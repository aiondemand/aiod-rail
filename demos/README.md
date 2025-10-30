# Demos

In this folder we have a few demo examples of various Experiment Templates and their associated Experiments.

In the `scripts/` folder we find three scripts performing basic RAIL operations via Python SDK each of them
taking specific arguments from the terminal as an input. Specifically there is:
- `scripts/create_template.py`: a script to create a template
- `scripts/create_experiment.py`: a script to create and subsequently run an experiment
- `scripts/inspect_experiment.py`: a script to inspect logs of an experiment run and download a specific file

On the other hand, in the `use-cases/` folder we have a few demo tasks and associated metadata and attributes we use
to fill-in all the properties of either an Experiment Template or an Experiment. You're free to check any of these demos
to see what their metadata files consist of. Each use case folder contain the following:
- `env_vars.json`: a definition of environment variables, whether required or optional, we wish to use in our Experiment Template
- `metadata.json`: additional metadata necessary to specify when creating either an Experiment Template or an Experiment
    - There's always only one set of metadata values for the Experiment Template, whereas there may be multiple Experiments and their associated properties found in this JSON file
- `requirements.txt`: Python requirements needed for the main script of the Experiment Template to be run
- `script.py`: The main script of the Experiment Template to be run. In the script you may refer to the environment variables you have defined in the `env_vars.json` file to utilize them properly


# Setup (BLOCKING: You need to wait for RAIL's approval)
1. Install RAIL Python SDK: `pip install OuterRail`
1. Choose the demo use case you wish to run from the `use-cases` folder
1. To execute all the three scripts (**that need to be run from root of the project**) to do the following:
    - Run `scripts/create_template.py` with its arguments (default values work with a testing use case) to create an Experiment Template
    - Wait for one of the RAIL contributors to approve your Experiment Template
    - Run `scripts/create_experiment.py` with its arguments (default values work with a testing use case) to create an Experiment and subsequently run it as an Experiment Run
    - Wait for the Experiment Run to be finished
    - Run `scripts/inspect_experiment.py` with its arguments (default values work with a testing use case) to inspect the logs and download a file from the Experimert Run


# Setup (NON-BLOCKING)
*The only thing this setup differs from the one above is the use of already approved template to avoid waiting for approval from one of RAIL's maintainers*

1. Install RAIL Python SDK: `pip install OuterRail`
1. Choose the demo use case you wish to run from the `use-cases` folder
1. Within the demo folder you have chosen for your example (e.g., `use-cases/testing-use-case`), create a new file called `ids.json` containing the following data:
    ```
    {
        "template_id": "HERE_YOU_NEED_TO_PUT_TEMPLATE_ID_OF_ALREADY_APPROVED_TEMPLATE_YOU_WISH_TO_USE",
        "experiment_ids": {},
        "run_ids": {}
    }
    ```
1. To execute all the scripts (**that need to be run from root of the project**) but the Experiment Template creation process, do the following:
    - Run `scripts/create_experiment.py` with its arguments (default values work with a testing use case) to create an Experiment and subsequently run it as an Experiment Run
    - Wait for the Experiment Run to be finished
    - Run `scripts/inspect_experiment.py` with its arguments (default values work with a testing use case) to inspect the logs and download a file from the Experimert Run
