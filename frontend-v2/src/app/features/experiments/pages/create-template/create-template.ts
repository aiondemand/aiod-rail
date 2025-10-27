import { Component, OnInit, Signal, WritableSignal, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { catchError, combineLatest, firstValueFrom, of, retry, switchMap } from 'rxjs';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { UiButton } from '../../../../shared/components/ui-button/ui-button';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { SnackBarService } from '../../../../shared/services/snack-bar.service';

import {
  ExperimentTemplate,
  ExperimentTemplateCreate,
} from '../../../../shared/models/experiment-template';
import { EnvironmentVarDef } from '../../../../shared/models/env-vars';
import { TaskType } from '../../../../shared/models/backend-generated/task-type';
import { AssetCardinality } from '../../../../shared/models/backend-generated/asset-cardinality';

import { CodeEditorModule } from '@ngstack/code-editor';

@Component({
  selector: 'app-create-template',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    // material
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatCheckboxModule,
    MatIconModule,
    MatTooltipModule,
    // ui
    UiLoadingComponent,
    UiErrorComponent,
    UiButton,
    // editor
    CodeEditorModule,
  ],
  templateUrl: './create-template.html',
  styleUrls: ['./create-template.scss'],
})
export class CreateTemplatePage implements OnInit {
  // DI
  private fb = inject(FormBuilder);
  private api = inject(BackendApiService);
  private snack = inject(SnackBarService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  // ----- state
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  inputTemplate: WritableSignal<ExperimentTemplate | null> = signal(null);
  action: WritableSignal<'create' | 'update'> = signal<'create' | 'update'>('create');

  // When template is used by experiments, some parts are locked
  editableEnvironment = signal<boolean>(true);
  editableVisibility = signal<boolean>(true);

  // ----- constants
  visibilityStrings: ReadonlyArray<'Public' | 'Private'> = ['Public', 'Private'];
  baseImageStrings: ReadonlyArray<string> = [
    'python:3.9',
    'python:3.10',
    'python:3.11',
    'python:3.12',
  ];

  readonly reservedEnvVars = ['MODEL_NAMES', 'DATASET_NAMES', 'MODEL_IDS', 'DATASET_IDS'];

  // ----- form
  form = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    baseImage: ['', Validators.required],
    visibility: this.fb.nonNullable.control<'Public' | 'Private'>('Public', {
      validators: [Validators.required],
    }),
    pipRequirements: [''],
  });

  // add-env mini-forms (required / optional)
  newRequiredEnvForm = this.fb.group({ name: [''], description: [''], isSecret: [false] });
  newOptionalEnvForm = this.fb.group({ name: [''], description: [''], isSecret: [false] });

  // ENVs data
  requiredVars: WritableSignal<EnvironmentVarDef[]> = signal<EnvironmentVarDef[]>([]);
  optionalVars: WritableSignal<EnvironmentVarDef[]> = signal<EnvironmentVarDef[]>([]);

  // ----- editor
  scriptCode = signal<string>('');
  editorModel = {
    language: 'python',
    uri: 'file:///script.py',
    value: '' as string,
  };
  editorOptions: any = {
    lineNumbers: 'on',
    contextmenu: true,
    minimap: { enabled: false },
    automaticLayout: true,
    scrollBeyondLastLine: false,
    wordWrap: 'on',
  };

  // derived flags
  hasNoEnvs: Signal<boolean> = computed(
    () => this.requiredVars().length === 0 && this.optionalVars().length === 0
  );

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    const isUpdateRoute = !!id && /\/experiments\/templates\/[^/]+\/update$/.test(this.router.url);

    if (isUpdateRoute && id) {
      this.action.set('update');
      this.loading.set(true);

      const data$ = of(id).pipe(
        switchMap((templateId) =>
          combineLatest([
            this.api.getExperimentsOfTemplateCount(templateId, false),
            this.api.getExperimentsOfTemplateCount(templateId, true),
            this.api.getExperimentTemplate(templateId),
          ])
        ),
        retry(3),
        catchError((err) => {
          this.fail("Couldn't load template data", err);
          return of<[number, number, ExperimentTemplate | null]>([0, 0, null]);
        })
      );

      firstValueFrom(data$)
        .then(([experimentCount, myExperimentCount, template]) => {
          if (!template) return;

          this.editableEnvironment.set(experimentCount === 0);
          this.editableVisibility.set(experimentCount - myExperimentCount === 0);

          this.inputTemplate.set(template);
          this.prefillForm(template);
          this.loading.set(false);
        })
        .catch((err) => this.fail("Couldn't load template data", err));
    } else {
      this.action.set('create');
      this.loading.set(false);
    }
  }

  /** Patch form with loaded template and lock parts that must not change */
  private prefillForm(templ: ExperimentTemplate) {
    this.form.patchValue({
      name: templ.name,
      description: templ.description,
      baseImage: this.parseBaseImageFromDockerfile(templ.dockerfile),
      pipRequirements: templ.pip_requirements || '',
      visibility: templ.is_public ? 'Public' : 'Private',
    });

    const code = templ.script || '';
    this.scriptCode.set(code);
    this.editorModel.value = code;

    // ENVs
    this.requiredVars.set([...(templ.envs_required ?? [])]);
    this.optionalVars.set([...(templ.envs_optional ?? [])]);

    // Lock fields depending on editability
    if (!this.editableEnvironment()) {
      this.form.controls.baseImage.disable();
      this.form.controls.pipRequirements.disable();
      this.newRequiredEnvForm.disable();
      this.newOptionalEnvForm.disable();
    }
    if (!this.editableVisibility()) {
      this.form.controls.visibility.disable();
    }
  }

  private parseBaseImageFromDockerfile(dockerfile: string | null | undefined): string {
    if (!dockerfile) return '';
    const first = (dockerfile.split('\n')[0] || '').trim();
    const parts = first.split(/\s+/);
    return parts.length >= 2 ? parts[1] : '';
  }

  // ----- ENV helpers
  addVariableReq() {
    this.addVariable(this.newRequiredEnvForm, this.requiredVars);
  }
  addVariableOpt() {
    this.addVariable(this.newOptionalEnvForm, this.optionalVars);
  }

  private addVariable(form: FormGroup, target: WritableSignal<EnvironmentVarDef[]>) {
    const rawName = (form.value['name'] ?? '').toString().trim();
    if (!rawName) return;

    const newName = rawName.toUpperCase();
    const description = (form.value['description'] ?? '').toString();
    const isSecret = !!form.value['isSecret'];

    const exists =
      [...this.requiredVars(), ...this.optionalVars()].some((e) => e.name === newName) ||
      this.reservedEnvVars.includes(newName);

    if (exists) {
      const msg = this.reservedEnvVars.includes(newName)
        ? `Environment variable ${newName} is RESERVED.`
        : `Environment variable ${newName} is already defined.`;
      this.snack.show(msg);
      return;
    }

    target.update((arr) => [...arr, { name: newName, description, is_secret: isSecret }]);
    form.reset();
  }

  removeVariable(target: WritableSignal<EnvironmentVarDef[]>, idx: number) {
    const arr = target();
    if (idx < 0 || idx >= arr.length) return;
    target.set(arr.filter((_, i) => i !== idx));
  }

  // ----- editor change
  onEditorChange(val: string) {
    const v = val ?? '';
    this.scriptCode.set(v);
    this.editorModel.value = v;
  }

  // ----- submit
  async submit() {
    if (this.form.invalid || !this.scriptCode().trim()) return;

    // fixed attributes (kept 1:1 with original)
    const fixedTask = TaskType.TextClassification;
    const fixedDatasetSchema = { cardinality: AssetCardinality._11 };
    const fixedModelSchema = { cardinality: AssetCardinality._11 };

    const payload: ExperimentTemplateCreate = {
      name: String(this.form.controls.name.value).trim(),
      description: String(this.form.controls.description.value).trim(),
      task: fixedTask,
      datasets_schema: fixedDatasetSchema as any,
      models_schema: fixedModelSchema as any,
      envs_required: this.requiredVars(),
      envs_optional: this.optionalVars(),
      base_image: String(this.form.controls.baseImage.value),
      script: this.scriptCode(),
      pip_requirements: String(this.form.controls.pipRequirements.value || ''),
      is_public: this.form.controls.visibility.value === 'Public',
    };

    this.loading.set(true);

    try {
      let result: ExperimentTemplate;
      if (this.action() === 'update' && this.inputTemplate()?.id) {
        result = await firstValueFrom(
          this.api.updateExperimentTemplate(this.inputTemplate()!.id, payload)
        );
      } else {
        result = await firstValueFrom(this.api.createExperimentTemplate(payload));
      }

      this.snack.show(`Experiment template ${this.action()}d`);
      this.router.navigate(['/experiments', 'templates', result.id]);
    } catch (err: any) {
      if (err?.status === 401) {
        this.snack.showError(
          'An authorization error occurred. Try logging out and then logging in again.'
        );
      } else {
        this.snack.showError(`Couldn't ${this.action()} experiment template`);
      }
      this.error.set(err?.error?.message || err?.message || 'Request failed.');
      this.loading.set(false);
    }
  }

  private fail(msg: string, err?: any) {
    console.error('[CreateTemplate] error:', err);
    this.error.set(err?.error?.message || err?.message || msg);
    this.snack.showError(msg);
    this.loading.set(false);
  }
}
