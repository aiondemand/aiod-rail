import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-experiment-template-detail',
  templateUrl: './experiment-template-detail.component.html',
  styleUrls: ['./experiment-template-detail.component.scss']
})
export class ExperimentTemplateDetailComponent {
  experimentTemplate$: Observable<ExperimentTemplate>;
  
  constructor(
    protected backend: BackendApiService,
    protected route: ActivatedRoute,
    protected router: Router
  ) { }

  displayedEnvVarColumns: string[] = ['name', 'description'];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.experimentTemplate$ = this.backend.getExperimentTemplate(params["id"]);
    });
  }

  getBaseDockerImage(dockerfile: string) {
    return dockerfile.split("\n")[0].split(" ")[1]
  }
}
