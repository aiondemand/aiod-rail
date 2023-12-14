import { Component } from '@angular/core';
import { ExperimentListBaseComponent } from './experiment-list-base.component';
import { Experiment } from 'src/app/models/experiment';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-all-experiment-list',
  templateUrl: './experiment-lists.component.html',
  styleUrls: ['./experiment-lists.component.scss']
})
export class AllExperimentListComponent extends ExperimentListBaseComponent {

  protected override getExperimentsCount(): Observable<number> {
    return this.backend.getExperimentsCount();
  }
  
  protected override updateExperiments(): Observable<Experiment[]> {
    return this.backend.getExperiments();
  }
}