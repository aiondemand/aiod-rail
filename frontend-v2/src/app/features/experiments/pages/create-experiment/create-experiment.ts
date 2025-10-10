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

  // ----- state
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

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

  // --- autocomplet
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

  modelsMine$ = this.modelFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => (typeof q === 'string' ? this.api.getMyModels(q) : of([]))),
    catchError((err) => {
      this.fail("Couldn't load my models", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  modelsPublic$ = this.modelFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => (typeof q === 'string' ? this.api.getModels(q) : of([]))),
    catchError((err) => {
      this.fail("Couldn't load models", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  datasetsMine$ = this.datasetFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => (typeof q === 'string' ? this.api.getMyDatasets(q) : of([]))),
    catchError((err) => {
      this.fail("Couldn't load my datasets", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  datasetsPublic$ = this.datasetFC.valueChanges.pipe(
    debounceTime(250),
    startWith(''),
    switchMap((q) => (typeof q === 'string' ? this.api.getDatasets(q) : of([]))),
    catchError((err) => {
      this.fail("Couldn't load datasets", err);
      return of([]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  publications$ = this.api.getPublications().pipe(
    catchError((err) => {
      this.fail("Couldn't load publications", err);
      return of([] as Publication[]);
    }),
    takeUntilDestroyed(this.destroyRef)
  );

  ngOnInit(): void {
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

    // --- UPDATE
    const expId = this.route.snapshot.paramMap.get('id');
    if (expId && /\/experiments\/[^/]+\/update$/.test(this.router.url)) {
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
                model: mdl as any,
                dataset: ds as any,
              },
              { emitEvent: true }
            );
            this.selectedTemplate.set(tpl as any);

            this.publicationsFA.clear();
            (pubs || []).forEach((p: Publication) =>
              this.publicationsFA.push(new FormControl(p, { nonNullable: true }))
            );

            // ENVs
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

  // UI
  displayTpl = (t?: ExperimentTemplate) => (t ? t.name : '');
  displayModel = (m?: Model) => (m ? m.name : '');
  displayDataset = (d?: Dataset) => (d ? d.name : '');

  addPublication(p: Publication) {
    if (this.publicationsFA.controls.some((c) => c.value.identifier === p.identifier)) return;
    this.publicationsFA.push(new FormControl(p, { nonNullable: true }));
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

    const envReq = this.envsReqFG.value as Record<string, string>;
    const envOpt = this.envsOptFG.value as Record<string, string>;
    const all = { ...envReq, ...envOpt };

    const env_vars = Object.entries(all)
      .filter(([, v]) => !!v && String(v).length > 0)
      .map(([key, value]) => ({ key, value }));

    const pubIds = this.publicationsFA.value.map((p) => String(p.identifier));

    const ds = this.datasetFC.value as Dataset;
    const mdl = this.modelFC.value as Model;

    const payload: ExperimentCreate = {
      name: String(this.form.controls.name.value).trim(),
      description: String(this.form.controls.description.value).trim(),
      publication_ids: pubIds,
      experiment_template_id: tpl.id,
      dataset_ids: [String(ds.identifier)],
      model_ids: [String(mdl.identifier)],
      env_vars,
      is_public: vis,
    };

    this.loading.set(true);
    this.api
      .createExperiment(payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (exp: Experiment) => {
          this.snack.show('Experiment created');
          this.router.navigate(['/experiments', exp.id]);
        },
        error: (err) => {
          this.fail(`Couldn't create experiment`, err);
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
