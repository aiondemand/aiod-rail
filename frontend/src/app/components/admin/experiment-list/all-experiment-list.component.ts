import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { Experiment } from 'src/app/models/experiment';
import { ExperimentListBaseComponent } from "../../experiments/experiment-lists/experiment-list-base.component";

@Component({
  selector: 'app-all-experiment-list',
  templateUrl: '../../experiments/experiment-lists/experiment-lists.component.html',
  styleUrls: ['../../experiments/experiment-lists/experiment-lists.component.scss']
})
export class AllExperimentListComponent extends ExperimentListBaseComponent {

  protected override getExperimentsCount(): Observable<number> {
    return this.backend.getExperimentsCount(
      "",
      {
      }
    );
  }

  protected getExperiments(): Observable<Experiment[]> {
    return this.backend.getExperiments(
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
