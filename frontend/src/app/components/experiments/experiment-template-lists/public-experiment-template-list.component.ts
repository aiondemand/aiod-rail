import { Component } from '@angular/core';
import { ExperimentTemplateListBaseComponent } from './experiment-template-list-base.component';
import { Observable } from 'rxjs';
import { ExperimentTemplate } from 'src/app/models/experiment-template';

@Component({
  selector: 'app-public-experiment-template-list',
  templateUrl: './experiment-template-lists.component.html',
  styleUrls: ['./experiment-template-lists.component.scss']
})
export class PublicExperimentTemplateListComponent extends ExperimentTemplateListBaseComponent {

  protected override getExperimentTemplatesCount(): Observable<number> {
    return this.backend.getExperimentTemplatesCount(
      "",
      {
        finalized: true,
        approved: true,
        public: true,
        archived: false,
      }
    );
  }

  protected override getExperimentTemplates(): Observable<ExperimentTemplate[]> {
    return this.backend.getExperimentTemplates(
      "",
      {
        offset: this.pagination.pageIndex * this.pagination.pageSize,
        limit: this.pagination.pageSize
      },
      {
        finalized: true,
        approved: true,
        public: true,
        archived: false,
      }
    );
  }
}
