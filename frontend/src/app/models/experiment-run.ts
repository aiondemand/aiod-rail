import { ExperimentRunResponse as BackendExperimentRunResponse } from './backend-generated/experiment-run-response';
import { ExperimentRunDetails as BackendExperimentRunDetails } from './backend-generated/experiment-run-details';

export interface ExperimentRun extends BackendExperimentRunResponse { }

export interface ExperimentRunDetails extends BackendExperimentRunDetails { }
