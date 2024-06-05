import { Component, OnInit, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSelectChange } from '@angular/material/select';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription, catchError, combineLatest, debounceTime, firstValueFrom, of, retry, startWith, switchMap } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { EnvironmentVarCreate, EnvironmentVarDef } from 'src/app/models/env-vars';
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
    visibility: ['Private', Validators.required],
    publications: this.fb.array(Array<Publication>()),
    dataset: new FormControl<Dataset | string>('', Validators.required),
    model: new FormControl<Model | string>('', Validators.required),
    envsRequired: this.fb.group({}),
    envsOptional: this.fb.group({}),
    experimentTemplate: new FormControl<ExperimentTemplate | string>('', Validators.required)
  });

  visibilityStrings: string[] = [
    "Public",
    "Private"
  ]

  selectedExperimentTemplate: ExperimentTemplate | null = null;

  error: string = '';

  experimentTemplates$: Observable<ExperimentTemplate[]> | undefined;
  publications$: Observable<Publication[]>;
  models$: Observable<Model[]> | undefined;
  myModels$: Observable<Model[]> | undefined;
  datasets$: Observable<Dataset[]> | undefined;
  myDatasets$: Observable<Dataset[]> | undefined;

  subscription: Subscription | undefined;

  constructor(
    private fb: FormBuilder,
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
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
            this.subscribeToExperimentTemplateChange()
            this.loading = false;
          })
          .catch(err => console.error(err));
      }
      else {
        this.subscribeToExperimentTemplateChange()
        this.loading = false;
      }
    });

    this.experimentTemplates$ = this.experimentTemplate?.valueChanges.pipe(
      debounceTime(300),
      startWith(""),
      switchMap(value => this.experimentTemplateAutocompleteFilter(value)),
      catchError(err => {
        this.error = err.message;
        this.snackBar.showError("Couldn't load experiment templates");
        return of([]);
      })
    )

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

    this.myModels$ = this.model?.valueChanges.pipe(
      debounceTime(300), // Debounce to avoid frequent requests
      startWith(""),
      switchMap(value => this.myModelAutocompleteFilter(value)),
      catchError(err => {
        this.error = err.message;
        this.snackBar.showError("Couldn't load my models");
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

    this.myDatasets$ = this.dataset?.valueChanges.pipe(
      debounceTime(300),
      startWith(""),
      switchMap(value => this.myDatasetAutocompleteFilter(value)),
      catchError(err => {
        this.error = "Couldn't load datasets." + err.message;
        this.snackBar.showError("Couldn't load my datasets");
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
  }

  subscribeToExperimentTemplateChange(): void {
    this.subscription = this.experimentTemplate?.valueChanges.subscribe(value => {
      if (!value || typeof value == "string") {
        return;
      }

      Object.keys(this.envsRequired.controls).forEach(k => this.envsRequired.removeControl(k));
      Object.keys(this.envsOptional.controls).forEach(k => this.envsOptional.removeControl(k));

      this.dataset?.setValue("");
      this.model?.setValue("");

      value?.envs_required.forEach(env => this.envsRequired.addControl(env.name, new FormControl<string>("", Validators.required)));
      value?.envs_optional.forEach(env => this.envsOptional.addControl(env.name, new FormControl<string>("")));
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

  get visibility() {
    return this.experimentForm.get('visibility');
  }

  get experimentTemplate() {
    return this.experimentForm.get('experimentTemplate');
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
    if (!exp || !this.inputExperimentTemplate) {
      return;
    }

    this.name?.setValue(exp.name);
    this.description?.setValue(exp.description);
    this.visibility?.setValue(exp.is_public ? "Public" : "Private");
    this.experimentTemplate?.setValue(this.inputExperimentTemplate);
    this.selectedExperimentTemplate = this.inputExperimentTemplate;

    this.inputPublications.forEach(publ => this.publications.push(new FormControl(publ)));
    this.model?.setValue(this.inputModel);
    this.dataset?.setValue(this.inputDataset);

    this.inputExperimentTemplate?.envs_required.forEach(env => {
      this.envsRequired.addControl(env.name, new FormControl<string>("", Validators.required));
      this.envsRequired.get(env.name)?.setValue(exp?.env_vars.find(e => e.key == env.name)?.value ?? "");
    });

    this.inputExperimentTemplate?.envs_optional.forEach(env => {
      this.envsOptional.addControl(env.name, new FormControl<string>(""));
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

  experimentTemplateAutocompleteFilter(query: string | ExperimentTemplate | null): Observable<ExperimentTemplate[]> {
    if (typeof query != "string") {
      this.selectedExperimentTemplate = query;
      return this.experimentTemplates$ ? this.experimentTemplates$ : of([]);
    }

    if (query) {
      this.selectedExperimentTemplate = null;
    }
    return this.backend.getExperimentTemplates(query, {}, {
      finalized: true,
      approved: true,
      archived: false
    });
  }

  modelAutocompleteFilter(query: string | Model | null): Observable<Model[]> {
    if (typeof query != "string") {
      return this.models$ ? this.models$ : of([]);
    }
    return this.backend.getModels(query)
  }

  myModelAutocompleteFilter(query: string | Model | null): Observable<Model[]> {
    if (typeof query != "string") {
      return this.myModels$ ? this.myModels$ : of([]);
    }
    return this.backend.getMyModels(query)
  }

  datasetAutocompleteFilter(query: string | Dataset | null): Observable<Dataset[]> {
    if (typeof query != "string") {
      return this.datasets$ ? this.datasets$ : of([]);;
    }
    return this.backend.getDatasets(query);
  }

  myDatasetAutocompleteFilter(query: string | Dataset | null): Observable<Dataset[]> {
    if (typeof query != "string") {
      return this.myDatasets$ ? this.myDatasets$ : of([]);;
    }
    return this.backend.getMyDatasets(query);
  }

  displayChosenExperimentTemplate(template: ExperimentTemplate) {
    return template ? template.name : "";
  }

  displayChosenModel(model: Model) {
    return model ? model.name : "";
  }

  displayChosenDataset(dataset: Dataset) {
    return dataset ? dataset.name : "";
  }

  onSubmit() {
    let publicationIds = (this.publications.value as Array<Publication>).map(publication => publication.identifier.toString());

    let all_envs: Record<string, string> = {
      ...this.envsRequired.value,
      ...this.envsOptional.value
    };
    let envsToSend: EnvironmentVarCreate[] = [];

    for (let env in all_envs) {
      if (all_envs[env] && all_envs[env].length > 0) {
        envsToSend.push({
          key: env,
          value: all_envs[env]
        });
      }
    }

    let experiment: ExperimentCreate = {
      name: String(this.name?.value?.trim()),
      description: String(this.description?.value?.trim()),
      publication_ids: publicationIds,
      experiment_template_id: String(this.selectedExperimentTemplate?.id),
      dataset_ids: [String((this.dataset?.value as Dataset)?.identifier)],
      model_ids: [String((this.model?.value as Model)?.identifier)],
      env_vars: envsToSend,
      is_public: String(this.visibility?.value) == "Public" ? true : false
    };

    let promisedExperiment: Promise<Experiment>;
    if (this.inputExperiment) {
      // UPDATE
      promisedExperiment = firstValueFrom(this.backend.updateExperiment(
        this.inputExperiment.id, experiment
      ));
    }
    else {
      // CREATE
      promisedExperiment = firstValueFrom(this.backend.createExperiment(experiment));
    }

    promisedExperiment
      .then(experiment => {
        this.snackBar.show(`Experiment ${this.action}d`);
        this.router.navigate(['/experiments', experiment.id]);
      })
      .catch(err => {
        this.error = err.message;
        this.snackBar.showError(`Couldn't ${this.action} experiment`);
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
