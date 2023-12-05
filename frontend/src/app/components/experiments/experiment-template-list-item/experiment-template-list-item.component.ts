import { Component, Input } from '@angular/core';
import { ExperimentTemplate } from 'src/app/models/experiment-template';

@Component({
  selector: 'app-experiment-template-list-item',
  templateUrl: './experiment-template-list-item.component.html',
  styleUrls: ['./experiment-template-list-item.component.scss']
})
export class ExperimentTemplateListItemComponent {
  @Input() template: ExperimentTemplate;

}
