import { Component, Input } from '@angular/core';
import { Dataset } from 'src/app/models/dataset';
import { BackendApiService } from 'src/app/services/backend-api.service';

@Component({
  selector: 'app-dataset-list-item',
  templateUrl: './dataset-list-item.component.html',
  styleUrls: ['./dataset-list-item.component.scss']
})
export class DatasetListItemComponent {
  @Input() dataset: Dataset;
  showMore: boolean = false;
}
