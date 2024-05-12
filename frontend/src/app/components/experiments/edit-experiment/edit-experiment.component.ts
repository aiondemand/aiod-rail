import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSelectChange } from '@angular/material/select';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription, catchError, combineLatest, debounceTime, firstValueFrom, of, retry, startWith, switchMap } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { EnvironmentVar } from 'src/app/models/env-vars';
import { Experiment, ExperimentCreate } from 'src/app/models/experiment';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { Model } from 'src/app/models/model';
import { Publication } from 'src/app/models/publication';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

@Component({
  selector: 'app-edit-experiment',
  templateUrl: './edit-experiment.component.html',
  styleUrls: ['./edit-experiment.component.scss']
})
export class EditExperimentComponent implements OnInit {
  inputExperiment: Experiment | null = null;
  inputExperimentTemplate: ExperimentTemplate | null = null;
  inputPublications: Publication[] = [];
  inputDataset: Dataset | null = null;
  inputModel: Model | null = null;

  editableAssets: boolean = true;
  loading: boolean = true;
  action: string = "create";
  
  experimentForm = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    publications: this.fb.array(Array<Publication>()),
    dataset: new FormControl<Dataset | string>('', Validators.required),
    model: new FormControl<Model | string>('', Validators.required),
    metrics: this.fb.group({}),
    envsRequired: this.fb.group({}),
    envsOptional: this.fb.group({}),
    experimentTemplate: new FormControl<ExperimentTemplate | null>(null, Validators.required)
  });

  error: string = '';

  experimentTemplates$: Observable<ExperimentTemplate[]>;
  publications$: Observable<Publication[]>;
  models$: Observable<Model[]> | undefined;
  datasets$: Observable<Dataset[]> | undefined;

  subscription: Subscription | undefined;

  constructor(
    private fb: FormBuilder,
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params["id"]) {
        var data$ = this.backend.getExperiment(params["id"]).pipe(
            switchMap(experiment => combineLatest([
              this.backend.getDataset(experiment.dataset_ids[0]),
              this.backend.getModel(experiment.model_ids[0]),
              this.backend.getExperimentPublications(experiment),
              this.backend.getExperimentTemplate(experiment.experiment_template_id),
              this.backend.getExperimentRunsCount(experiment.id),
              of(experiment),
            ])),
            retry(3)
          );
        firstValueFrom(data$)
          .then(([dataset, model, publications, template, experimentRunsCount, experiment]) => {
            this.inputDataset = dataset;
            this.inputModel = model;
            this.inputPublications = publications;
            this.inputExperimentTemplate = template;
            this.inputExperiment = experiment;
            this.editableAssets = experimentRunsCount == 0;

            this.prefillOldValues();
            this.action = "update"
            this.loading = false;
          })
          .catch(err => console.error(err));
      } 
      else {
        this.loading = false;
      }     
    });

    this.experimentTemplates$ = this.backend.getExperimentTemplates({}, {
      only_finalized: true,
      only_public: true,
      only_usable: true
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

    this.subscription = this.experimentTemplate?.valueChanges.subscribe(value => {
        Object.keys(this.metrics.controls).forEach(k => this.metrics.removeControl(k));
        Object.keys(this.envsRequired.controls).forEach(k => this.envsRequired.removeControl(k));
        Object.keys(this.envsOptional.controls).forEach(k => this.envsOptional.removeControl(k));

        value?.available_metrics.forEach(metric => {
          this.metrics.addControl(metric, new FormControl<boolean>(true));
          this.metrics.get(metric)?.setValue(true);
        });
        value?.envs_required.forEach(env => this.envsRequired.addControl(env.name, new FormControl<string>("", Validators.required)));
        value?.envs_optional.forEach(env => this.envsOptional.addControl(env.name, new FormControl<string>("")));

        this.dataset?.setValue("");
        this.model?.setValue("");
      });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  get name() {
    return this.experimentForm.get('name');
  }

  get description() {
    return this.experimentForm.get('description');
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

  get envsRequired() {
    return this.experimentForm.get("envsRequired") as FormGroup;
  }

  get envsOptional() {
    return this.experimentForm.get("envsOptional") as FormGroup;
  }

  prefillOldValues(): void {
    let exp = this.inputExperiment;
    if (!exp) {
      return;
    }
  
    this.name?.setValue(exp.name);
    this.description?.setValue(exp.description);
    this.experimentTemplate?.setValue(this.inputExperimentTemplate);

    this.inputPublications.forEach(publ => this.publications.push(new FormControl(publ)));
    this.model?.setValue(this.inputModel);
    this.dataset?.setValue(this.inputDataset);

    this.inputExperimentTemplate?.available_metrics.forEach(metric => {
      this.metrics.addControl(metric, new FormControl<boolean>(true));
      this.metrics.get(metric)?.setValue(exp?.metrics.includes(metric) ?? false);
    });

    this.inputExperimentTemplate?.envs_required.forEach(env => {
      this.envsRequired.addControl(env.name, new FormControl<string>("", Validators.required));
      this.envsRequired.get(env.name)?.setValue(exp?.env_vars.find(e => e.key == env.name)?.value ?? "");
    });

    this.inputExperimentTemplate?.envs_optional.forEach(env => {
      this.envsOptional.addControl(env.name, new FormControl<string>("", Validators.required));
      this.envsOptional.get(env.name)?.setValue(exp?.env_vars.find(e => e.key == env.name)?.value ?? "");
    });

    if (!this.editableAssets) {
      this.model?.disable()
      this.dataset?.disable();
      this.experimentTemplate?.disable();
      
      this.experimentForm.get("metrics")?.disable();
      this.experimentForm.get("envsOptional")?.disable();
      this.experimentForm.get("envsRequired")?.disable(); 
    }
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
      ...this.experimentForm?.value?.envsRequired,
      ...this.experimentForm?.value?.envsOptional
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
      env_vars: envsToSend,
      is_public: false
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
