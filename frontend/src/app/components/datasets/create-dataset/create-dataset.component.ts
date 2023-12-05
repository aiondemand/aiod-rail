import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Observable, Subscription, firstValueFrom, map } from 'rxjs';
import { Dataset, createDatasetFromFormData } from 'src/app/models/dataset';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { isPlatformSupported, keywordsValidator, nameValidator, platformIsSupportedValidator } from './validators';
import { Platform } from 'src/app/models/platform';


@Component({
  selector: 'app-create-dataset',
  templateUrl: './create-dataset.component.html',
  styleUrls: ['./create-dataset.component.scss']
})
export class CreateDatasetComponent implements OnInit, OnDestroy {
  datasetForm = this.fb.group({
    name: ['', [Validators.required, nameValidator]],
    description: ['', Validators.required],
    platform: ['', [Validators.required, platformIsSupportedValidator]],
    version: ['', Validators.required],
    alternateNames: '',
    keywords: ['', keywordsValidator],
    huggingface: this.fb.group({
      username: '',
      secretToken: '',
      file: '',
      fileSource: new FormControl(''),
    })
  });

  createDatasetSubscription: Subscription | null = null;
  submitButtonDisabled: boolean = false;
  error: string = '';
  platforms$: Observable<Platform[]> = this.backend.getPlatforms()
    .pipe(
      map(platforms =>
        // Show supported platforms first
        platforms.sort((a, b) =>
          isPlatformSupported(a) == isPlatformSupported(b)
            ? 0
            : isPlatformSupported(a) ? -1 : 1
        )
      )
    );

  constructor(
    private fb: FormBuilder,
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Trigger validation when platform changes as they depend on it
    this.datasetForm.get('platform')?.valueChanges.subscribe(_ => {
      this.datasetForm.get('name')?.updateValueAndValidity();
      this.datasetForm.get('keywords')?.updateValueAndValidity();
    });
  }

  ngOnDestroy(): void {
    this.createDatasetSubscription?.unsubscribe();
  }

  get platformValue(): string {
    return this.datasetForm.get('platform')?.value?.toString() || '';
  }

  get huggingfaceFormGroup() {
    return this.datasetForm.get('huggingface') as FormGroup;
  }

  isPlatformSupported(platform: Platform | string): boolean {
    return isPlatformSupported(platform);
  }

  async onSubmit() {
    this.error = '';
    this.submitButtonDisabled = true;
    this.createDatasetSubscription?.unsubscribe();

    let datasetFormValue = this.datasetForm.value;

    // let datasetName = String(datasetFormValue.name)
    // if (datasetFormValue.huggingface) {
    //   let username = String(datasetFormValue.huggingface?.username)
    //   datasetName = `${username}/${datasetName}`
    // }
    
    let dataset = createDatasetFromFormData({
      name: String(datasetFormValue.name).trim(),
      description: String(datasetFormValue.description).trim(),
      platform: String(datasetFormValue.platform),
      version: String(datasetFormValue.version).trim(),
      alternateNames: String(datasetFormValue.alternateNames),
      keywords: String(datasetFormValue.keywords),
      huggingface: { username: String(datasetFormValue.huggingface?.username) }
    });

    this.createDatasetSubscription = this.backend.createDataset(
      dataset,
      this.datasetForm.get('huggingface.fileSource')?.value,
      String(this.datasetForm.get('huggingface.username')?.value),
      String(this.datasetForm.get('huggingface.secretToken')?.value)
    ).subscribe({
      next: (dataset: Dataset) => {
        this.snackBar.show('Dataset created successfully.', 'Close');
        this.router.navigate(['/datasets', dataset.identifier]);
      },
      error: (error) => {
        this.snackBar.showError('Dataset could not be created.', 'Close');
        this.error = `Dataset could not be created. Detail: ${error}`;
        this.submitButtonDisabled = false;
      },
      complete: () => {
        this.submitButtonDisabled = false;
      }
    });
  }
}
