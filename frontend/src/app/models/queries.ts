export interface PageQueries {
  offset?: number;
  limit?: number;
}

export interface ExperimentTemplateQueries {
  only_mine?: boolean;
  include_pending?: boolean;
  only_finalized?: boolean;
  only_usable?: boolean,
  only_public?: boolean,
}

export interface ExperimentQueries {
  // TODO: Add query parameters
}
