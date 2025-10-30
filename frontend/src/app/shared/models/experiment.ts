import { ExperimentCreate as BackendExperimentCreate } from './backend-generated/experiment-create';
import { ExperimentResponse as BackendExperimentResponse } from './backend-generated/experiment-response';

export interface ExperimentCreate extends BackendExperimentCreate { }

export interface Experiment extends BackendExperimentResponse { }
