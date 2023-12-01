import { Component, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { Observable } from 'rxjs';
import { EnvironmentVarDef } from 'src/app/models/env-vars';


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

    // this.experimentTemplate$.subscribe(template => {
    //   let reqData: EnvironmentVarDef[] = [];
    //   for (let i = 0; i < template.envs_required.length; i++) {
    //     reqData.push({
    //       name: template.envs_required[i],
    //       description: this.reqDescriptions[i]
    //     });
    //   }

    //   let optData: EnvironmentVarDef[] = [];
    //   for (let i = 0; i < template.envs_optional.length; i++) {
    //     optData.push({
    //       name: template.envs_optional[i],
    //       description: this.optDescriptions[i]
    //     });
    //   }

      // this.reqEnvTableData = reqData;
      // this.optEnvTableData = optData;
  }

  getBaseDockerImage(dockerfile: string) {
    return dockerfile.split("\n")[0].split(" ")[1]
  }
}
