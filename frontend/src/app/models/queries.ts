export interface PageQueries {
  offset?: number;
  limit?: number;
}

export interface ExperimentTemplateQueries {
  only_mine?: boolean;
  only_finalized?: boolean;
  only_usable?: boolean,
  only_public?: boolean,
}

export interface ExperimentQueries {
  only_mine?: boolean;
  only_usable?: boolean;
  only_public?: boolean;
}
