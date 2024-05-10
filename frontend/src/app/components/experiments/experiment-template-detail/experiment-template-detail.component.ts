import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { Observable, firstValueFrom } from 'rxjs';


@Component({
  selector: 'app-experiment-template-detail',
  templateUrl: './experiment-template-detail.component.html',
  styleUrls: ['./experiment-template-detail.component.scss']
})
export class ExperimentTemplateDetailComponent {
  experimentTemplate$: Observable<ExperimentTemplate>;
  templateId: string;
  existExperiments: boolean = false;
  
  constructor(
    protected backend: BackendApiService,
    protected route: ActivatedRoute,
    protected router: Router
  ) { }

  displayedEnvVarColumns: string[] = ['name', 'description'];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.templateId = params["id"];
      this.experimentTemplate$ = this.backend.getExperimentTemplate(params["id"]);

      firstValueFrom(this.backend.getExperimentsOfTemplateCount(params["id"]))
        .then(count => this.existExperiments = count > 0);
    });
  }

  editBtnClicked() {
    let queryParams = {  
      id: this.templateId
    };
    this.router.navigate(
      ['/experiments', 'templates', 'edit'],
      { queryParams: queryParams }
    );
  }

  deleteBtnClicked() {
    // TODO add logic for deleting
  }
}
