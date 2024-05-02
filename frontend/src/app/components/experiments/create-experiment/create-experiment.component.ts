import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSelectChange } from '@angular/material/select';
import { Router } from '@angular/router';
import { Observable, Subscription, catchError, debounceTime, firstValueFrom, of, startWith, switchMap } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { EnvironmentVar } from 'src/app/models/env-vars';
import { ExperimentCreate } from 'src/app/models/experiment';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { Model } from 'src/app/models/model';
import { Publication } from 'src/app/models/publication';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

@Component({
  selector: 'app-create-experiment',
  templateUrl: './create-experiment.component.html',
  styleUrls: ['./create-experiment.component.scss']
})
export class CreateExperimentComponent implements OnInit {
  experimentForm = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    publications: this.fb.array(Array<Publication>()),
    dataset: new FormControl<Dataset | string>('', Validators.required),
    model: new FormControl<Model | string>('', Validators.required),
    metrics: this.fb.group({}),
    envs_required: this.fb.group({}),
    envs_optional: this.fb.group({}),
    experimentTemplate: new FormControl<ExperimentTemplate | null>(null, Validators.required)
  });


  error: string = '';

  experimentTemplates$: Observable<ExperimentTemplate[]>;
  publications$: Observable<Publication[]>;
  models$: Observable<Model[]> | undefined;
  datasets$: Observable<Dataset[]> | undefined;

  subscriptions: (Subscription | undefined)[] = [];

  constructor(
    private fb: FormBuilder,
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.experimentTemplates$ = this.backend.getExperimentTemplates({}, {
      only_finalized: true
    }).pipe(
      catchError(err => {
        if (err.status == 401) {
          this.snackBar.showError("An authorization error occurred. Try logging out and then logging in again.");
        }
        else {
          this.error = err.message;
          this.snackBar.showError("Couldn't load experiment types");
        }
        return of([]);
      })
    );

    this.models$ = this.model?.valueChanges.pipe(
      debounceTime(300), // Debounce to avoid frequent requests
      startWith(""),
      switchMap(value => this.modelAutocompleteFilter(value)),
      catchError(err => {
        this.error = err.message;
        this.snackBar.showError("Couldn't load models");
        return of([]);
      })
    );

    this.datasets$ = this.dataset?.valueChanges.pipe(
      debounceTime(300), // Debounce to avoid frequent requests
      startWith(""),
      switchMap(value => this.datasetAutocompleteFilter(value)),
      catchError(err => {
        this.error = err.message;
        this.snackBar.showError("Couldn't load datasets");
        return of([]);
      })
    );

    this.publications$ = this.backend.getPublications()
      .pipe(
        catchError(err => {
          this.error = "Couldn't load publications." + err.message;
          this.snackBar.showError("Couldn't load publications");
          return of([]);
        })
      );

    this.subscriptions.push(
      this.experimentTemplate?.valueChanges.subscribe(value => {
        value?.available_metrics.forEach(metric => this.metrics.addControl(metric, new FormControl<boolean>(true)));
      })
    );
    this.subscriptions.push(
      this.experimentTemplate?.valueChanges.subscribe(value => {
        value?.envs_required.forEach(env => this.envs_required.addControl(env.name, new FormControl<string>("", Validators.required)));
        value?.envs_optional.forEach(env => this.envs_optional.addControl(env.name, new FormControl<string>("")));
      })
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub?.unsubscribe());
  }

  get experimentTemplate() {
    return this.experimentForm.get('experimentTemplate');
  }

  get metrics() {
    return this.experimentForm.get('metrics') as FormGroup;
  }

  get publications() {
    return this.experimentForm.get('publications') as FormArray;
  }

  get model() {
    return this.experimentForm.get("model");
  }

  get dataset() {
    return this.experimentForm.get("dataset");
  }

  get envs_required() {
    return this.experimentForm.get("envs_required") as FormGroup;
  }

  get envs_optional() {
    return this.experimentForm.get("envs_optional") as FormGroup;
  }

  modelAutocompleteFilter(query: string | Model | null): Observable<Model[]> {
    if (typeof query != "string") {
      return this.models$ ? this.models$ : of([]);
    }
    return this.backend.getModels(query)
  }

  datasetAutocompleteFilter(query: string | Dataset | null): Observable<Dataset[]> {
    if (typeof query != "string") {
      return this.datasets$ ? this.datasets$ : of([]);;
    }
    return this.backend.getDatasets(query);
  }

  displayChosenModel(model: Model) {
    return model ? model.name : "";
  }

  displayChosenDataset(dataset: Dataset) {
    return dataset ? dataset.name : "";
  }

  onSubmit() {
    const selectedMetrics = Object.entries(this.experimentForm?.value?.metrics as Record<string, boolean>)
      .filter(([_, value]) => value)
      .map(([key, _]) => key);
    const publicationIds = (this.experimentForm.value.publications as Array<Publication>).map(publication => publication.identifier.toString());

    let all_envs: Record<string, string> = {
      ...this.experimentForm?.value?.envs_required,
      ...this.experimentForm?.value?.envs_optional
    };
    let envsToSend: EnvironmentVar[] = [];

    for (let env in all_envs) {
      if (all_envs[env] && all_envs[env].length > 0) {
        envsToSend.push({
          key: env,
          value: all_envs[env]
        });
      }
    }

    const experiment: ExperimentCreate = {
      name: String(this.experimentForm.value.name?.trim()),
      description: String(this.experimentForm.value.description?.trim()),
      publication_ids: publicationIds,
      experiment_template_id: String(this.experimentTemplate?.value?.id),
      dataset_ids: [String((this.experimentForm?.value?.dataset as Dataset)?.identifier)],
      model_ids: [String((this.experimentForm?.value?.model as Model)?.identifier)],
      metrics: selectedMetrics,
      env_vars: envsToSend
    };

    firstValueFrom(this.backend.createExperiment(experiment))
      .then(experiment => {
        this.snackBar.show('Experiment created');
        this.router.navigate(['/experiments', experiment.id]);
      })
      .catch(err => {
        this.error = err.message;
        this.snackBar.showError("Couldn't create experiment");
      });
  }

  onSelectPublication(event: MatSelectChange) {
    const publication = event.value as Publication;
    if (this.publications.controls.find(control => control.value.identifier === publication.identifier)) {
      return;
    }
    this.publications.push(new FormControl(publication));
  }

  onRemovePublication(publicationFormControl: any) {
    const index = this.publications.controls.indexOf(publicationFormControl);
    this.publications.removeAt(index);
  }
}
