import { Component } from '@angular/core';
import { ExperimentListBaseComponent } from './experiment-list-base.component';
import { Observable } from 'rxjs/internal/Observable';
import { Experiment } from 'src/app/models/experiment';

@Component({
  selector: 'app-my-experiment-list',
  templateUrl: './experiment-lists.component.html',
  styleUrls: ['./experiment-lists.component.scss']
})
export class MyExperimentListComponent extends ExperimentListBaseComponent {
  protected override getExperimentsCount(): Observable<number> {
    return this.backend.getExperimentsCount(
      this.searchQuery,
      {
        mine: true
      }
    );
  }

  protected override getExperiments(): Observable<Experiment[]>  {
    return this.backend.getExperiments(
      this.searchQuery,
      {
        offset: this.pagination.pageIndex * this.pagination.pageSize,
        limit: this.pagination.pageSize
      },
      {
        mine: true,
      }
    );
  }
}
