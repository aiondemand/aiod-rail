import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { firstValueFrom } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmPopupComponent } from '../../general/popup/confirm-popup.component';
import { ConfirmPopupInput, ConfirmPopupResponse } from 'src/app/models/popup';
import { AuthService } from '../../../services/auth.service';


@Component({
  selector: 'app-experiment-template-detail',
  templateUrl: './experiment-template-detail.component.html',
  styleUrls: ['./experiment-template-detail.component.scss']
})
export class ExperimentTemplateDetailComponent {
  experimentTemplate: ExperimentTemplate;
  templateId: string;

  constructor(
    protected backend: BackendApiService,
    protected route: ActivatedRoute,
    protected router: Router,
    protected dialog: MatDialog,
    private authService: AuthService
  ) { }

  displayedEnvVarColumns: string[] = ['name', 'description'];

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.templateId = params["id"];

      firstValueFrom(this.backend.getExperimentTemplate(params["id"]))
        .then(template => this.experimentTemplate = template)
        .catch(err => console.error(err));
    });
  }

  editBtnClicked() {
    firstValueFrom(this.backend.getExperimentsOfTemplateCount(this.templateId, false))
      .then(count => {
        let existExperiments = count > 0;
        let routeParts = ['update'];
        let routeExtras = {
          relativeTo: this.route,
        };

        if (existExperiments) {
          let str = (
            "This Experiment Template is already utilized by some existing Experiment. " +
            "Modifying parameters that could change the template's behavior is restricted"
          );
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
              if (state == ConfirmPopupResponse.Yes) {
                this.router.navigate(routeParts, routeExtras);
              }
            });
        }
        else {
          this.router.navigate(routeParts, routeExtras);
        }
      })
      .catch(err => console.error(err));
  }

  deleteBtnClicked() {
    firstValueFrom(this.backend.getExperimentsOfTemplateCount(this.templateId, false))
      .then(count => {
        let existExperiments = count > 0;
        let routeParts = ["/experiments", "templates", "my"];

        let str = (
          existExperiments
          ?
          "This Experiment Template is already utilized by some existing Experiment. " +
          "You can no longer delete this template, but you can still forbid creation " +
          "of new experiments built upon this template by archiving it.\n\n" +
          "Do you wish ARCHIVE this experiment template?"
          :
          "Do you wish to DELETE this experiment template?"
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
            if (state == ConfirmPopupResponse.Yes && existExperiments) {
              firstValueFrom(this.backend.archiveExperimentTemplate(this.templateId, true))
                .then(_ => this.router.navigate(routeParts))
                .catch(err => console.error(err));
            }
            else if (state == ConfirmPopupResponse.Yes) {
              firstValueFrom(this.backend.deleteExperimentTemplate(this.templateId))
                  .then(_ => this.router.navigate(routeParts))
                  .catch(err => console.error(err));
            }
          });
      })
      .catch(err => console.error(err));
  }

  undoBtnClicked(): void {
    firstValueFrom(this.backend.archiveExperimentTemplate(this.templateId, false))
    .then(_ => {
      this.experimentTemplate.is_mine = true;
      this.experimentTemplate.is_archived = false;
    })
    .catch(err => console.error(err));
  }

  get isAdminUser(): boolean {
    return this.authService.isLoggedIn && this.authService.hasAdminRole;
  }

  approveBtnClicked(): void {
    firstValueFrom(this.backend.approveExperimentTemplate(this.templateId, true))
    .then(_ => {
      this.experimentTemplate.is_approved = true;
    })
    .catch(err => console.error(err));
  }
}
