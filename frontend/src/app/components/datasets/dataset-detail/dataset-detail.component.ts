import { Component, Input, ViewChild } from '@angular/core';
import { Observable } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { BackendApiService } from 'src/app/services/backend-api.service';

@Component({
  selector: 'app-dataset-detail',
  templateUrl: './dataset-detail.component.html',
  styleUrls: ['./dataset-detail.component.scss']
})
export class DatasetDetailComponent {
  dataset$: Observable<Dataset>;
  showFullDescription = false;

  constructor(private backend: BackendApiService) { }

  @Input()
  set id(id: string) {
    this.dataset$ = this.backend.getDataset(id);
  }


}
