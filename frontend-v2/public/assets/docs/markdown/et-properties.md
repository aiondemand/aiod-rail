name

- Type: str

- Short name of the Experiment Template. It should tell what the Experiment Template is capable of, for example “HuggingFace text summarization pipeline” or “Model training”

description

- Type: str

- A detailed description of the Experiment Template. It should tell what the template does, what models and datasets it is compatible with  (if they are not hardcoded) and what are the outputs.

script (Executable)

- Type: str

- An arbitrary Python script. This script will be executed within the Docker image once an Experiment derived from an Experiment Template is executed.

pip\_requirements (Dependencies)

- Type: str

- A list of Python packages that will be installed in a selected Docker image. It’s basically a string representing the requirements.txt file.

base\_image (Docker image)

- Type: str

- The script will be executed within this base Docker image. All the requirements will be installed in this base image.

envs\_required

- Type: List\[{name: str, description: str}]

- Mandatory environment variables that need to be defined when creating an Experiment from an Experiment Template. These variables are available in the script and can influence the execution of the script. The meaning of the variables is fully determined by script and its author. For example, if a script works with HuggingFace datasets and it needs to specify “split” of the data, an environment variable “split” should be defined and later used in the code.

envs\_optional

- Type: List\[{name: str, description: str}]

- Optional environment variables that may be defined when creating an Experiment from an Experiment Template. These variables are available in the script and can influence the execution of the script. The meaning of the variables is fully determined by script and its author. For example, if a script works with HuggingFace datasets and it needs to specify “split” of the data, an environment variable “split” should be defined and later used in the code. As these variables are optional, the script should run correctly even if they are not defined.

public

- Type: bool

- Defines whether the Experiment Template should be available (and visible) to other users.

state

- Type: Enum

  - CREATED: The Experiment Template has been created, but the Docker image representing it has been built yet.

  - IN\_PROGRESS: The Docker image representing the Experiment Template is being built.

  - CRASHED: The build of the Docked image failed.

  - FINISHED: The build of the Docked image has been successful and the image was uploaded to the registry. The Experiment Template is ready to be used.

- The build state of the Experiment Template.

archived

- Type: bool

- Whether the Experiment Template has been archived. It may be archived by its author. If archived, the Experiment Template won’t be available to other users and also no new Experiment can be created based on this Experiment Template.

approved

- Type: bool

- Whether the Experiment Template has been approved by RAIL administrators.

Besides these, there are variables that will be supported in the future:

datasets\_schema

- Type: { cardinality: Enum\[0-0, 1-1, 0-1, 1-n] }

- Defines how many datasets an Experiment Template works with. For example, if you define a Machine translation Experiment Template that enables you to translate multiple datasets at once, you can define _dataset\_schema = { cardinality: “1-n” }_ and the users will be able to select multiple datasets when creating an Experiment from the Experiment Template.

models\_schema

- Type: { cardinality: Enum\[0-0, 1-1, 0-1, 1-n] }

- Defines how many models an Experiment Template works with. For example, if you define a Semantic segmentation evaluation Experiment Template that enables you to evaluate performance of multiple image segmentation models on the same dataset, you can define _dataset\_schema = { cardinality: “1-n” }_ and the users will be able to select multiple models when creating an Experiment from the Experiment Template.

task

- Type: Enum

- In the future, this property will be used to restrict selection of models when creating an Experiment from an Experiment Template.
