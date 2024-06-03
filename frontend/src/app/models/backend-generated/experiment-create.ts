/**
 * AIoD - RAIL
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.20240603-beta
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { EnvironmentVar } from './environment-var';


export interface ExperimentCreate {
  name: string;
  description: string;
  is_public: boolean;
  experiment_template_id: string;
  dataset_ids: Array<string>;
  model_ids: Array<string>;
  publication_ids?: Array<string>;
  env_vars: Array<EnvironmentVar>;
}

