import { Component } from '@angular/core';
import { ExperimentTemplateListBaseComponent } from './experiment-template-list-base.component';
import { Observable } from 'rxjs';
import { ExperimentTemplate } from 'src/app/models/experiment-template';

@Component({
  selector: 'app-all-experiment-template-list',
  templateUrl: './experiment-template-lists.component.html',
  styleUrls: ['./experiment-template-lists.component.scss']
})
export class AllExperimentTemplateList extends ExperimentTemplateListBaseComponent {

  protected override getExperimentTemplatesCount(): Observable<number> {
    return this.backend.getExperimentTemplatesAllViewCount();
  }
  
  protected override updateExperimentTemplates(): Observable<ExperimentTemplate[]> {
    return this.backend.getExperimentTemplatesAllView(this.pagination.pageIndex * this.pagination.pageSize,
      this.pagination.pageSize
    );
  }
}