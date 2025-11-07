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
import { debounceTime, startWith, switchMap, catchError, of, combineLatest } from 'rxjs';
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
  private hydrating = false;
  private originalExp: Experiment | null = null;

  // lock when runs exist
  assetsLocked = signal<boolean>(false);

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
    switchMap((q) =>
      typeof q !== 'string' || q === this.NO_MODEL_TOKEN ? of<Model[]>([]) : this.api.getMyModels(q)
    ),
    catchError((err) => {
      this.fail("Couldn't load my models", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  modelsPublic$ = this.modelFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) =>
      typeof q !== 'string' || q === this.NO_MODEL_TOKEN ? of<Model[]>([]) : this.api.getModels(q)
    ),
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
    switchMap((q) =>
      typeof q !== 'string' || q === this.NO_DATASET_TOKEN
        ? of<Dataset[]>([])
        : this.api.getMyDatasets(q)
    ),
    catchError((err) => {
      this.fail("Couldn't load my datasets", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  datasetsPublic$ = this.datasetFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) =>
      typeof q !== 'string' || q === this.NO_DATASET_TOKEN
        ? of<Dataset[]>([])
        : this.api.getDatasets(q)
    ),
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

  // ===== helpers =====

  /** Build fresh FormGroup for required envs from a template. */
  private buildEnvsRequiredGroup(tpl: ExperimentTemplate | null): FormGroup {
    const group = this.fb.group({});
    if (tpl) {
      (tpl.envs_required ?? []).forEach((env) => {
        group.addControl(
          env.name,
          new FormControl<string>('', { nonNullable: true, validators: [Validators.required] })
        );
      });
    }
    return group;
  }

  /** Build fresh FormGroup for optional envs from a template. */
  private buildEnvsOptionalGroup(tpl: ExperimentTemplate | null): FormGroup {
    const group = this.fb.group({});
    if (tpl) {
      (tpl.envs_optional ?? []).forEach((env) => {
        group.addControl(env.name, new FormControl<string>('', { nonNullable: true }));
      });
    }
    return group;
  }

  /** Replace env groups in the form with brand-new instances and recompute validity. */
  private replaceEnvGroups(tpl: ExperimentTemplate | null) {
    const newReq = this.buildEnvsRequiredGroup(tpl);
    const newOpt = this.buildEnvsOptionalGroup(tpl);

    this.form.setControl('envsRequired', newReq);
    this.form.setControl('envsOptional', newOpt);

    // recompute validity top-level
    this.form.updateValueAndValidity({ emitEvent: false });
  }

  ngOnInit(): void {
    // on template change -> reset dependent fields, replace env groups, mark dirty/touched, recompute validity
    this.tplFC.valueChanges.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((val) => {
      if (this.hydrating) return;
      const tpl = typeof val === 'string' ? null : val;
      this.selectedTemplate.set(tpl);

      // reset dependent assets
      this.modelFC.setValue('', { emitEvent: false });
      this.datasetFC.setValue('', { emitEvent: false });

      // **the fix**: swap whole FormGroups to avoid stale errors/validators
      this.replaceEnvGroups(tpl);

      // make Angular aware of the change
      this.tplFC.markAsDirty();
      this.tplFC.markAsTouched();
      this.form.markAsDirty();
      this.form.markAsTouched();
      this.form.updateValueAndValidity({ emitEvent: true });
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
            this.hydrating = true;
            this.originalExp = exp;

            //  build brand new env groups for loaded template
            this.replaceEnvGroups(tpl);

            this.form.patchValue(
              {
                name: (exp as any).name,
                description: (exp as any).description,
                visibility: (exp as any).is_public ? 'Public' : 'Private',
                experimentTemplate: tpl as any,
                model: mdl ? (mdl as any) : this.NO_MODEL_TOKEN,
                dataset: ds ? (ds as any) : this.NO_DATASET_TOKEN,
              },
              { emitEvent: false }
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
              const c = (this.form.get('envsRequired') as FormGroup).get(
                env.name
              ) as FormControl<string>;
              if (c) c.setValue(envMap.get(env.name) ?? '', { emitEvent: false });
            });
            (tpl?.envs_optional ?? []).forEach((env: any) => {
              const c = (this.form.get('envsOptional') as FormGroup).get(
                env.name
              ) as FormControl<string>;
              if (c) c.setValue(envMap.get(env.name) ?? '', { emitEvent: false });
            });

            // lock assets if there are runs
            const editableAssets = (runsCount as number) === 0;
            this.assetsLocked.set(!editableAssets);
            if (!editableAssets) {
              this.modelFC.disable({ emitEvent: false });
              this.datasetFC.disable({ emitEvent: false });
              this.tplFC.disable({ emitEvent: false });
              (this.form.get('envsRequired') as FormGroup).disable({ emitEvent: false });
              (this.form.get('envsOptional') as FormGroup).disable({ emitEvent: false });
              this.pubSearchFC.disable({ emitEvent: false });
            }

            // flush validity after hydration
            this.form.updateValueAndValidity({ emitEvent: false });

            this.hydrating = false;
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
    if (!p || this.assetsLocked()) return;
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
    if (this.assetsLocked()) return;
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

    const raw = this.form.getRawValue();
    const vis = raw.visibility === 'Public';

    const readGroup = (fg: FormGroup) =>
      (typeof (fg as any)?.getRawValue === 'function'
        ? (fg as any).getRawValue()
        : fg.value) as Record<string, unknown>;
    const toStringRecord = (obj: Record<string, unknown>): Record<string, string> => {
      const entries = Object.entries(obj || {}).map(([k, v]) => [k, v == null ? '' : String(v)]);
      return Object.fromEntries(entries) as Record<string, string>;
    };

    const envReq = toStringRecord(readGroup(this.form.get('envsRequired') as FormGroup));
    const envOpt = toStringRecord(readGroup(this.form.get('envsOptional') as FormGroup));
    const all = { ...envReq, ...envOpt };

    let env_vars = Object.entries(all)
      .filter(([, v]) => v.length > 0)
      .map(([key, value]) => ({ key, value }));

    const pubIds = this.publicationsFA.value.map((p) => String(p.identifier));

    const dsVal = raw.dataset;
    const mdlVal = raw.model;

    let dataset_ids =
      !dsVal || (typeof dsVal === 'string' && dsVal === this.NO_DATASET_TOKEN)
        ? []
        : [String((dsVal as Dataset).identifier)];

    let model_ids =
      !mdlVal || (typeof mdlVal === 'string' && mdlVal === this.NO_MODEL_TOKEN)
        ? []
        : [String((mdlVal as Model).identifier)];

    if (this.assetsLocked()) {
      if (!dataset_ids.length && (this.originalExp?.dataset_ids?.length ?? 0) > 0) {
        dataset_ids = [...(this.originalExp!.dataset_ids || [])];
      }
      if (!model_ids.length && (this.originalExp?.model_ids?.length ?? 0) > 0) {
        model_ids = [...(this.originalExp!.model_ids || [])];
      }
      if (!env_vars.length && (this.originalExp?.env_vars?.length ?? 0) > 0) {
        env_vars = (this.originalExp!.env_vars as any[]).map((ev) => ({
          key: ev.key,
          value: String(ev.value),
        }));
      }
    }

    const payload: ExperimentCreate = {
      name: String(raw.name).trim(),
      description: String(raw.description).trim(),
      publication_ids: pubIds.length
        ? pubIds
        : (this.originalExp?.publication_ids || []).map(String),
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
