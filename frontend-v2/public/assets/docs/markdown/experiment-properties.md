experiment\_template\_id (Experiment Template)

- Type: str

- ID of the Experiment Template this experiment is derived from.

name

- Type: str

- Short name of the Experiment.

description

- Type: str

- A detailed description of the Experiment. It should tell what the experiment does and what its purpose is. For example “Training and evaluation of our new Model X on dataset Y”.

dataset\_ids

- Type: List\[str]

- AIoD IDs of dataset or datasets that will be used in the Experiment. The script (defined in Experiment Template) will have access to these IDs and the names of the datasets in the environment variables.

model\_ids

- Type: List\[str]

- AIoD IDs of dataset or models that will be used in the Experiment. The script (defined in Experiment Template) will have access to these IDs and the names of the models in the environment variables.

publication\_ids

- Type: List\[str]

- AIoD IDs of publications. These do not influence the execution of the Experiment, but they express relation of the experiment to 0-n publications (e.g. the link to the Experiment can be shared with the publication as a reproducible reference).

env\_vars

- Type: List\[{key: str, value: str}]

- Values of environment variables defined in the Experiment Template (both required and optional). These values will be accessible to the script defined in Experiment Template through environment variables.

public

- Type: bool

- Defines whether the Experiment should be available (and visible) to other users.
