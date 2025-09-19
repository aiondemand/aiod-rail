experiment\_id

- Type: str

- Reference to an Experiment from which this Experiment Run originates.

retry\_count

- Type: int

- If an Experiment Run fails, it’s retried up to 3 times. This property represents the currency attempts.

state

- Type: Enum

  - CREATED: The Run has been created.

  - IN\_PROGRESS: The Run has been sent to REANA and is being executed or is waiting in the queue.

  - CRASHED: The Run crashed. There are currently 3 retry attempts.

  - FINISHED: The Run has successfully finished.

- Represents the state of the Experiment Run.

metrics

- Type: Dict\[str, float]

- Metrics logged in the experiment script.

public

- Type: bool

- If the Run and its results are available to other users.

archived

- Type: bool

- If the Run is archived.

mine

- Type: bool

- Whether or not the Experiment Run belongs to current user.

logs

- Type: str

- Logs logged by the script during the execution of the Docker container and Python script running inside.
