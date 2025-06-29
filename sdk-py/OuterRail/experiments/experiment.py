from OuterRail.experiments import ExperimentTemplate

class Experiment(ExperimentTemplate):

    def __init__(self, ):
        super().__init__()
        pass

    @classmethod
    def create(cls, experiment_json: dict):
        response = {}
        return Experiment(response)

    def run(self):
        pass

