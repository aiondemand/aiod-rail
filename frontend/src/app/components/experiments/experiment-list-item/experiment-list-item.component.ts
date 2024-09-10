import { Component, Input } from '@angular/core';
import { combineLatest, firstValueFrom } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { Experiment } from 'src/app/models/experiment';
import { Model } from 'src/app/models/model';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

@Component({
  selector: 'app-experiment-list-item',
  templateUrl: './experiment-list-item.component.html',
  styleUrls: ['./experiment-list-item.component.scss']
})
export class ExperimentListItemComponent {
  @Input() experiment: Experiment;

  dataset: Dataset;
  model: Model;

  constructor(private backend: BackendApiService, private snackBar: SnackBarService) { }

  onShowMore() {
    firstValueFrom(
      combineLatest([
        // TODO: Update to use arrays
        this.backend.getDataset(this.experiment.dataset_ids[0]),
        this.backend.getModel(this.experiment.model_ids[0])
      ]))
      .then(([dataset, model]) => {
        this.dataset = dataset;
        this.model = model;
      })
      .catch(err => {
        console.error(err);
        this.snackBar.showError("Failed to load experiment details");
      })
  }
}
