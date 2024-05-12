import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { Observable, firstValueFrom, min } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmPopupComponent } from '../../general/popup/confirm-popup.component';
import { ConfirmPopupInput } from 'src/app/models/popup-input';


@Component({
  selector: 'app-experiment-template-detail',
  templateUrl: './experiment-template-detail.component.html',
  styleUrls: ['./experiment-template-detail.component.scss']
})
export class ExperimentTemplateDetailComponent {
  experimentTemplate$: Observable<ExperimentTemplate>;
  templateId: string;
  existExperiments: boolean = false;
  isTemplateMine: boolean = false;
  
  constructor(
    protected backend: BackendApiService,
    protected route: ActivatedRoute,
    protected router: Router,
    protected dialog: MatDialog
  ) { }

  displayedEnvVarColumns: string[] = ['name', 'description'];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.templateId = params["id"];
      this.experimentTemplate$ = this.backend.getExperimentTemplate(params["id"]);

      firstValueFrom(this.backend.getExperimentsOfTemplateCount(params["id"]))
        .then(count => this.existExperiments = count > 0)
        .catch(err => console.error(err));
      firstValueFrom(this.backend.isExperimentTemplateMine(params["id"]))
        .then(mine => this.isTemplateMine = mine)
        .catch(err => console.error(err));
    });
  }

  editBtnClicked() {
    let routeParts = ['/experiments', 'templates', 'edit'];
    let queryParams = {  
      id: this.templateId
    };
    let routeExtras = { queryParams: queryParams };

    if (this.existExperiments) {
      let str = (
        "Since there exist Experiments that utilize this particular template, " + 
        "you cannot further modify the parameters that could change the template behavior."
      )
      let popupInput: ConfirmPopupInput = {
        message: str,
        acceptBtnMessage: "Continue"
      };
      firstValueFrom(this.dialog.open(ConfirmPopupComponent, {
        maxWidth: '450px',
        width: '100%',
        autoFocus: false,
        data: popupInput
      }).afterClosed())
        .then(state => {
          if (state) {
            this.router.navigate(routeParts, routeExtras);
          }
        });
    }
    else {
      this.router.navigate(routeParts, routeExtras);
    }  
  }

  deleteBtnClicked() {
    let routeParts = ["/experiments", "templates", "my"];
    
    let str = (
      this.existExperiments 
      ?
      "Since there exist Experiments that utilize this particular template, you can no longer delete this template. " +
      "However, you can still forbid a creation of new experiments built upon this template. " + 
      "Do you wish to make this template unusable for others and you henceforth?" 
      : 
      "Do you wish to delete this experiment template?"
    );  
    let popupInput: ConfirmPopupInput = {
      message: str,
      acceptBtnMessage: "Yes",
      declineBtnMessage: "No"
    }
    firstValueFrom(this.dialog.open(ConfirmPopupComponent, {
      maxWidth: '450px',
      width: '100%',
      autoFocus: false,
      data: popupInput
    }).afterClosed())
      .then(state => {
        if (state && this.existExperiments) {
          firstValueFrom(this.backend.setExperimentTemplateUsability(this.templateId, false))
            .then(_ => this.router.navigate(routeParts))
            .catch(err => console.error(err));
        }
        else if (state) {
          firstValueFrom(this.backend.deleteExperimentTemplate(this.templateId))
              .then(_ => this.router.navigate(routeParts))
              .catch(err => console.error(err));
        }
      });
  }
}
