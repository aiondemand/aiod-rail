import { ExperimentTemplateCreate as BackendExperimentTemplateCreate } from './backend-generated/experiment-template-create';
import { ExperimentTemplateResponse as BackendExperimentTemplateResponse } from './backend-generated/experiment-template-response';

export interface ExperimentTemplateCreate extends BackendExperimentTemplateCreate { }

export interface ExperimentTemplate extends BackendExperimentTemplateResponse { }