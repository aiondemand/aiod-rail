import { EnvironmentVarDef as BackendEnvironmentVarDef } from './backend-generated/environment-var-def';
import { EnvironmentVar as BackendEnvironmentVar } from './backend-generated/environment-var';
import { EnvironmentVarCreate as BackendEnvironmentVarCreate } from './backend-generated/environment-var-create';

export interface EnvironmentVarDef extends BackendEnvironmentVarDef {}

export interface EnvironmentVarCreate extends BackendEnvironmentVarCreate {}

export interface EnvironmentVar extends BackendEnvironmentVar {}
