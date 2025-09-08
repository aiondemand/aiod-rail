import { EnvironmentVarDef as BackendEnvironmentVarDef } from './backend-generated/environment-var-def';
import { EnvironmentVar as BackendEnvironmentVar } from './backend-generated/environment-var';

export interface EnvironmentVarDef extends BackendEnvironmentVarDef {}

export interface EnvironmentVar extends BackendEnvironmentVar {}
