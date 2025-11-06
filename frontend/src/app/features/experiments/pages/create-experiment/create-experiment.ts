import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators,
  FormGroup,
  FormControl,
  FormArray,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { debounceTime, startWith, switchMap, catchError, of, combineLatest, map } from 'rxjs';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { SnackBarService } from '../../../../shared/services/snack-bar.service';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { UiButton } from '../../../../shared/components/ui-button/ui-button';

import { ExperimentCreate, Experiment } from '../../../../shared/models/experiment';
import { ExperimentTemplate } from '../../../../shared/models/experiment-template';
import { Model } from '../../../../shared/models/model';
import { Dataset } from '../../../../shared/models/dataset';
import { Publication } from '../../../../shared/models/publication';

@Component({
  selector: 'app-create-experiment',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    // material
    MatAutocompleteModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatSelectModule,
    MatChipsModule,
    MatTooltipModule,
    // ui
    UiLoadingComponent,
    UiErrorComponent,
    UiButton,
  ],
  templateUrl: './create-experiment.html',
  styleUrls: ['./create-experiment.scss'],
})
export class CreateExperimentPage implements OnInit {
  // DI
  private api = inject(BackendApiService);
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private snack = inject(SnackBarService);
  private destroyRef = inject(DestroyRef);
  private route = inject(ActivatedRoute);

  readonly NO_MODEL_TOKEN = '__NO_MODEL__';
  readonly NO_DATASET_TOKEN = '__NO_DATASET__';
  readonly NO_MODEL_LABEL = ' ➖ No model needed for this experiment';
  readonly NO_DATASET_LABEL = '➖ No dataset needed for this experiment';

  // ----- state
  loading = signal<boolean>(true);
  error = signal<string | null>(null);
  action = signal<'create' | 'update'>('create');

  // --- mode
  private isUpdate = false;
  private currentExpId: string | null = null;

  // form
  form = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    visibility: this.fb.nonNullable.control<'Public' | 'Private'>('Private', {
      validators: [Validators.required],
    }),
    publications: this.fb.array<FormControl<Publication>>([]),
    experimentTemplate: this.fb.control<ExperimentTemplate | string>('', {
      validators: [Validators.required],
    }),
    model: this.fb.control<Model | string>('', { validators: [Validators.required] }),
    dataset: this.fb.control<Dataset | string>('', { validators: [Validators.required] }),
    envsRequired: this.fb.group({}) as FormGroup,
    envsOptional: this.fb.group({}) as FormGroup,
  });

  // helpers (getters)
  get publicationsFA() {
    return this.form.get('publications') as FormArray<FormControl<Publication>>;
  }
  get tplFC() {
    return this.form.get('experimentTemplate') as FormControl<ExperimentTemplate | string>;
  }
  get modelFC() {
    return this.form.get('model') as FormControl<Model | string>;
  }
  get datasetFC() {
    return this.form.get('dataset') as FormControl<Dataset | string>;
  }
  get envsReqFG() {
    return this.form.get('envsRequired') as FormGroup;
  }
  get envsOptFG() {
    return this.form.get('envsOptional') as FormGroup;
  }

  selectedTemplate = signal<ExperimentTemplate | null>(null);

  hasNoEnvs = computed(() => {
    const t = this.selectedTemplate();
    return !t || ((t.envs_required?.length ?? 0) === 0 && (t.envs_optional?.length ?? 0) === 0);
  });

  // ===== Autocompletes =====

  // Templates
  templates$ = this.tplFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => {
      if (typeof q !== 'string') return of<ExperimentTemplate[]>([]);
      return this.api
        .getExperimentTemplates(q, {}, { finalized: true, approved: true, archived: false })
        .pipe(
          catchError((err) => {
            this.fail("Couldn't load experiment templates", err);
            return of([]);
          })
        );
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  // Models
  modelsMine$ = this.modelFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => {
      if (typeof q !== 'string') return of<Model[]>([]);
      if (q === this.NO_MODEL_TOKEN) return of<Model[]>([]);
      return this.api.getMyModels(q);
    }),
    catchError((err) => {
      this.fail("Couldn't load my models", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  modelsPublic$ = this.modelFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => {
      if (typeof q !== 'string') return of<Model[]>([]);
      if (q === this.NO_MODEL_TOKEN) return of<Model[]>([]);
      return this.api.getModels(q);
    }),
    catchError((err) => {
      this.fail("Couldn't load models", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  // Datasets
  datasetsMine$ = this.datasetFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => {
      if (typeof q !== 'string') return of<Dataset[]>([]);
      if (q === this.NO_DATASET_TOKEN) return of<Dataset[]>([]);
      return this.api.getMyDatasets(q);
    }),
    catchError((err) => {
      this.fail("Couldn't load my datasets", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  datasetsPublic$ = this.datasetFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => {
      if (typeof q !== 'string') return of<Dataset[]>([]);
      if (q === this.NO_DATASET_TOKEN) return of<Dataset[]>([]);
      return this.api.getDatasets(q);
    }),
    catchError((err) => {
      this.fail("Couldn't load datasets", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  // Publications — searchable autocomplete
  pubSearchFC = new FormControl<Publication | string>('');

  // Preferred: if backend supports querying publications by term, swap in this block:
  publicationsSearch$ = this.pubSearchFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => (typeof q === 'string' ? this.api.getPublications(q) : of([]))),
    catchError(() => of([])),
    takeUntilDestroyed(this.destroyRef)
  );

  ngOnInit(): void {
    // When template changes, reset dependent fields and rebuild ENV controls
    this.tplFC.valueChanges.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((val) => {
      const tpl = typeof val === 'string' ? null : val;
      this.selectedTemplate.set(tpl);

      this.modelFC.setValue('');
      this.datasetFC.setValue('');

      Object.keys(this.envsReqFG.controls).forEach((k) => this.envsReqFG.removeControl(k));
      Object.keys(this.envsOptFG.controls).forEach((k) => this.envsOptFG.removeControl(k));

      if (!tpl) return;

      (tpl.envs_required ?? []).forEach((env) =>
        this.envsReqFG.addControl(
          env.name,
          new FormControl<string>('', { nonNullable: true, validators: [Validators.required] })
        )
      );
      (tpl.envs_optional ?? []).forEach((env) =>
        this.envsOptFG.addControl(env.name, new FormControl<string>('', { nonNullable: true }))
      );
    });

    // --- UPDATE MODE
    const expId = this.route.snapshot.paramMap.get('id');
    if (expId && /\/experiments\/[^/]+\/update$/.test(this.router.url)) {
      this.isUpdate = true;
      this.currentExpId = expId;
      this.action.set('update');

      this.loading.set(true);
      this.api
        .getExperiment(expId)
        .pipe(
          switchMap((exp: Experiment) =>
            combineLatest([
              of(exp),
              exp?.dataset_ids?.length ? this.api.getDataset(exp.dataset_ids[0]) : of(null),
              exp?.model_ids?.length ? this.api.getModel(exp.model_ids[0]) : of(null),
              this.api.getExperimentPublications(exp),
              exp?.experiment_template_id
                ? this.api.getExperimentTemplate(exp.experiment_template_id)
                : of(null),
              this.api.getExperimentRunsCount(exp.id),
            ])
          )
        )
        .subscribe({
          next: ([exp, ds, mdl, pubs, tpl, runsCount]) => {
            this.form.patchValue(
              {
                name: (exp as any).name,
                description: (exp as any).description,
                visibility: (exp as any).is_public ? 'Public' : 'Private',
                experimentTemplate: tpl as any,
                model: mdl ? (mdl as any) : this.NO_MODEL_TOKEN,
                dataset: ds ? (ds as any) : this.NO_DATASET_TOKEN,
              },
              { emitEvent: true }
            );
            this.selectedTemplate.set(tpl as any);

            // prefill selected pubs into chips
            this.publicationsFA.clear();
            (pubs || []).forEach((p: Publication) =>
              this.publicationsFA.push(new FormControl(p, { nonNullable: true }))
            );

            // ENVs prefill
            const envMap = new Map<string, string>(
              ((exp as any).env_vars || []).map((e: any) => [e.key, e.value])
            );
            (tpl?.envs_required ?? []).forEach((env: any) => {
              const c = this.envsReqFG.get(env.name) as FormControl<string>;
              if (c) c.setValue(envMap.get(env.name) ?? '');
            });
            (tpl?.envs_optional ?? []).forEach((env: any) => {
              const c = this.envsOptFG.get(env.name) as FormControl<string>;
              if (c) c.setValue(envMap.get(env.name) ?? '');
            });

            // lock assets if there are runs
            const editableAssets = (runsCount as number) === 0;
            if (!editableAssets) {
              this.modelFC.disable();
              this.datasetFC.disable();
              this.tplFC.disable();
              this.envsOptFG.disable();
              this.envsReqFG.disable();
            }

            this.loading.set(false);
          },
          error: (err) => this.fail("Couldn't load experiment for update", err),
        });
    } else {
      queueMicrotask(() => this.loading.set(false));
    }
  }

  // UI display helpers
  displayTpl = (t?: ExperimentTemplate) => (t ? t.name : '');
  displayPub = (p?: Publication) => (p ? p.name : '');

  displayModel = (m?: Model | string) =>
    typeof m === 'string' ? (m === this.NO_MODEL_TOKEN ? this.NO_MODEL_LABEL : m) : m ? m.name : '';

  displayDataset = (d?: Dataset | string) =>
    typeof d === 'string'
      ? d === this.NO_DATASET_TOKEN
        ? this.NO_DATASET_LABEL
        : d
      : d
      ? d.name
      : '';

  // Publications add/remove
  onPublicationPicked(p: Publication) {
    if (!p) return;
    if (this.publicationsFA.controls.some((c) => c.value.identifier === p.identifier)) return;
    this.publicationsFA.push(new FormControl(p, { nonNullable: true }));
    // Clear input so the user can type another query immediately
    this.pubSearchFC.setValue('');
  }

  addPublication(p: Publication) {
    // kept for backward compatibility; can be removed if not used anywhere else
    this.onPublicationPicked(p);
  }

  removePublication(ctrl: FormControl<Publication>) {
    const idx = this.publicationsFA.controls.indexOf(ctrl);
    if (idx >= 0) this.publicationsFA.removeAt(idx);
  }

  submit() {
    if (this.form.invalid) return;

    const tpl = this.selectedTemplate();
    if (!tpl) {
      this.snack.showError('Choose an experiment template first.');
      return;
    }

    const vis = this.form.controls.visibility.value === 'Public';

    // --- read raw data
    const envReqRaw =
      (this.envsReqFG as any)?.getRawValue?.() ?? (this.envsReqFG.value as Record<string, unknown>);
    const envOptRaw =
      (this.envsOptFG as any)?.getRawValue?.() ?? (this.envsOptFG.value as Record<string, unknown>);

    const toStringRecord = (obj: Record<string, unknown>): Record<string, string> =>
      Object.fromEntries(
        Object.entries(obj || {}).map(([k, v]) => [k, v == null ? '' : String(v)])
      ) as Record<string, string>;

    const envReq = toStringRecord(envReqRaw);
    const envOpt = toStringRecord(envOptRaw);
    const all = { ...envReq, ...envOpt };

    const env_vars = Object.entries(all)
      .filter(([, v]) => !!v && String(v).length > 0)
      .map(([key, value]) => ({ key, value }));

    const pubIds = this.publicationsFA.value.map((p) => String(p.identifier));

    const dsVal = this.datasetFC.value;
    const mdlVal = this.modelFC.value;

    const dataset_ids =
      !dsVal || (typeof dsVal === 'string' && dsVal === this.NO_DATASET_TOKEN)
        ? []
        : [String((dsVal as Dataset).identifier)];

    const model_ids =
      !mdlVal || (typeof mdlVal === 'string' && mdlVal === this.NO_MODEL_TOKEN)
        ? []
        : [String((mdlVal as Model).identifier)];

    const payload: ExperimentCreate = {
      name: String(this.form.controls.name.value).trim(),
      description: String(this.form.controls.description.value).trim(),
      publication_ids: pubIds,
      experiment_template_id: tpl.id,
      dataset_ids,
      model_ids,
      env_vars,
      is_public: vis,
    };

    this.loading.set(true);

    // --- added update api
    const req$ =
      this.isUpdate && this.currentExpId
        ? this.api.updateExperiment(this.currentExpId, payload)
        : this.api.createExperiment(payload);

    req$.pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (exp: Experiment) => {
        this.snack.show(this.isUpdate ? 'Experiment updated' : 'Experiment created');
        this.router.navigate(['/experiments', exp.id]);
      },
      error: (err) => {
        this.fail(`Couldn't ${this.isUpdate ? 'update' : 'create'} experiment`, err);
      },
    });
  }

  private fail(msg: string, err?: any) {
    console.error('[CreateExperiment] error:', err);
    this.error.set(err?.error?.message || err?.message || msg);
    this.snack.showError(msg);
    this.loading.set(false);
  }
}
