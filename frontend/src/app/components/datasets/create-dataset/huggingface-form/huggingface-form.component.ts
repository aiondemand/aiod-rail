import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-huggingface-form',
  templateUrl: './huggingface-form.component.html',
  styleUrls: ['./huggingface-form.component.scss']
})
export class HuggingfaceFormComponent implements OnInit, OnDestroy {
  @Input() formGroup: FormGroup;

  ngOnInit(): void {
    for(let controlName in this.formGroup.controls) {
      this.formGroup.get(controlName)?.setValidators(Validators.required);
    }
  }

  ngOnDestroy(): void {
    for(let controlName in this.formGroup.controls) {
      let control = this.formGroup.get(controlName);
      if(control) {
        control.clearValidators();
        control.updateValueAndValidity();
      }
    }
  }

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.formGroup.patchValue({
        fileSource: file
      });
    }
  }
}
