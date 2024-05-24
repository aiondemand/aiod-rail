import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { ExperimentTemplateListBaseComponent } from '../../experiments/experiment-template-lists/experiment-template-list-base.component';

@Component({
  selector: 'app-all-experiment-template-list',
  templateUrl: '../../experiments/experiment-template-lists/experiment-template-lists.component.html',
  styleUrls: ['../../experiments/experiment-template-lists/experiment-template-lists.component.scss']
})
export class AllExperimentTemplateListComponent extends ExperimentTemplateListBaseComponent {

  protected override getExperimentTemplatesCount(): Observable<number> {
    return this.backend.getExperimentTemplatesCount(
      "",
      {
      }
    );
  }

  protected getExperimentTemplates(): Observable<ExperimentTemplate[]> {
    return this.backend.getExperimentTemplates(
      "",
      {
        offset: this.pagination.pageIndex * this.pagination.pageSize,
        limit: this.pagination.pageSize
      },
      {
      }
    );
  }
}
