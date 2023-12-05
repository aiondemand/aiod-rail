import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatTable } from '@angular/material/table';
import { Router } from '@angular/router';
import { EnvironmentVarDef } from 'src/app/models/env-vars';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { ExperimentTemplateCreate } from 'src/app/models/experiment-template';
import { TaskType } from 'src/app/models/backend-generated/task-type';
import { AssetCardinality } from 'src/app/models/backend-generated/asset-cardinality';


@Component({
  selector: 'app-create-experiment-template',
  templateUrl: './create-experiment-template.component.html',
  styleUrls: ['./create-experiment-template.component.scss']
})
export class CreateExperimentTemplateComponent {
  experimentTemplateForm = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    baseImage: ['', Validators.required],
    pipRequirements: [''],
    script: ['', Validators.required],
  });
  newRequiredEnvForm = this.fb.group({
    name: [''],
    description: [''],
  });
  newOptionalEnvForm = this.fb.group({
    name: [''],
    description: [''],
  });
  metricForm = this.fb.group({
    name: ['']
  })

  base_images: string[] = [
    "python:3.9",
    "python:3.10",
    "python:3.11",
    "python:3.12"
  ]

  requiredVarsData: EnvironmentVarDef[] = [];
  optionalVarsData: EnvironmentVarDef[] = [];
  displayedEnvVarColumns: string[] = ['name', 'description', 'remove-btn'];

  @ViewChild(MatTable) requiredVarsTable: MatTable<EnvironmentVarDef>;
  @ViewChild(MatTable) optionalVarsTable: MatTable<EnvironmentVarDef>;

  metrics: string[] = [];

  constructor(
    private fb: FormBuilder,
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router
  ) { }

  debug() {
    console.log(this.experimentTemplateForm.value);
  }

  ngOnInit(): void {

  }

  onSubmit() {
    var formValue = this.experimentTemplateForm.value;

    // TODO for now this attributes will be fixed
    const fixedTask = TaskType.TextClassification;
    const fixedDatasetSchema = {
      "cardinality": AssetCardinality._11,
    };
    const fixedModelSchema = {
      "cardinality": AssetCardinality._11,
    };

    var experimentTemplate: ExperimentTemplateCreate = {
      name: String(formValue.name?.trim()),
      description: String(formValue.description),
      task: fixedTask,
      datasets_schema: fixedDatasetSchema,
      models_schema: fixedModelSchema,
      envs_required: this.requiredVarsData,
      envs_optional: this.optionalVarsData,
      available_metrics: this.metrics,
      base_image: String(formValue.baseImage),
      script: String(formValue.script),
      pip_requirements: String(formValue.pipRequirements)
    };

    this.backend.createExperimentTemplate(experimentTemplate)
      .subscribe({
        next: experimentTemplate => {
          this.snackBar.show('Experiment template created');
          this.router.navigate(['/experiments', 'templates', experimentTemplate.id]);
        },
        error: err => {
          this.snackBar.showError("Couldn't create experiment");
        }
      });
  }

  addVariable(form: FormGroup, table: MatTable<EnvironmentVarDef>, dataTable: EnvironmentVarDef[]) {
    var newEnvName = String(form.value.name.trim());
    var alreadyExists = this.requiredVarsData
      .concat(...this.optionalVarsData)
      .some(env => env.name == newEnvName);

    if (alreadyExists) {
      this.snackBar.show(`Environment variable ${newEnvName} has already been defined.`)
      return;
    }

    dataTable.push({
      name: newEnvName,
      description: form.value.description ?? ""
    });

    form.reset();
    table?.renderRows();
  }

  removeVariable(table: MatTable<EnvironmentVarDef>, dataTable: EnvironmentVarDef[], index: number) {
    dataTable.splice(index, 1);
    table?.renderRows();
  }

  addMetric(): void {
    var newMetric = String(this.metricForm.value.name?.trim())
    if (this.metrics.includes(newMetric)) {
      this.snackBar.show(`Metric ${newMetric} has already been added.`)
      return;
    }

    this.metrics.push(newMetric);
    this.metricForm.reset();
  }

  removeMetric(index: number): void {
    this.metrics.splice(index, 1);
  }
}
