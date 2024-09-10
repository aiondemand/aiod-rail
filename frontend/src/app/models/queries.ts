export interface PageQueries {
  offset?: number;
  limit?: number;
}

export interface ExperimentTemplateFilter {
  mine?: boolean;
  finalized?: boolean;
  approved?: boolean;
  archived?: boolean,
  public?: boolean,
}

export interface ExperimentFilter {
  mine?: boolean;
  archived?: boolean;
  public?: boolean;
}
