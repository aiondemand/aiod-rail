export type QueryOperator = 'AND' | 'OR';

export const QueryOperator = {
    And: 'AND' as QueryOperator,
    Or: 'OR' as QueryOperator
};


export interface PageQueries {
    offset?: number;
    limit?: number;
}

export interface ExperimentTemplateQueries { 
    include_mine?: boolean;
    include_approved?: boolean;
    query_operator?: QueryOperator;
}

export interface ExperimentQueries {
    include_mine?: boolean;
    query_operator?: QueryOperator;
}