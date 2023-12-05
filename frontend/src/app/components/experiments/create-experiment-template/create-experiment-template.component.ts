import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSelectChange } from '@angular/material/select';
import { Router } from '@angular/router';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

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
    pipRequirements: ['', Validators.required],
    script: ['', Validators.required],
  });

  base_images: string[] = [
    "python:3.9",
    "python:3.10",
    "python:3.11",
    "python:3.12"
  ]

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

  }

  onSelectBaseImage(event: MatSelectChange) {

  }
}
