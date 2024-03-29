import { Component } from '@angular/core';
import { ExperimentTemplateListBaseComponent } from './experiment-template-list-base.component';
import { Observable } from 'rxjs';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { QueryOperator } from 'src/app/models/queries';

@Component({
  selector: 'app-my-experiment-template-list',
  templateUrl: './experiment-template-lists.component.html',
  styleUrls: ['./experiment-template-lists.component.scss']
})
export class MyExperimentTemplateList extends ExperimentTemplateListBaseComponent {

  protected override getExperimentTemplatesCount(): Observable<number> {
    return this.backend.getExperimentTemplatesCount({ 
      include_mine: true,
      query_operator: QueryOperator.Or
    });
  }
  
  protected override updateExperimentTemplates(): Observable<ExperimentTemplate[]> {
    return this.backend.getExperimentTemplates(
      {
        offset: this.pagination.pageIndex * this.pagination.pageSize,
        limit: this.pagination.pageSize
      },
      {
        include_mine: true,
        query_operator: QueryOperator.Or
      }
    );
  }
}