import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatTable } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { EnvironmentVarDef } from 'src/app/models/env-vars';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { ExperimentTemplate, ExperimentTemplateCreate } from 'src/app/models/experiment-template';
import { TaskType } from 'src/app/models/backend-generated/task-type';
import { AssetCardinality } from 'src/app/models/backend-generated/asset-cardinality';
import { combineLatest, firstValueFrom, of, retry, switchMap } from 'rxjs';


@Component({
  selector: 'app-edit-experiment-template',
  templateUrl: './edit-experiment-template.component.html',
  styleUrls: ['./edit-experiment-template.component.scss']
})
export class EditExperimentTemplateComponent {
  inputExperimentTemplate: ExperimentTemplate | null = null;
  editableEnvironment: boolean = true;
  editableVisibility: boolean = true;
  loading: boolean = true;
  action: string = "create";

  experimentTemplateForm = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    baseImage: ['', Validators.required],
    visibility: ['Public', Validators.required],
    pipRequirements: [''],
  });
  newRequiredEnvForm = this.fb.group({
    name: [''],
    description: [''],
    isSecret: [false]
  });
  newOptionalEnvForm = this.fb.group({
    name: [''],
    description: [''],
    isSecret: [false]
  });

  scriptCode: string = "";
  visibilityStrings: string[] = [
    "Public",
    "Private"
  ]
  baseImageStrings: string[] = [
    "python:3.9",
    "python:3.10",
    "python:3.11",
    "python:3.12"
  ]

  editorModel: any;
  editorOptions: any;

  requiredVarsData: EnvironmentVarDef[] = [];
  optionalVarsData: EnvironmentVarDef[] = [];
  displayedEnvVarColumns: string[] = ['name', 'description', 'remove-btn'];

  @ViewChild("requiredVarsTable") requiredVarsTable: MatTable<EnvironmentVarDef>;
  @ViewChild("optionalVarsTable") optionalVarsTable: MatTable<EnvironmentVarDef>;

  metrics: string[] = [];

  constructor(
    private fb: FormBuilder,
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router,
    private route: ActivatedRoute,
  ) { }

  reserved_environment_variables: string[] = [
    "MODEL_NAMES", "DATASET_NAMES", "MODEL_IDS", "DATASET_IDS",
  ]

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params["id"]) {
        var data$ = of(params["id"]).pipe(
          switchMap(templateId => combineLatest([
            this.backend.getExperimentsOfTemplateCount(templateId, false),
            this.backend.getExperimentsOfTemplateCount(templateId, true),
            this.backend.getExperimentTemplate(templateId)
          ])),
          retry(3)
        );

        firstValueFrom(data$)
          .then(([experimentCount, myExperimentCount, template]) => {
            this.editableEnvironment = experimentCount == 0 ;
            this.editableVisibility = experimentCount - myExperimentCount == 0;

            this.inputExperimentTemplate = template
            this.prefillOldValues();
            this.setupEditor()
            this.action = "update"
            this.loading = false;
          })
          .catch(err => console.error(err))
      }
      else {
        this.setupEditor()
        this.loading = false;
      }
    })
  }

  prefillOldValues(): void {
    let templ = this.inputExperimentTemplate
    if (!templ) {
      return;
    }

    this.experimentTemplateForm.get("name")?.setValue(templ.name);
    this.experimentTemplateForm.get("description")?.setValue(templ.description);
    this.experimentTemplateForm.get("baseImage")?.setValue(this.parseBaseImageFromDockerfile(templ.dockerfile));
    this.experimentTemplateForm.get("pipRequirements")?.setValue(templ.pip_requirements);
    this.experimentTemplateForm.get("visibility")?.setValue(templ.is_public ? "Public" : "Private");
    this.scriptCode = templ.script;

    templ.envs_required.forEach(env => this.requiredVarsData.push(env));
    this.requiredVarsTable?.renderRows();

    templ.envs_optional.forEach(env => this.optionalVarsData.push(env));
    this.optionalVarsTable?.renderRows();

    if (!this.editableEnvironment) {
      this.experimentTemplateForm.get("baseImage")?.disable();
      this.experimentTemplateForm.get("pipRequirements")?.disable();

      this.newRequiredEnvForm.get("name")?.disable();
      this.newRequiredEnvForm.get("description")?.disable();
      this.newRequiredEnvForm.get("isSecret")?.disable();

      this.newOptionalEnvForm.get("name")?.disable();
      this.newOptionalEnvForm.get("description")?.disable();
      this.newOptionalEnvForm.get("isSecret")?.disable();
    }
    if (!this.editableVisibility) {
      this.experimentTemplateForm.get("visibility")?.disable();
    }

  }

  parseBaseImageFromDockerfile(dockerfile: string) {
    return dockerfile.split("\n")[0].split(" ")[1];
  }

  onSubmit() {
    let form = this.experimentTemplateForm;

    // TODO for now this attributes will be fixed
    const fixedTask = TaskType.TextClassification;
    const fixedDatasetSchema = {
      "cardinality": AssetCardinality._11,
    };
    const fixedModelSchema = {
      "cardinality": AssetCardinality._11,
    };

    let experimentTemplate: ExperimentTemplateCreate = {
      name: String(form.get("name")?.value?.trim()),
      description: String(form.get("description")?.value),
      task: fixedTask,
      datasets_schema: fixedDatasetSchema,
      models_schema: fixedModelSchema,
      envs_required: this.requiredVarsData,
      envs_optional: this.optionalVarsData,
      base_image: String(form.get("baseImage")?.value),
      script: this.scriptCode,
      pip_requirements: String(form.get("pipRequirements")?.value),
      is_public: String(form.get("visibility")?.value) == "Public" ? true : false
    };

    let promisedTemplate: Promise<ExperimentTemplate>;
    if (this.inputExperimentTemplate) {
      // UPDATE
      promisedTemplate = firstValueFrom(this.backend.updateExperimentTemplate(
        this.inputExperimentTemplate.id, experimentTemplate
      ));
    }
    else {
      // CREATE
      promisedTemplate = firstValueFrom(
        this.backend.createExperimentTemplate(experimentTemplate)
      );
    }

    promisedTemplate
      .then(experimentTemplate => {
        this.snackBar.show(`Experiment template ${this.action}d`);
        this.router.navigate(['/experiments', 'templates', experimentTemplate.id]);
      })
      .catch(err => {
        if (err.status == 401) {
          this.snackBar.showError("An authorization error occurred. Try logging out and then logging in again.");
        }
        else {
          this.snackBar.showError(`Couldn't ${this.action} experiment template`);
        }
      });
  }

  addVariableReq(form: FormGroup, dataTable: EnvironmentVarDef[]) {
    this.addVariable(form, dataTable);
    this.requiredVarsTable?.renderRows();
  }

  addVariableOpt(form: FormGroup, dataTable: EnvironmentVarDef[]) {
    this.addVariable(form, dataTable);
    this.optionalVarsTable?.renderRows();
  }

  addVariable(form: FormGroup, dataTable: EnvironmentVarDef[]) {
    let newEnvName = String(form.value.name.trim().toUpperCase());
    let alreadyExists = this.requiredVarsData
      .concat(...this.optionalVarsData)
      .some(env => env.name == newEnvName);

    if (alreadyExists) {
      this.snackBar.show(`Environment variable ${newEnvName} has already been defined.`)
      return;
    }
    if (this.reserved_environment_variables.includes(newEnvName)) {
      this.snackBar.show(`Environment variable ${newEnvName} is one of the RESERVED ENVIRONMENT VARIABLES.`)
      return;
    }

    console.log(`VALUE ${form.value.isSecret}`)

    dataTable.push({
      name: newEnvName,
      description: form.value.description ?? "",
      is_secret: form.value.isSecret ?? false
    });

    form.reset();
  }

  removeVariable(table: MatTable<EnvironmentVarDef>, dataTable: EnvironmentVarDef[], index: number) {
    dataTable.splice(index, 1);
    table.renderRows();
  }

  setupEditor() {
    this.editorModel = {
      language: 'python',
      uri: '',
      value: this.scriptCode,
    };
    this.editorOptions = {
      linenumbers: true,
      contextmenu: true,
      minimap: {
        enabled: false,
      },
    }
  }
}
