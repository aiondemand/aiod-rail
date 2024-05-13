import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Dataset } from 'src/app/models/dataset';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

@Component({
  selector: 'app-save-remove-dataset-button',
  templateUrl: './save-remove-dataset-button.component.html',
  styleUrls: ['./save-remove-dataset-button.component.scss']
})
export class SaveRemoveDatasetButtonComponent {
  @Input() dataset: Dataset;

  constructor(
    private backend: BackendApiService,
    private snackBar: SnackBarService
  ) { }

  saveToMyDatasets(dataset: Dataset) {
    this.backend.saveDataset(dataset).subscribe({
      complete: () => {
        dataset.is_in_my_saved = true;
        this.snackBar.show('Dataset was saved')
      },
      error: () => this.snackBar.showError('Error saving dataset')
    });
  }

  removeFromMyDatasets(dataset: Dataset) {
    this.backend.removeFromSaved(dataset).subscribe({
      complete: () => {
        dataset.is_in_my_saved = false;
        this.snackBar.show('Dataset was removed from saved');
      },
      error: () => console.error('Error removing dataset')
    });
  }

}
