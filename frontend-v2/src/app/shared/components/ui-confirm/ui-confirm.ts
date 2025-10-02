import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { UiButton } from '../ui-button/ui-button';

export type UiConfirmResult = 'yes' | 'no' | 'third';

export interface UiConfirmData {
  message: string;

  acceptBtnMessage?: string; // default: "Confirm"

  declineBtnMessage?: string; // default: "Dismiss"

  thirdOptionBtnMessage?: string;
}

@Component({
  selector: 'ui-confirm',
  standalone: true,
  imports: [CommonModule, MatDialogModule, UiButton],
  templateUrl: './ui-confirm.html',
  styleUrls: ['./ui-confirm.scss'],
})
export class UiConfirmComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: UiConfirmData,
    private ref: MatDialogRef<UiConfirmComponent, UiConfirmResult>
  ) {}

  yes() {
    this.ref.close('yes');
  }
  no() {
    this.ref.close('no');
  }
  third() {
    this.ref.close('third');
  }
}
