export interface PageQueries {
  offset?: number;
  limit?: number;
}

export interface ExperimentTemplateQueries {
  mine?: boolean;
  finalized?: boolean;
  approved?: boolean;
  archived?: boolean,
  public?: boolean,
}

export interface ExperimentQueries {
  mine?: boolean;
  archived?: boolean;
  public?: boolean;
}
